from crewai import Task

from agents.manager_agent import manager_agent
from tasks.email_task import email_task
from tasks.inventory_task import inventory_task


manager_task = Task(

    description="""
You are the Supply Chain Risk Manager.

You will receive:

1. Email Agent output.
2. Inventory Agent output.

Your job is to compare BOTH outputs.

IMPORTANT:

Create a table containing ONLY products that satisfy BOTH conditions:

Condition 1:

The product appears in:

- HIGH RISK inventory items

OR

- MEDIUM RISK inventory items.

Condition 2:

The same product appears in:

- Delayed shipments

OR

- Partially shipped shipments.

Do NOT include products that satisfy only one condition.

------------------------------------------------

Return this table:

| Product | Risk Level | Delay Reason | Expected Delivery | Supplier | Recommended Action |
|----------|-------------|-------------|-------------------|-----------|-------------------|

------------------------------------------------

Rules:

- Use ONLY Email Agent and Inventory Agent outputs.
- Never hallucinate.
- Never estimate inventory.
- Never estimate delays.
- Never create products.
- Never create suppliers.
- Never create delivery dates.
- Never create recommendations without evidence.

Supplier matching rules:

Example:

kumar@partsco.com = Kumar Parts Co

Use exact matching whenever possible.

------------------------------------------------

If no such products exist, return:

"No high-risk or medium-risk delayed products found."

------------------------------------------------

After the table, provide:

# FINAL RECOMMENDATIONS

Provide 3–5 short recommendations based ONLY on the identified products.
""",

    expected_output="""
A markdown table containing products that are both inventory risks and delayed shipments, followed by final recommendations.
""",

    agent=manager_agent,

    context=[
        email_task,
        inventory_task
    ]
)