import base64
from crewai.tools import tool
from tools.gmail_tool import authenticate_gmail


def get_email_body(payload):
    """
    Extract plain text or HTML body from Gmail message.
    """

    body = ""

    # Simple email
    if payload.get("body") and payload["body"].get("data"):
        body = payload["body"]["data"]

    # Multipart email
    elif "parts" in payload:
        for part in payload["parts"]:

            mime = part.get("mimeType")

            if mime == "text/plain":
                body = part["body"].get("data", "")
                break

            elif mime == "text/html" and not body:
                body = part["body"].get("data", "")

    if body:
        body = base64.urlsafe_b64decode(body).decode("utf-8", errors="ignore")

    return body


@tool("Email Reader Tool")
def read_vendor_emails():
    """
    Reads latest vendor emails with subject, sender and body.
    """

    service = authenticate_gmail()

    results = service.users().messages().list(
        userId="me",
        maxResults=20
    ).execute()

    messages = results.get("messages", [])

    output = ""

    for msg in messages:

        message = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        payload = message["payload"]
        headers = payload["headers"]

        sender = ""
        subject = ""
        date = ""

        for h in headers:

            if h["name"] == "From":
                sender = h["value"]

            elif h["name"] == "Subject":
                subject = h["value"]

            elif h["name"] == "Date":
                date = h["value"]

        body = get_email_body(payload)

        output += f"""
From: {sender}
Subject: {subject}
Date: {date}

Body:
{body}

------------------------------------------------------
"""

    return output