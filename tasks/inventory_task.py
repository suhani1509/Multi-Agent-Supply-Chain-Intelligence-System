from crewai import Task
from agents.inventory_agent import inventory_agent

inventory_task = Task(
    description="""
    Use the Inventory Checker Tool to retrieve the inventory data.

    Use ONLY the tool output.
    Do not invent or infer any values.

    Report:
    1. Total Parts
    2. High Risk Inventory
    3. Medium Risk Inventory

    For each item include:
    Product Name, Vendor, Minimum Required,
    Current Stock, Reorder Quantity.

    Return only a concise Markdown report.
    """,

    expected_output="""
    A concise Markdown inventory report based only on
    the Inventory Checker Tool output.
    """,

    agent=inventory_agent
)