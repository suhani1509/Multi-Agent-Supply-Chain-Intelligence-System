from crewai import Task
from agents.email_agent import email_agent

email_task = Task(
    description="""
    Use the Email Reader Tool to retrieve the vendor emails.

    The tool output is the ONLY source of truth.

    Process every email and every shipment row separately.

    Extract ONLY information explicitly present in the emails.
    Never invent, infer, predict, estimate, merge, or assume information.
    If a value is missing, use N/A.
    Ignore promotional and newsletter emails.

    Classify shipments ONLY when the email explicitly states the status:
    - Delayed / Partially Shipped
    - Out for Delivery
    - In Transit
    - Delivered

    Include urgent requests and supplier issues ONLY when explicitly
    mentioned in the emails.

    Return the following Markdown report:

    DELAYED SHIPMENTS
    | Product | Vendor | Qty Ordered | Qty Shipped | Delay Reason | Expected Delivery | Courier | Tracking ID | Contact |

    OUT FOR DELIVERY
    | Product | Vendor | Quantity | Delivery Date | Courier | Tracking ID | Contact |

    IN TRANSIT
    | Product | Vendor | Quantity | Expected Delivery | Courier | Tracking ID | Contact |

    DELIVERED
    | Product | Vendor | Quantity | Delivered On | Courier | Tracking ID |

    URGENT REQUESTS
    | Vendor | Request | Action Required |

    SUPPLIER ISSUES
    | Vendor | Issue | Impact |

    If a section has no matching records, write N/A.

    Return ONLY the final report.
    """,

    expected_output="""
    A Markdown supply-chain report containing only facts explicitly
    present in the Email Reader Tool output. No hallucinated or inferred data.
    """,

    agent=email_agent
)