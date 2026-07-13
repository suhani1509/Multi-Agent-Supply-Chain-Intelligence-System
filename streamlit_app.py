import streamlit as st

from crew_setup import supply_chain_crew
from reports.report_generator import generate_pdf


st.set_page_config(

    page_title="Supply Chain Intelligence System",

    page_icon="📦",

    layout="wide"

)

st.title("📦 Multi-Agent Supply Chain Intelligence System")

st.markdown(
    """
Analyze supplier emails and inventory using CrewAI agents.

This system:

- Reads supplier emails
- Checks inventory
- Detects risks
- Generates recommendations
- Creates a PDF report
"""
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(

        label="📧 Email Agent",

        value="Ready"

    )

with col2:

    st.metric(

        label="📦 Inventory Agent",

        value="Ready"

    )

with col3:

    st.metric(

        label="👨‍💼 Manager Agent",

        value="Ready"

    )

st.divider()

if st.button("🚀 Run Supply Chain Analysis", use_container_width=True):

    with st.spinner("Running CrewAI agents..."):

        result = supply_chain_crew.kickoff()

    st.success("Analysis completed successfully!")

    email_report = result.tasks_output[0].raw

    inventory_report = result.tasks_output[1].raw

    manager_report = result.tasks_output[2].raw

    pdf_path = generate_pdf(

        email_report,

        inventory_report,

        manager_report

    )

    tab1, tab2, tab3 = st.tabs(

        [

            "📧 Email Analysis",

            "📦 Inventory Analysis",

            "👨‍💼 Manager Recommendations"

        ]

    )

    with tab1:

        st.markdown(email_report)

    with tab2:

        st.markdown(inventory_report)

    with tab3:

        st.markdown(manager_report)

    st.divider()

    st.subheader("📄 Download Report")

    with open(pdf_path, "rb") as file:

        st.download_button(

            label="⬇ Download PDF Report",

            data=file,

            file_name="supply_chain_report.pdf",

            mime="application/pdf",

            use_container_width=True

        )