from crewai import Task
from agents.inventory_agent import inventory_agent

inventory_task = Task(
    description="""
    Analyze inventory data and identify:

    - Low stock items
    - Out of stock items
    - Reorder requirements

    Provide a concise summary.
    """,
    expected_output="Summary of inventory findings",
    agent=inventory_agent
)