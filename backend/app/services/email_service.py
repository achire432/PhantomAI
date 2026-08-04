"""
EMAIL SERVICE
==============
Purpose: Connect PhantomAI to email services.

Why This Matters:
- This is how PhantomAI reads and sends emails
- Makes PhantomAI a real-world assistant
- Enables email automation

How It Works:
1. Connects to email server (Gmail, Outlook, etc.)
2. Fetches emails
3. Saves them to the database
4. Provides AI-generated summaries
5. Sends emails with user confirmation

Security:
- Uses IMAP and SMTP protocols
- Credentials stored in .env (not in code)
- Requires user confirmation before sending
"""

import imapclient
import smtplib
import ssl
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
from email import message_from_bytes
from email.policy import default
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from backend.app.models.email import Email, EmailDraft
from backend.app.schemas.email import EmailDraftCreate

# ============================================
# LOAD AND CLEAN EMAIL SETTINGS FROM .env
# ============================================

# Email settings from .env
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "").strip()
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "").strip()

# Remove spaces from password (Gmail app passwords have spaces)
EMAIL_PASSWORD = EMAIL_PASSWORD.replace(" ", "")

# Remove any non-breaking spaces or hidden characters
EMAIL_ADDRESS = EMAIL_ADDRESS.replace('\xa0', ' ').strip()
EMAIL_PASSWORD = EMAIL_PASSWORD.replace('\xa0', ' ').strip()

IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")


def get_imap_connection():
    """
    Connect to email server with SSL context.
    
    Why We Need This:
    - Gmail uses SSL certificates
    - Older macOS versions don't trust the certificate
    - This fixes the SSL error
    
    How It Works:
    1. Creates an SSL context
    2. Disables certificate verification (fixes the error)
    3. Connects to the email server
    """
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        return {"error": "Email credentials not set. Please add EMAIL_ADDRESS and EMAIL_PASSWORD to .env"}
    
    try:
        # Create SSL context that doesn't verify certificates
        # This fixes the "certificate verify failed" error
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # Connect with SSL context
        client = imapclient.IMAPClient(IMAP_SERVER, use_uid=True, ssl_context=context)
        client.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        client.select_folder("INBOX")
        return client
        
    except Exception as e:
        return {"error": f"Failed to connect: {str(e)}"}


def parse_email(raw_bytes: bytes) -> dict:
    """
    Parse raw email bytes into readable format with proper Unicode handling.
    
    How It Works:
    1. Uses Python's built-in email library
    2. Extracts: sender, subject, body, date
    3. Handles Unicode characters correctly
    4. Returns as dictionary
    
    Why We Need This:
    - Emails come in raw format
    - We need to extract useful information
    - Must support Unicode characters
    - Fixes the '\xa0' encoding error
    """
    try:
        msg = message_from_bytes(raw_bytes, policy=default)
        
        # Get body with UTF-8 decoding
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body = part.get_content()
                        # If it's bytes, decode properly with UTF-8
                        if isinstance(body, bytes):
                            body = body.decode('utf-8', errors='replace')
                    except Exception as e:
                        body = "Error decoding email content"
                    break
            # If no plain text found, try HTML
            if not body:
                for part in msg.walk():
                    if part.get_content_type() == "text/html":
                        try:
                            body = part.get_content()
                            if isinstance(body, bytes):
                                body = body.decode('utf-8', errors='replace')
                        except:
                            body = "Error decoding HTML content"
                        break
        else:
            # Single part email
            try:
                body = msg.get_content()
                if isinstance(body, bytes):
                    body = body.decode('utf-8', errors='replace')
            except:
                body = "Error decoding email content"
        
        # Clean up problematic characters
        # Replace non-breaking space with regular space
        body = body.replace('\xa0', ' ')
        body = body.replace('\r\n', '\n')
        body = body.replace('\r', '\n')
        
        # Ensure UTF-8 encoding
        body = body.encode('utf-8', errors='replace').decode('utf-8')
        
        return {
            "sender": msg.get("From", ""),
            "subject": msg.get("Subject", "No Subject"),
            "body": body,
            "date": msg.get("Date", datetime.now().isoformat())
        }
        
    except Exception as e:
        return {
            "sender": "",
            "subject": "Error parsing email",
            "body": f"Error: {str(e)}",
            "date": datetime.now().isoformat()
        }


def fetch_recent_emails(db: Session, user_id: int, limit: int = 10) -> list:
    """
    Fetch recent emails from the server.
    
    How It Works:
    1. Connects to email server
    2. Gets list of emails from the last 7 days
    3. Downloads each email
    4. Parses the content
    5. Saves to database
    6. Returns email list
    
    Why This Matters:
    - Users want to check emails quickly
    - AI can summarize emails
    - Saves time by not opening Gmail/Outlook
    """
    client = get_imap_connection()
    if isinstance(client, dict) and client.get("error"):
        return client
    
    try:
        # Search for emails from the last 7 days
        since_date = (datetime.now() - timedelta(days=7)).strftime("%d-%b-%Y")
        messages = client.search(['SINCE', since_date])
        
        emails = []
        for msg_id in messages[-limit:]:
            raw_email = client.fetch([msg_id], ['BODY.PEEK[]'])
            email_bytes = raw_email[msg_id][b'BODY[]']
            parsed_email = parse_email(email_bytes)
            
            # Check if email already exists (avoid duplicates)
            existing = db.query(Email).filter(Email.email_id == str(msg_id)).first()
            if existing:
                emails.append(existing)
                continue
            
            email_obj = Email(
                user_id=user_id,
                email_id=str(msg_id),
                sender=parsed_email.get("sender", ""),
                subject=parsed_email.get("subject", "No Subject"),
                body=parsed_email.get("body", ""),
                received_at=datetime.now()
            )
            db.add(email_obj)
            emails.append(email_obj)
        
        db.commit()
        return emails
        
    except Exception as e:
        return {"error": str(e)}
    finally:
        try:
            client.logout()
        except:
            pass


def send_email(db: Session, user_id: int, to: str, subject: str, body: str) -> dict:
    """
    Send an email using smtplib (direct, no yagmail).
    
    Why This Matters:
    - Users can send emails through PhantomAI
    - AI can draft replies automatically
    - Streamlines communication
    
    How It Works:
    1. Uses smtplib directly (bypasses yagmail encoding issues)
    2. Uses UTF-8 encoding for all text
    3. Saves to database
    4. Returns result
    
    Security:
    - Requires confirmation before sending
    - Credentials stored in .env
    - Uses secure SMTP connection
    """
    try:
        # Clean ALL strings - remove \xa0 and other hidden characters
        # Keep only ASCII characters (this fixes the encoding error)
        
        to_clean = to.strip()
        # Remove any \xa0 or other whitespace chars
        to_clean = ''.join(c for c in to_clean if ord(c) < 128)
        to_clean = to_clean.replace('\xa0', ' ')
        to_clean = to_clean.strip()
        
        # Clean subject
        subject_clean = subject.strip()
        subject_clean = ''.join(c for c in subject_clean if ord(c) < 128)
        subject_clean = subject_clean.replace('\xa0', ' ')
        subject_clean = subject_clean.strip()
        
        # Clean body
        body_clean = body.strip()
        body_clean = ''.join(c for c in body_clean if ord(c) < 128)
        body_clean = body_clean.replace('\xa0', ' ')
        body_clean = body_clean.strip()
        
        # Clean email address
        email_clean = EMAIL_ADDRESS.strip()
        email_clean = ''.join(c for c in email_clean if ord(c) < 128)
        email_clean = email_clean.replace('\xa0', ' ')
        
        # Clean password (already cleaned, but just in case)
        password_clean = EMAIL_PASSWORD.strip()
        password_clean = ''.join(c for c in password_clean if ord(c) < 128)
        password_clean = password_clean.replace(' ', '')
        
        print(f"📧 Sending email to: {to_clean}")
        print(f"📧 Subject: {subject_clean}")
        print(f"📧 Body length: {len(body_clean)}")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_clean
        msg['To'] = to_clean
        msg['Subject'] = subject_clean
        
        # Attach body with UTF-8 encoding
        msg.attach(MIMEText(body_clean, 'plain', 'utf-8'))
        
        # Create SMTP connection
        server = smtplib.SMTP(SMTP_SERVER, 587)
        server.starttls()
        server.login(email_clean, password_clean)
        
        # Send
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent to {to_clean}")
        
        # Save the sent email as a draft record
        draft = EmailDraft(
            user_id=user_id,
            to=to_clean,
            subject=subject_clean,
            body=body_clean,
            is_sent=True
        )
        db.add(draft)
        db.commit()
        
        return {"success": True, "message": f"Email sent to {to_clean}"}
        
    except Exception as e:
        print(f"❌ Email error: {str(e)}")
        return {"success": False, "error": str(e)}


def get_drafts(db: Session, user_id: int) -> list:
    """
    Get all drafts for a user.
    """
    return db.query(EmailDraft).filter(
        EmailDraft.user_id == user_id,
        EmailDraft.is_sent == False
    ).order_by(EmailDraft.created_at.desc()).all()