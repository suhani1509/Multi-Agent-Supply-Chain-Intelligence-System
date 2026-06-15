from crewai import Task
from agents.email_agent import email_agent

email_task = Task(
    description="""
    Read vendor emails using the Email Reader Tool.

    STRICT RULES:
    - Use ONLY the emails returned by the tool.
    - Do NOT invent suppliers.
    - Do NOT invent products.
    - Do NOT invent delays.
    - Do NOT invent urgent requests.
    - Do NOT invent supply chain risks.
    - If information is not present in the emails, do not mention it.

    Identify only:
    - Delayed shipments
    - Urgent requests explicitly mentioned
    - Supplier issues explicitly mentioned

    Report facts only.
    """,

    expected_output="""
    Email Summary

    Delayed Shipments:
    - Supplier
    - Product
    - Reason
    - New Delivery Date

   
    Urgent Requests:
    Only include requests where the supplier is explicitly asking
    for immediate action, urgent delivery, urgent quotation,
    or urgent material requirements.

    Do NOT classify delay notifications or production issues
    as urgent requests.

    Supplier Issues:
    - Only if explicitly present

    No assumptions.
    No forecasting.
    No invented suppliers.
    IMPORTANT:
    The tool returns the complete list of emails.

    You MUST ONLY report information present in the emails.
    The total number of emails analyzed must match the number returned by the tool.

    If the tool returns 3 emails, your report must be based only on those 3 emails.

    Do not mention any supplier, product, delay, issue, or request not explicitly present in the emails.
    """,

    agent=email_agent
)