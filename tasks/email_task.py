from crewai import Task
from agents.email_agent import email_agent

email_task = Task(
description="""
Use the Email Reader Tool exactly once to retrieve vendor emails.

The tool is the ONLY source of truth.

The emails may contain:

- Plain text
- Shipment tables
- Purchase order updates
- Courier information
- Tracking IDs
- Delivery dates
- Supplier issues
- Urgent requests

Your task is to EXTRACT information, not analyze or predict.

WORKFLOW

1. Read every email returned by the Email Reader Tool.

2. Process emails ONE BY ONE.

3. Never skip any email.

4. If an email contains a shipment table, process EVERY row separately.

5. Every row represents one shipment record.

6. Do NOT merge shipment rows.

7. If the same product appears:
   - in different emails,
   - from different vendors,
   - or multiple times,
   treat every occurrence as a separate shipment.

8. Preserve all values exactly as written.

9. If a field is missing, write "N/A".

10. Ignore promotional, advertisement and newsletter emails.

STRICTLY FORBIDDEN

- Do NOT hallucinate.
- Do NOT summarize before reading all emails.
- Do NOT invent suppliers.
- Do NOT invent shipment status.
- Do NOT invent courier names.
- Do NOT invent delivery dates.
- Do NOT invent tracking IDs.
- Do NOT invent quantities.
- Do NOT invent phone numbers.
- Do NOT invent supplier issues.
- Do NOT invent urgent requests.
- Do NOT classify products into delayed, in transit or delivered unless the email explicitly states that status.
- Do NOT infer information from previous emails.
- Do NOT combine multiple emails together.

QUALITY CHECK

Before producing the final report verify:

✓ Every email has been processed.
✓ Every shipment table has been processed.
✓ Every shipment row has been extracted.
✓ Every occurrence of the same product has been kept separately.
✓ Every value comes directly from the emails.

If any email has not been processed, continue reading before generating the report.

Your final answer must contain ONLY facts explicitly present in the emails returned by the Email Reader Tool.
CRITICAL INSTRUCTIONS

The Email Reader Tool is the ONLY source of truth.

Generate the report ONLY using the exact text returned by the Email Reader Tool.

If a shipment, vendor, product, courier, issue or request is not explicitly present in the tool output, DO NOT include it.

Never use prior knowledge.

Never create examples.

Never complete missing tables.

Never infer additional emails.

Never invent vendors.

Never invent products.

The final report must be a strict transformation of the Email Reader Tool output.

If the Email Reader Tool returns only one email, the final report must contain information from only that email.

Do not imagine additional emails.
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