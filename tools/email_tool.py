from crewai.tools import tool
from data.email_mock import MOCK_EMAILS
import json

@tool("Email Reader Tool")
def read_vendor_emails():
    """
    Reads vendor emails from mock data.
    """

    return json.dumps(MOCK_EMAILS, indent=2)