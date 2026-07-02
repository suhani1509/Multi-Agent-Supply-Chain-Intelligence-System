from crewai import Task
from agents.email_agent import email_agent

email_task = Task(
description="""
Use the Email Reader Tool to read all vendor emails.

The emails may contain:

- Plain text
- Tables
- Shipment status reports
- Purchase order updates
- Courier details
- Tracking information

Read EVERY email completely, including all rows of any tables.

IMPORTANT RULES

- Use ONLY the information present in the emails.
- Never invent suppliers, products, shipment details, delays, courier names, dates, tracking IDs, phone numbers or requests.
- Ignore advertisements, newsletters and promotional emails.
- If a value is missing, return "N/A".
- If an email contains a shipment table, analyze every row separately.
- One email can contain multiple products.
- Treat every product as an individual shipment record.
- Do not merge different products together.
- Report facts exactly as written.
""",

expected_output="""
You are an expert Supply Chain Email Analyst.

Read all vendor emails carefully.

If an email contains a shipment table, extract information from every row.

Return a clean, professional report using Markdown tables.

# DELAYED SHIPMENTS

| Product | Quantity Ordered | Quantity Shipped | Delay Reason | Expected Delivery | Courier | Tracking ID | Vendor Contact |
|----------|-----------------|-----------------|--------------|------------------|----------|-------------|----------------|
| ... |

Only include products whose shipment is delayed or partially delayed.

If none exist, write:

No delayed shipments found.

------------------------------------------------------

# OUT FOR DELIVERY

| Product | Quantity | Delivery Date | Courier | Tracking ID | Vendor Contact |
|----------|----------|---------------|----------|-------------|----------------|
| ... |

Include only products whose shipment status is:

- Out for Delivery
- Out for Delivery Today

If none exist, write:

No products are currently out for delivery.

------------------------------------------------------

# IN TRANSIT

| Product | Quantity | Expected Delivery | Courier | Tracking ID | Vendor Contact |
|----------|----------|------------------|----------|-------------|----------------|
| ... |

Include only products currently in transit.

------------------------------------------------------

# DELIVERED

| Product | Quantity | Delivered On | Courier | Tracking ID |
|----------|----------|--------------|----------|-------------|
| ... |

------------------------------------------------------

# URGENT REQUESTS

Include ONLY requests explicitly marked as:

- URGENT
- Immediate Action Required
- Immediate Delivery Required
- Urgent Quotation
- Critical Material Requirement

Do NOT classify shipment delays as urgent requests.

If none exist, write:

None.

------------------------------------------------------

# SUPPLIER ISSUES

Extract only issues explicitly mentioned by the supplier.

Examples:

- Raw material shortage
- Machine breakdown
- Labour strike
- Customs delay
- Weather disruption
- Logistics delay

If none exist, write:

None.

------------------------------------------------------

GENERAL RULES

- Never hallucinate.
- Never infer missing information.
- Never create products that do not exist.
- Never combine multiple rows into one.
- Every row in a shipment table represents one shipment item.
- If a value is unavailable, write "N/A".
- Preserve courier names, tracking IDs, phone numbers and delivery dates exactly as written.
- The report must contain information ONLY from the emails returned by the Email Reader Tool.
""",

    agent=email_agent
)