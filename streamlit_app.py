from crew_setup import supply_chain_crew
from reports.report_generator import generate_pdf

import streamlit as st
import bcrypt

from database import supabase, upload_report


# ----------------------------------------------------------------------
# Auth helper
# ----------------------------------------------------------------------
def authenticate(email, password):
    response = (
        supabase
        .table("users")
        .select("*")
        .eq("email", email)
        .execute()
    )

    if len(response.data) == 0:
        return False

    user = response.data[0]
    stored_hash = user["password_hash"]

    return bcrypt.checkpw(
        password.encode(),
        stored_hash.encode()
    )


# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Micro Turners | Supply Chain Intelligence",
    page_icon="⬢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# Design tokens & global styling
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

        :root {
            --ink: #0B2545;
            --ink-soft: #1E3A5F;
            --bg: #F1F5F9;
            --surface: #FFFFFF;
            --border: #E2E8F0;
            --amber: #F59E0B;
            --amber-dark: #B45309;
            --teal: #0D9488;
            --red: #DC2626;
            --text: #101828;
            --text-soft: #64748B;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .main { background-color: var(--bg); }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] { background: transparent; }

        h1, h2, h3 {
            font-family: 'Space Grotesk', sans-serif !important;
            color: var(--ink) !important;
            letter-spacing: -0.01em;
        }

        /* ---------- Force readable text everywhere on the main page ---------- */
        /* Streamlit ships its own theme CSS (often white/grey text) that can win
           the cascade against narrower selectors. A blanket ".main *" rule beats
           that because it matches every descendant, and everything below it in
           the stylesheet (buttons, badges, sidebar) explicitly re-colors itself
           where a different color is actually wanted. This block MUST stay
           above those component-specific rules so the later, more specific
           intent wins. */
        .main, .main * {
            color: var(--text) !important;
        }

        /* Muted/secondary text */
        .main .hero-sub,
        .main .stCaption,
        .main small,
        .main [data-testid="stCaptionContainer"] * {
            color: var(--text-soft) !important;
        }

        /* Headings stay on-brand ink, not the flat body text color */
        .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
            color: var(--ink) !important;
        }

        /* Alerts (st.success / st.error / st.warning / st.info) keep readable
           dark text instead of inheriting light theme defaults */
        .main [data-testid="stAlert"],
        .main [data-testid="stAlert"] * {
            color: var(--text) !important;
        }

        /* Code / monospace blocks inside markdown reports */
        .main code, .main pre, .main pre * {
            color: var(--ink) !important;
            background-color: #F8FAFC !important;
        }

        /* Text typed into inputs must stay dark on their white fields */
        input, textarea {
            color: var(--text) !important;
            -webkit-text-fill-color: var(--text) !important;
            background-color: #FFFFFF !important;
        }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, var(--ink) 0%, var(--ink-soft) 100%);
        }
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] li,
        section[data-testid="stSidebar"] * {
            color: #E2E8F0 !important;
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 { color: #FFFFFF !important; }

        section[data-testid="stSidebar"] div.stButton > button {
            background: rgba(255,255,255,0.08) !important;
            border: 1px solid rgba(255,255,255,0.25) !important;
            color: #F1F5F9 !important;
        }
        section[data-testid="stSidebar"] div.stButton > button:hover {
            background: rgba(255,255,255,0.16) !important;
            color: #FFFFFF !important;
        }

        .brand-mark {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 1.35rem;
            color: #FFFFFF !important;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 0 0.2rem 0;
        }
        .brand-sub {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.7rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: #94A3B8 !important;
            padding-bottom: 1.2rem;
            border-bottom: 1px solid rgba(255,255,255,0.12);
            margin-bottom: 1.2rem;
        }
        .sidebar-user-card {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 10px;
            padding: 0.85rem 1rem;
            margin-bottom: 1rem;
        }
        .sidebar-user-label {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.65rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: #94A3B8 !important;
            margin-bottom: 0.2rem;
        }
        .sidebar-nav-item {
            display: flex; align-items: center; gap: 0.55rem;
            font-size: 0.88rem; font-weight: 500;
            padding: 0.55rem 0.7rem; border-radius: 8px;
            margin-bottom: 0.25rem;
        }
        .sidebar-nav-item.active {
            background: rgba(245, 158, 11, 0.16);
            border: 1px solid rgba(245, 158, 11, 0.35);
            color: #FCD34D !important;
        }

        /* ---------- Hero ---------- */
        .eyebrow {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.72rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--amber-dark) !important;
            font-weight: 600;
            margin-bottom: 0.4rem;
        }
        .hero-title {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 2.1rem;
            color: var(--ink) !important;
            margin: 0 0 0.35rem 0;
            line-height: 1.15;
        }
        .hero-sub {
            color: var(--text-soft) !important;
            font-size: 1rem;
            max-width: 640px;
            margin-bottom: 0;
        }

        /* ---------- Pipeline ---------- */
        .pipeline-wrap {
            display: flex;
            align-items: stretch;
            gap: 0;
            margin: 1.6rem 0 1.8rem 0;
        }
        .pipeline-node {
            flex: 1;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.1rem 1.2rem;
            position: relative;
            box-shadow: 0 1px 2px rgba(16,24,40,0.03);
        }
        .pipeline-connector {
            width: 34px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #CBD5E1 !important;
            font-size: 1.1rem;
        }
        .pipeline-index {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.7rem;
            color: var(--amber-dark) !important;
            font-weight: 600;
            letter-spacing: 0.08em;
        }
        .pipeline-title {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
            font-size: 1.02rem;
            color: var(--ink) !important;
            margin: 0.15rem 0 0.3rem 0;
        }
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            color: var(--teal) !important;
            background: rgba(13, 148, 136, 0.1);
            border: 1px solid rgba(13, 148, 136, 0.25);
            padding: 0.2rem 0.55rem;
            border-radius: 999px;
        }
        .status-badge::before {
            content: "";
            width: 6px; height: 6px; border-radius: 50%;
            background: var(--teal);
        }

        /* ---------- Buttons ---------- */
        div.stButton > button {
            border-radius: 8px;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            transition: all 0.15s ease-in-out;
            border: 1px solid var(--border);
            color: var(--text) !important;
        }
        div.stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 10px rgba(16,24,40,0.08);
        }
        div.stButton > button[kind="primary"] {
            background: var(--amber) !important;
            border: 1px solid var(--amber-dark) !important;
            color: #1A1203 !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background: var(--amber-dark) !important;
            color: #FFFFFF !important;
        }

        /* ---------- Login ---------- */
        .login-banner {
            background: linear-gradient(120deg, var(--ink) 0%, var(--ink-soft) 100%);
            border-radius: 18px;
            padding: 3rem 2rem 4.2rem 2rem;
            text-align: center;
            margin-top: 1rem;
        }
        .login-banner .brand-mark {
            justify-content: center;
            font-size: 1.8rem;
        }
        .login-banner p {
            color: #CBD5E1 !important;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.78rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-top: 0.4rem;
        }
        .login-card {
            max-width: 420px;
            margin: -3.2rem auto 0 auto;
            padding: 2rem 2rem 1.6rem 2rem;
            background: var(--surface);
            border-radius: 16px;
            box-shadow: 0 12px 32px rgba(11,37,69,0.14);
            border: 1px solid var(--border);
            position: relative;
        }
        .login-card h3 {
            font-family: 'Space Grotesk', sans-serif;
            margin-bottom: 0.2rem;
        }
        .login-card .caption {
            color: var(--text-soft) !important;
            font-size: 0.85rem;
            margin-bottom: 1.2rem;
        }

        /* ---------- Report cards ---------- */
        button[data-baseweb="tab"] {
            font-weight: 600;
            font-size: 0.92rem;
            font-family: 'Inter', sans-serif;
        }
        .report-box {
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem 1.7rem;
            border-top: 3px solid var(--amber);
        }
        .section-divider {
            border: none;
            border-top: 1px solid var(--border);
            margin: 1.6rem 0;
        }
        .deliverable-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-left: 4px solid var(--teal);
            border-radius: 10px;
            padding: 1rem 1.2rem;
        }
        .deliverable-card div[style*="color:var(--teal)"] {
            color: var(--teal) !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Session state defaults
# ----------------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None


# ----------------------------------------------------------------------
# Login screen
# ----------------------------------------------------------------------
if not st.session_state.logged_in:
    left, mid, right = st.columns([1, 1.3, 1])
    with mid:
        st.markdown(
            """
            <div class="login-banner">
                <div class="brand-mark">⬢ MICRO TURNERS</div>
                <p>Supply Chain Intelligence Platform</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.markdown("### Sign in")
        st.markdown("<div class='caption'>Access your supply chain workspace</div>", unsafe_allow_html=True)

        email = st.text_input("Email", placeholder="you@company.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")

        login_clicked = st.button("Sign in", use_container_width=True, type="primary")

        if login_clicked:
            if not email or not password:
                st.warning("Please enter both email and password.")
            else:
                with st.spinner("Verifying credentials..."):
                    user = authenticate(email, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# ----------------------------------------------------------------------
# Sidebar: brand, user, nav
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand-mark">⬢ MICRO TURNERS</div>
        <div class="brand-sub">Supply Chain Intelligence</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="sidebar-user-card">
            <div class="sidebar-user-label">Signed in as</div>
            <div style="font-weight:600; font-size:0.92rem;">{st.session_state.user_email}</div>
        </div>
        <div class="sidebar-nav-item active">📊&nbsp; Analysis Workspace</div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.rerun()

    st.markdown("<div style='height:1px; background:rgba(255,255,255,0.12); margin:1.4rem 0;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:#94A3B8; letter-spacing:0.06em;">
        AGENT PIPELINE<br>Email → Inventory → Manager
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------
# Hero
# ----------------------------------------------------------------------
st.markdown("<div class='eyebrow'>Multi-Agent Analysis Platform</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-title'>Supply Chain Intelligence Dashboard</div>", unsafe_allow_html=True)
st.markdown(
    "<p class='hero-sub'>Run a coordinated crew of AI agents that read supplier emails, "
    "check inventory levels, detect risk, and hand off a manager-ready recommendation report.</p>",
    unsafe_allow_html=True,
)

st.write("")

# ----------------------------------------------------------------------
# Agent pipeline (sequential — order reflects actual execution)
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="pipeline-wrap">
        <div class="pipeline-node">
            <div class="pipeline-index">01 · EMAIL AGENT</div>
            <div class="pipeline-title">📧 Supplier Correspondence</div>
            <span class="status-badge">READY</span>
        </div>
        <div class="pipeline-connector">→</div>
        <div class="pipeline-node">
            <div class="pipeline-index">02 · INVENTORY AGENT</div>
            <div class="pipeline-title">📦 Stock &amp; Demand</div>
            <span class="status-badge">READY</span>
        </div>
        <div class="pipeline-connector">→</div>
        <div class="pipeline-node">
            <div class="pipeline-index">03 · MANAGER AGENT</div>
            <div class="pipeline-title">👨‍💼 Recommendations</div>
            <span class="status-badge">READY</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("What does this system do?"):
    st.markdown(
        """
        - 📧 **Reads** supplier emails
        - 📦 **Checks** inventory levels
        - ⚠️ **Detects** potential supply chain risks
        - 💡 **Generates** actionable recommendations
        - 📄 **Creates** a downloadable PDF report
        """
    )

st.write("")

# ----------------------------------------------------------------------
# Run analysis
# ----------------------------------------------------------------------
run_clicked = st.button(
    "▶  Run Supply Chain Analysis",
    use_container_width=True,
    type="primary",
)

if run_clicked:
    progress = st.progress(0, text="Starting CrewAI agents...")

    with st.spinner("Running CrewAI agents... this may take a minute."):
        progress.progress(20, text="Agents analyzing data...")
        result = supply_chain_crew.kickoff()
        progress.progress(80, text="Compiling results...")

    progress.progress(100, text="Done!")
    st.success("Analysis completed successfully.")

    email_report = result.tasks_output[0].raw
    inventory_report = result.tasks_output[1].raw
    manager_report = result.tasks_output[2].raw

    with st.spinner("Generating PDF report..."):
        pdf_path = generate_pdf(
            email_report,
            inventory_report,
            manager_report,
        )

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>Results</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(
        [
            "📧  Email Analysis",
            "📦  Inventory Analysis",
            "👨‍💼  Manager Recommendations",
        ]
    )

    with tab1:
        st.markdown("<div class='report-box'>", unsafe_allow_html=True)
        st.markdown(email_report)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='report-box'>", unsafe_allow_html=True)
        st.markdown(inventory_report)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("<div class='report-box'>", unsafe_allow_html=True)
        st.markdown(manager_report)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.spinner("Uploading report..."):
        report_url = upload_report(pdf_path, st.session_state.user_email)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>Deliverable</div>", unsafe_allow_html=True)

    dl_col, link_col = st.columns([1, 2])

    with dl_col:
        with open(pdf_path, "rb") as file:
            st.download_button(
                label="⬇  Download PDF Report",
                data=file,
                file_name="supply_chain_report.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary",
            )

    with link_col:
        st.markdown(
            f"""
            <div class="deliverable-card">
                <div style="font-weight:600; color:var(--teal); margin-bottom:0.2rem;">✓ PDF uploaded successfully</div>
                <div style="font-family:'IBM Plex Mono',monospace; font-size:0.8rem; color:var(--text-soft); word-break:break-all;">{report_url}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )