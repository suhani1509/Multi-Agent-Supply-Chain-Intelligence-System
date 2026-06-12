from crewai.tools import tool
from data.email_mock import MOCK_EMAILS


@tool("Email Reader Tool")
def read_vendor_emails() -> str:
    """
    Reads vendor emails from mock data
    """

    email_text = ""

    for email in MOCK_EMAILS:
        email_text += f"""
From: {email['from']}
Subject: {email['subject']}
Date: {email['date']}
Body: {email['body']}

----------------------------------
"""

    return email_text