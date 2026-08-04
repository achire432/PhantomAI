"""
PDF SERVICE
============
Purpose: Generate PDF files from PhantomAI data.

Why This Matters:
- Users need to export reports
- Professional documents
- Shareable output

How It Works:
1. Takes data (conversation, notes, tasks)
2. Creates a PDF using ReportLab
3. Returns the PDF file

What Would Happen Without This:
- No way to generate reports
- Data stays in the database only
- Less shareable
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime

def generate_conversation_pdf(conversation_data: dict) -> BytesIO:
    """
    Generate a PDF from a conversation.
    
    Parameters:
    - conversation_data: {
        "title": "My Chat",
        "messages": [{"role": "user", "content": "Hello"}, ...],
        "created_at": "2026-08-04"
    }
    
    Returns:
    - BytesIO object containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#00d4ff'),
        spaceAfter=12
    )
    
    message_style = ParagraphStyle(
        'MessageStyle',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=20,
        spaceAfter=6
    )
    
    user_style = ParagraphStyle(
        'UserStyle',
        parent=message_style,
        textColor=colors.HexColor('#1a3a6e'),
        fontName='Helvetica-Bold'
    )
    
    assistant_style = ParagraphStyle(
        'AssistantStyle',
        parent=message_style,
        textColor=colors.HexColor('#2a2a3e')
    )
    
    # Build document
    story = []
    
    # Title
    story.append(Paragraph(f"🧠 {conversation_data.get('title', 'Conversation')}", title_style))
    
    # Metadata
    meta_style = ParagraphStyle('MetaStyle', parent=styles['Normal'], fontSize=10, textColor=colors.grey)
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", meta_style))
    if conversation_data.get('created_at'):
        story.append(Paragraph(f"Started: {conversation_data['created_at']}", meta_style))
    story.append(Spacer(1, 20))
    
    # Messages
    for msg in conversation_data.get('messages', []):
        role = msg.get('role', 'unknown')
        content = msg.get('content', '')
        
        if role == 'user':
            story.append(Paragraph(f"👤 You:", user_style))
            story.append(Paragraph(content, message_style))
        else:
            story.append(Paragraph(f"🤖 Phantom AI:", assistant_style))
            story.append(Paragraph(content, message_style))
        
        story.append(Spacer(1, 8))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("--- End of Conversation ---", styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_notes_pdf(notes_data: list) -> BytesIO:
    """
    Generate a PDF from notes.
    
    Parameters:
    - notes_data: [{"title": "Note 1", "content": "...", "created_at": "..."}]
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("📝 My Notes", styles['Heading1']))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    for note in notes_data:
        story.append(Paragraph(note.get('title', 'Untitled'), styles['Heading2']))
        story.append(Paragraph(note.get('content', ''), styles['Normal']))
        if note.get('created_at'):
            story.append(Paragraph(f"Created: {note['created_at']}", styles['Italic']))
        story.append(Spacer(1, 12))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_tasks_pdf(tasks_data: list) -> BytesIO:
    """
    Generate a PDF from tasks.
    
    Parameters:
    - tasks_data: [{"title": "Task 1", "status": "pending", "priority": "high"}]
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("✅ My Tasks", styles['Heading1']))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Table data
    table_data = [["Task", "Status", "Priority", "Due Date"]]
    
    for task in tasks_data:
        table_data.append([
            task.get('title', ''),
            task.get('status', 'pending'),
            task.get('priority', 'medium'),
            task.get('due_date', '')[:10] if task.get('due_date') else ''
        ])
    
    # Create table
    table = Table(table_data, colWidths=[200, 80, 80, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3a6e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer