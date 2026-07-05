from crewai import Task
from agents.inventory_agent import inventory_agent

inventory_task = Task(
    description="""
    Read the inventory data returned by the Inventory Checker Tool.

STRICT RULES
- Use ONLY the tool output.
- Never invent parts.
- Never invent stock values.
- Never estimate reorder quantities.
- Never perform forecasting.
- Never mention products not present in the tool output.

Create an inventory report containing:

1. Total Parts

2. Low Stock Items
For every low stock item report:
- Part ID
- Part Name
- Vendor
- Current Stock
- Minimum Required
- Reorder Quantity

If no low stock items exist, return "None".

Return only factual information.
    """,
expected_output="""
Inventory Health Report

1. HIGH RISK INVENTORY
Display a table with:
- Product Name
- Vendor
- Minimum Required
- Current Stock
- Reorder Quantity

Only include products whose stock is below 60% of the minimum requirement.

-----------------------------------------------------

2. MEDIUM RISK INVENTORY
Display a table with:
- Product Name
- Vendor
- Minimum Required
- Current Stock
- Reorder Quantity

Only include products whose stock is between 60% and below 100% of the minimum requirement.

-----------------------------------------------------

Do not display low-risk products.

Do not invent any products.

Use only the inventory data returned by the tool.

Return the report in clean markdown tables.
""",

    agent=inventory_agent
)