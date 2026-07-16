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
# Inventory Health Report

## HIGH RISK INVENTORY

Products whose stock is below 60% of the minimum required stock.

Return ONLY a markdown table in the following format:

| Product Name | Vendor | Minimum Required | Current Stock | Reorder Quantity |
|--------------|---------|------------------|----------------|------------------|
| Example | Example | 100 | 20 | 80 |

Rules:

- Include only products whose stock is below 60% of the minimum requirement.
- Do not add explanations before or after the table.
- If there are no high-risk products, write:

No high-risk inventory found.

-----------------------------------------------------

## MEDIUM RISK INVENTORY

Products whose stock is between 60% and below 100% of the minimum required stock.

Return ONLY a markdown table in the following format:

| Product Name | Vendor | Minimum Required | Current Stock | Reorder Quantity |
|--------------|---------|------------------|----------------|------------------|
| Example | Example | 100 | 80 | 20 |

Rules:

- Include only products whose stock is between 60% and below 100% of the minimum requirement.
- Do not add explanations before or after the table.
- If there are no medium-risk products, write:

No medium-risk inventory found.

-----------------------------------------------------

Important:

- Do not invent any products.
- Use only the inventory data returned by the tool.
- Return valid markdown tables only.
- Keep all columns in the exact same order.
""",

    agent=inventory_agent
)