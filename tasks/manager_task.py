from crewai import Task

from agents.manager_agent import manager_agent
from tasks.email_task import email_task
from tasks.inventory_task import inventory_task

manager_task = Task(
    description="""
    Review email findings and inventory findings.

    Identify critical risks and provide
    final supply chain recommendations.
    """,
    expected_output="Final supply chain action plan",
    agent=manager_agent,
    context=[email_task, inventory_task]
)