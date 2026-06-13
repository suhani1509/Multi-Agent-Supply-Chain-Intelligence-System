from crewai import Task
from agents.inventory_agent import inventory_agent

inventory_task = Task(
    description="""
    Read the inventory data returned by the tool.

    IMPORTANT:
    - Use ONLY the data returned by the tool.
    - Do NOT create new products.
    - Do NOT create out-of-stock items.
    - Do NOT assume stock values.
    - Do NOT assume future risks.
    - If a product is not listed in LOW STOCK ITEMS, do not mention it.
    - Report only the products shown by the tool.

    Provide:
    1. Total Parts
    2. Low Stock Items
    3. Reorder Quantity
    """,
    expected_output="Factual inventory summary using only tool data.",
    agent=inventory_agent
)