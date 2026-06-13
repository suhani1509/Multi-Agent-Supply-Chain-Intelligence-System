from crewai import Task
from agents.email_agent import email_agent

email_task = Task(
    description="""
    Read all vendor emails and identify:

    - Delayed shipments
    - Urgent requests
    - Supplier issues
    - Supply chain risks

    Provide a concise summary.
    """,
    expected_output="Summary of email findings",
    agent=email_agent
)