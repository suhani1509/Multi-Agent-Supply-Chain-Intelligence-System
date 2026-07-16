import os

from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter

from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

styles = getSampleStyleSheet()

cell_style = ParagraphStyle(
    "CellStyle",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=8,
    leading=10,
    wordWrap="LTR"
)


def markdown_table_to_reportlab(lines):

    data = []

    for line in lines:

        line = line.strip()

        if not line.startswith("|"):
            continue

        if "---" in line:
            continue

        cells = line.split("|")[1:-1]

        row = []

        for cell in cells:

            row.append(
                Paragraph(
                    cell.strip().replace("\n", "<br/>"),
                    cell_style
                )
            )

        data.append(row)

    if not data:
        return None

    num_cols = len(data[0])

    # Available width on landscape letter page
    available_width = 10.8 * inch

    if num_cols == 9:

        weights = [

            1.2,   # Part Name
            1.8,   # Vendor
            0.8,   # Qty Ordered
            0.8,   # Qty Shipped
            2.8,   # Delay Reason
            1.4,   # Expected Delivery
            1.3,   # Courier
            1.4,   # Tracking ID
            1.2    # Contact

        ]

    elif num_cols == 7:

        weights = [

            1.5,
            1.8,
            0.9,
            1.4,
            1.2,
            1.2,
            1.5

        ]

    elif num_cols == 6:

        weights = [

            1.5,
            1.8,
            1.0,
            1.5,
            1.3,
            1.5

        ]

    elif num_cols == 3:

        weights = [

            2,
            3,
            2

        ]

    else:

        weights = [1] * num_cols

    total_weight = sum(weights)

    col_widths = [

        available_width * w / total_weight

        for w in weights

    ]

    table = Table(

        data,

        colWidths=col_widths,

        repeatRows=1,

        splitByRow=True

    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("FONTSIZE", (0, 0), (-1, -1), 8),

            ("LEADING", (0, 0), (-1, -1), 10),

            ("VALIGN", (0, 0), (-1, -1), "TOP"),

            ("LEFTPADDING", (0, 0), (-1, -1), 5),

            ("RIGHTPADDING", (0, 0), (-1, -1), 5),

            ("TOPPADDING", (0, 0), (-1, -1), 6),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),

            ("WORDWRAP", (0, 0), (-1, -1), "LTR")

        ])

    )

    return table


def add_section(title, report_text, story):

    story.append(

        Paragraph(

            f"<font size='16'><b>{title}</b></font>",

            styles["Heading1"]

        )

    )

    story.append(Spacer(1, 12))

    lines = report_text.split("\n")

    table_lines = []

    inside_table = False

    for line in lines:

        stripped = line.strip()

        if stripped.startswith("|"):

            table_lines.append(stripped)

            inside_table = True

            continue

        if inside_table:

            table = markdown_table_to_reportlab(table_lines)

            if table:

                story.append(table)

                story.append(Spacer(1, 15))

            table_lines = []

            inside_table = False

        if stripped:

            story.append(

                Paragraph(

                    stripped,

                    styles["BodyText"]

                )

            )

            story.append(

                Spacer(1, 5)

            )

    if table_lines:

        table = markdown_table_to_reportlab(table_lines)

        if table:

            story.append(table)

            story.append(Spacer(1, 15))


def generate_pdf(

    email_report,
    inventory_report,
    manager_report

):

    os.makedirs(

        "generated_reports",

        exist_ok=True

    )

    timestamp = datetime.now().strftime(

        "%Y%m%d_%H%M%S"

    )

    pdf_path = (

        f"generated_reports/"
        f"supply_chain_report_{timestamp}.pdf"

    )

    doc = SimpleDocTemplate(

        pdf_path,

        pagesize=landscape(letter),

        leftMargin=20,

        rightMargin=20,

        topMargin=20,

        bottomMargin=20

    )

    story = []

    story.append(

        Paragraph(

            "<font size='22'><b>Supply Chain Intelligence Report</b></font>",

            styles["Title"]

        )

    )

    story.append(

        Spacer(1, 20)

    )

    story.append(

        Paragraph(

            f"<b>Generated:</b> "
            f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",

            styles["Normal"]

        )

    )

    story.append(

        Spacer(1, 25)

    )

    add_section(

        "Email Analysis",

        email_report,

        story

    )

    add_section(

        "Inventory Analysis",

        inventory_report,

        story

    )

    add_section(

        "Manager Recommendations",

        manager_report,

        story

    )

    doc.build(story)

    return pdf_path