"""
PhantomAI Web Reader

Fetches a public webpage and extracts readable text from it.

Used by:
- Web Search Tool
- Webpage Reader
- AI Summarization
- Ask AI About Webpage
- Future Research Mode
"""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


# ============================================================
# CONFIGURATION
# ============================================================

REQUEST_TIMEOUT = 15

# Maximum amount of webpage text PhantomAI will keep.
# This prevents extremely large webpages from consuming memory
# or being sent unnecessarily to the AI model.
MAX_CONTENT_LENGTH = 120_000

# Maximum downloaded response size.
MAX_DOWNLOAD_SIZE = 5_000_000

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/150.0.0.0 Safari/537.36 "
    "PhantomAI-WebReader/1.0"
)


# ============================================================
# URL VALIDATION
# ============================================================

def validate_url(url: str) -> tuple[bool, str]:
    """
    Validate a URL before PhantomAI attempts to access it.

    Only HTTP and HTTPS URLs are allowed.

    Also blocks localhost and private/internal IP addresses
    to reduce SSRF/security risks.
    """

    if not url or not url.strip():
        return False, "URL cannot be empty."

    url = url.strip()

    try:
        parsed = urlparse(url)

        if parsed.scheme not in {"http", "https"}:
            return False, "Only HTTP and HTTPS URLs are supported."

        if not parsed.hostname:
            return False, "Invalid URL."

        hostname = parsed.hostname.lower()

        # Block obvious localhost/internal names.
        blocked_hostnames = {
            "localhost",
            "localhost.localdomain",
            "ip6-localhost",
            "ip6-loopback",
        }

        if hostname in blocked_hostnames:
            return False, "Access to local addresses is not allowed."

        # If hostname itself is an IP address, check it.
        try:
            ip = ipaddress.ip_address(hostname)

            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_reserved
                or ip.is_multicast
            ):
                return (
                    False,
                    "Access to private or internal addresses is not allowed.",
                )

        except ValueError:
            # Hostname is not an IP address.
            pass

        # Resolve hostname and check resulting IP addresses.
        try:
            addresses = socket.getaddrinfo(
                hostname,
                None,
            )

            for address in addresses:
                ip_text = address[4][0]

                try:
                    ip = ipaddress.ip_address(ip_text)

                    if (
                        ip.is_private
                        or ip.is_loopback
                        or ip.is_link_local
                        or ip.is_reserved
                        or ip.is_multicast
                    ):
                        return (
                            False,
                            "The URL resolves to a private or internal address.",
                        )

                except ValueError:
                    continue

        except socket.gaierror:
            return False, "Unable to resolve the website address."

        return True, ""

    except Exception as error:
        return False, f"Invalid URL: {str(error)}"


# ============================================================
# DOWNLOAD WEBPAGE
# ============================================================

def fetch_webpage(url: str) -> dict:
    """
    Download a webpage safely.

    Returns structured information that can later be consumed
    by the webpage reader, AI summarizer and research tools.
    """

    valid, error = validate_url(url)

    if not valid:
        return {
            "success": False,
            "url": url,
            "error": error,
        }

    url = url.strip()

    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": (
                    "text/html,application/xhtml+xml,"
                    "application/xml;q=0.9,*/*;q=0.8"
                ),
            },
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
            stream=True,
        )

        # Check the final redirected URL too.
        final_url = response.url

        valid_final, final_error = validate_url(
            final_url
        )

        if not valid_final:
            response.close()

            return {
                "success": False,
                "url": url,
                "error": final_error,
            }

        if response.status_code >= 400:
            response.close()

            return {
                "success": False,
                "url": url,
                "status_code": response.status_code,
                "error": (
                    f"Website returned HTTP "
                    f"{response.status_code}."
                ),
            }

        content_type = (
            response.headers.get(
                "Content-Type",
                "",
            )
            .lower()
        )

        # We currently focus on webpages.
        if (
            "text/html" not in content_type
            and "application/xhtml+xml" not in content_type
        ):
            response.close()

            return {
                "success": False,
                "url": url,
                "content_type": content_type,
                "error": (
                    "This URL does not contain a supported "
                    "HTML webpage."
                ),
            }

        # ----------------------------------------------------
        # DOWNLOAD WITH SIZE LIMIT
        # ----------------------------------------------------

        chunks = []
        total_size = 0

        for chunk in response.iter_content(
            chunk_size=8192
        ):
            if not chunk:
                continue

            total_size += len(chunk)

            if total_size > MAX_DOWNLOAD_SIZE:
                response.close()

                return {
                    "success": False,
                    "url": url,
                    "error": (
                        "The webpage is too large for PhantomAI "
                        "to process safely."
                    ),
                }

            chunks.append(chunk)

        response.close()

        raw_content = b"".join(chunks)

        # Try to decode using the server's detected encoding.
        encoding = (
            response.encoding
            or response.apparent_encoding
            or "utf-8"
        )

        try:
            html = raw_content.decode(
                encoding,
                errors="replace",
            )

        except Exception:
            html = raw_content.decode(
                "utf-8",
                errors="replace",
            )

        return {
            "success": True,
            "url": url,
            "final_url": final_url,
            "status_code": response.status_code,
            "content_type": content_type,
            "html": html,
        }

    except requests.Timeout:
        return {
            "success": False,
            "url": url,
            "error": (
                "The website took too long to respond."
            ),
        }

    except requests.ConnectionError:
        return {
            "success": False,
            "url": url,
            "error": (
                "Unable to connect to the website."
            ),
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "url": url,
            "error": (
                f"Unable to fetch webpage: {str(error)}"
            ),
        }

    except Exception as error:
        return {
            "success": False,
            "url": url,
            "error": (
                f"Unexpected webpage error: {str(error)}"
            ),
        }


# ============================================================
# EXTRACT PAGE TITLE
# ============================================================

def extract_title(soup: BeautifulSoup) -> str:
    """
    Extract the best available webpage title.
    """

    if soup.title:
        title = soup.title.get_text(
            " ",
            strip=True,
        )

        if title:
            return title

    og_title = soup.find(
        "meta",
        property="og:title",
    )

    if og_title:
        content = og_title.get("content", "")

        if content:
            return content.strip()

    return "Untitled webpage"


# ============================================================
# EXTRACT WEBPAGE TEXT
# ============================================================

def extract_webpage_text(
    html: str,
) -> dict:
    """
    Convert raw HTML into clean readable text.

    Removes:
    - scripts
    - styles
    - navigation
    - advertisements
    - forms
    - noscript elements

    Attempts to prioritize the main article/content area.
    """

    if not html or not html.strip():
        return {
            "success": False,
            "error": "Webpage contains no readable content.",
        }

    try:
        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        title = extract_title(soup)

        # ----------------------------------------------------
        # REMOVE UNNECESSARY ELEMENTS
        # ----------------------------------------------------

        unwanted_tags = [
            "script",
            "style",
            "noscript",
            "svg",
            "canvas",
            "iframe",
            "form",
            "nav",
            "footer",
            "header",
            "aside",
        ]

        for tag_name in unwanted_tags:
            for tag in soup.find_all(tag_name):
                tag.decompose()

        # ----------------------------------------------------
        # TRY TO FIND MAIN CONTENT
        # ----------------------------------------------------

        main_content = (
            soup.find("article")
            or soup.find("main")
            or soup.find(
                "div",
                attrs={
                    "role": "main",
                },
            )
        )

        if main_content:
            text_source = main_content
        else:
            text_source = soup.body or soup

        # ----------------------------------------------------
        # EXTRACT TEXT
        # ----------------------------------------------------

        text = text_source.get_text(
            separator="\n",
            strip=True,
        )

        # ----------------------------------------------------
        # CLEAN TEXT
        # ----------------------------------------------------

        lines = []

        for line in text.splitlines():
            line = " ".join(
                line.strip().split()
            )

            if not line:
                continue

            lines.append(line)

        cleaned_text = "\n".join(lines)

        # Remove excessive repeated blank lines.
        while "\n\n\n" in cleaned_text:
            cleaned_text = cleaned_text.replace(
                "\n\n\n",
                "\n\n",
            )

        # ----------------------------------------------------
        # LIMIT CONTENT
        # ----------------------------------------------------

        truncated = False

        if len(cleaned_text) > MAX_CONTENT_LENGTH:
            cleaned_text = (
                cleaned_text[
                    :MAX_CONTENT_LENGTH
                ].rstrip()
                + "\n\n[Content truncated by PhantomAI.]"
            )

            truncated = True

        if not cleaned_text.strip():
            return {
                "success": False,
                "title": title,
                "error": (
                    "PhantomAI could not extract readable "
                    "text from this webpage."
                ),
            }

        return {
            "success": True,
            "title": title,
            "text": cleaned_text,
            "character_count": len(cleaned_text),
            "truncated": truncated,
        }

    except Exception as error:
        return {
            "success": False,
            "error": (
                f"Unable to extract webpage text: {str(error)}"
            ),
        }


# ============================================================
# READ WEBPAGE
# ============================================================

def read_webpage(url: str) -> dict:
    """
    Fetch a webpage and return clean readable text.

    This is the main function the FastAPI router will use.
    """

    webpage = fetch_webpage(url)

    if not webpage.get("success"):
        return webpage

    extraction = extract_webpage_text(
        webpage.get("html", "")
    )

    if not extraction.get("success"):
        return {
            "success": False,
            "url": url,
            "final_url": webpage.get(
                "final_url",
                url,
            ),
            "error": extraction.get(
                "error",
                "Unable to read webpage.",
            ),
        }

    return {
        "success": True,
        "url": url,
        "final_url": webpage.get(
            "final_url",
            url,
        ),
        "title": extraction.get(
            "title",
            "Untitled webpage",
        ),
        "text": extraction.get(
            "text",
            "",
        ),
        "character_count": extraction.get(
            "character_count",
            0,
        ),
        "truncated": extraction.get(
            "truncated",
            False,
        ),
    }