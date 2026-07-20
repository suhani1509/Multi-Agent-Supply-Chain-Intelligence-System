# 📦 Multi-Agent Supply Chain Intelligence System

An AI-powered supply chain intelligence platform built using CrewAI, Streamlit, and Supabase.

The system uses multiple AI agents to analyze supplier emails, monitor inventory levels, detect supply chain risks, and generate downloadable PDF reports.

🌐 Live Demo:

https://multi-agent-supply-chain-intelligence-system-hcjs3ybcsrjaq9j37.streamlit.app/
Login ID : supplychain.project.ai@gmail.com
Password : 12345

---

# 🚀 Features

✅ Multi-agent architecture using CrewAI

✅ Email analysis agent

✅ Inventory analysis agent

✅ Manager recommendation agent

✅ Secure user authentication

✅ Cloud database with Supabase

✅ PDF report generation

✅ Cloud storage for reports

✅ Gmail API integration

✅ Streamlit web interface

---

# 🏗️ System Architecture

The platform consists of three AI agents:

### 📧 Email Agent

- Reads supplier emails
- Detects delays and risks
- Extracts important updates

### 📦 Inventory Agent

- Monitors stock levels
- Identifies low inventory
- Calculates reorder requirements

### 👨‍💼 Manager Agent

- Combines outputs from all agents
- Generates recommendations
- Produces actionable insights

---

# 🛠️ Tech Stack

## Frontend

- Streamlit

## Backend

- Python
- CrewAI

## AI / LLM

- Groq
- Cerebras
- Gemini

## Database

- Supabase PostgreSQL

## Storage

- Supabase Storage

## APIs

- Gmail API

## Reporting

- ReportLab

---

# 📂 Project Structure

```text
project/

├── agents/
├── tasks/
├── tools/
├── reports/
├── data/
├── credentials/
├── crew_setup.py
├── database.py
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

# 🔐 Authentication

Users can log in using credentials stored securely in Supabase.

Features:

- Multiple user accounts
- Password hashing with bcrypt
- Session-based authentication

---

# 📄 Report Generation

The system automatically:

- Generates PDF reports
- Stores them locally
- Uploads them to Supabase Storage
- Saves report URLs in the database

---

# ⚙️ Installation

Clone the repository:

```bash
git clone <your-github-repository-link>
```

Move into the project:

```bash
cd Multi-Agent-Supply-Chain-Intelligence-System
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run streamlit_app.py
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=

CEREBRAS_API_KEY=

SUPABASE_URL=

SUPABASE_KEY=

GMAIL_USER=
```

---

# ☁️ Deployment

The project is deployed on Streamlit Community Cloud.

Deployment steps:

1. Push project to GitHub.
2. Create Streamlit app.
3. Add secrets.
4. Deploy.
5. Share the public URL.

---

# 👩‍💻 Author

Suhani Agghi

B.Tech CSE Student

---
