from crewai import Task

from agents.manager_agent import manager_agent
from tasks.email_task import email_task
from tasks.inventory_task import inventory_task

manager_task = Task(
    description="""
    Review email findings and inventory findings.

    Identify critical risks and provide
    final supply chain recommendations.
    STRICT RULES:

    - Use only Email Agent and Inventory Agent outputs.
    - Do not assume missing inventory data.
    - Treat supplier email domain and supplier name as the same supplier if clearly related.
    - Separate FACTS from RECOMMENDATIONS.
    - Recommendations must be based only on identified risks.
    - Do not invent suppliers, inventory levels, demand forecasts, or future shortages.
    Treat supplier email domains and supplier names as the same supplier
    when they clearly refer to the same organization.

    Example:
    kumar@partsco.com = Kumar Parts Co
    """,
    expected_output="Final supply chain action plan",
    agent=manager_agent,
    context=[email_task, inventory_task]
)