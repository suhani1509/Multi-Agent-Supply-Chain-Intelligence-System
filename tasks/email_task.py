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

Analyze ONLY the emails returned by the Email Reader Tool.

If an email contains shipment tables, extract EVERY row independently.

Do NOT merge rows.

If the same product appears in multiple emails or from different vendors, include each occurrence as a separate row.

Return a clean, professional report using Markdown.

=========================================================
🚚 DELAYED SHIPMENTS
=========================================================

Include ONLY products where:

- Status = Delayed
- Status = Partially Shipped
- Delay explicitly mentioned

| Product | Vendor | Qty Ordered | Qty Shipped | Delay Reason | Expected Delivery | Courier | Tracking ID | Contact |
|---------|--------|------------:|------------:|-------------|------------------|---------|-------------|---------|
| ... |

If none:

No delayed shipments found.

---------------------------------------------------------

🚛 OUT FOR DELIVERY

Include ONLY products whose status is:

- Out for Delivery
- Out for Delivery Today

| Product | Vendor | Quantity | Delivery Date | Courier | Tracking ID | Contact |
|---------|--------|---------:|---------------|---------|-------------|---------|
| ... |

If none:

No products are currently out for delivery.

---------------------------------------------------------

📦 IN TRANSIT

Include ONLY products currently in transit in mail . dont hallucinate

| Product | Vendor | Quantity | Expected Delivery | Courier | Tracking ID | Contact |
|---------|--------|---------:|------------------|---------|-------------|---------|
| ... |

If none:

No products currently in transit.

---------------------------------------------------------

✅ DELIVERED

Include ONLY delivered products in mail . dont hallucinate

| Product | Vendor | Quantity | Delivered On | Courier | Tracking ID |
|---------|--------|---------:|--------------|---------|-------------|
| ... |

If none:

No delivered shipments.

---------------------------------------------------------

🚨 URGENT REQUESTS

Only include requests explicitly marked as:

- URGENT
- Immediate Action Required
- Immediate Delivery Required
- Critical Material Requirement
- Urgent Quotation

Do NOT classify shipment delays as urgent requests.

Format:
dont hallucinate. just consider data in mails

| Vendor | Request | Action Required |
|--------|---------|-----------------|
| ... |

If none:

None.

---------------------------------------------------------

⚠ SUPPLIER ISSUES

Include ONLY issues explicitly mentioned.

Possible examples:

- Machine Breakdown
- Raw Material Shortage
- Labour Strike
- Customs Delay
- Weather Disruption
- Logistics Delay

Format:

| Vendor | Issue | Impact |
|--------|-------|--------|
| ... |

If none:

None.

=========================================================

STRICT RULES

- Use ONLY Email Reader Tool data.
- Never hallucinate.
- Never estimate values.
- Never infer missing information.
- Never create suppliers.
- Never create products.
- Never combine shipment rows.
- Every shipment row must remain an individual row.
- Preserve courier names exactly.
- Preserve tracking IDs exactly.
- Preserve phone numbers exactly.
- Preserve delivery dates exactly.
- If any value is missing, write "N/A".
- Return ONLY the formatted report.
""",

    agent=email_agent
)