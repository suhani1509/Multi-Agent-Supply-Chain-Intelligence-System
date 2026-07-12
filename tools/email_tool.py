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

        body = base64.urlsafe_b64decode(
            body
        ).decode(
            "utf-8",
            errors="ignore"
        )

    return body


def clean_email_body(body):

    cleaned_lines = []

    ignore_keywords = [

        "Regards",
        "Best regards",
        "Thanks",
        "Thank you",
        "Senior Supply Chain Executive",
        "Procurement Team",
        "Account Manager",
        "Customer Care",
        "Sent from my iPhone"

    ]

    lines = body.split("\n")

    for line in lines:

        line = line.strip()

        if not line:

            continue

        skip = False

        for keyword in ignore_keywords:

            if keyword.lower() in line.lower():

                skip = True

                break

        if not skip:

            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


@tool("Email Reader Tool")
def read_vendor_emails():

    """
    Reads vendor emails.

    Returns sender, subject, date and email content.

    """

    service = authenticate_gmail()

    results = service.users().messages().list(

        userId="me",

        maxResults=5,

        q="newer_than:30d"

    ).execute()

    messages = results.get("messages", [])

    if not messages:

        return "No emails found."

    output = ""

    for msg in messages:

        message = service.users().messages().get(

            userId="me",

            id=msg["id"],

            format="full"

        ).execute()

        payload = message["payload"]

        headers = payload["headers"]

        sender = "N/A"

        subject = "N/A"

        date = "N/A"

        for h in headers:

            if h["name"] == "From":

                sender = h["value"]

            elif h["name"] == "Subject":

                subject = h["value"]

            elif h["name"] == "Date":

                date = h["value"]

        body = get_email_body(payload)

        body = clean_email_body(body)

        output += f"""

==================================================

FROM: {sender}

SUBJECT: {subject}

DATE: {date}

EMAIL CONTENT:

{body}

IMPORTANT INSTRUCTIONS:

- This email content is the ONLY source of truth.
- Do not infer anything.
- Do not invent products.
- Do not invent suppliers.
- Do not invent shipment status.
- Do not invent urgent requests.
- Do not invent supplier issues.
- Use only the information explicitly written above.

==================================================

"""

    return output