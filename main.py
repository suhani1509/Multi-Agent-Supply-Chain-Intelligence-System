from crew_setup import supply_chain_crew
from reports.report_generator import generate_pdf

result = supply_chain_crew.kickoff()

email_report = result.tasks_output[0].raw
inventory_report = result.tasks_output[1].raw
manager_report = result.tasks_output[2].raw

pdf_path = generate_pdf(
    email_report,
    inventory_report,
    manager_report
)

print("\nPDF Generated Successfully!")
print(pdf_path)