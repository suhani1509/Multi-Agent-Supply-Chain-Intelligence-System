from crewai.tools import tool
from tools.gmail_tool import authenticate_gmail


@tool("Email Reader Tool")
def read_vendor_emails():
    """
    Reads vendor emails from Gmail inbox.
    """

    service = authenticate_gmail()

    results = service.users().messages().list(
        userId='me',
        maxResults=20
    ).execute()

    messages = results.get('messages', [])

    output = ""

    for msg in messages:

        message = service.users().messages().get(
            userId='me',
            id=msg['id']
        ).execute()

        headers = message['payload']['headers']

        sender = ""
        subject = ""

        for h in headers:

            if h['name'] == 'From':
                sender = h['value']

            elif h['name'] == 'Subject':
                subject = h['value']

        output += f"""
From: {sender}
Subject: {subject}

-----------------------------------
"""

    return output