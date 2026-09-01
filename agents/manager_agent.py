from crewai import Agent, LLM
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

# Get API key - works locally and on Streamlit Cloud
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found")

llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=api_key
)

manager_agent = Agent(
    role="Supply Chain Risk Manager",

    goal="""
    Compare inventory risks with shipment delays and identify
    business-critical supply chain issues.
    """,

    backstory="""
    You are a senior supply chain manager.

    Your responsibility is to compare:

    1. Inventory Agent output
    2. Email Agent output

    You must identify products that are:

    - Medium risk or High risk in inventory.
    - Delayed or partially shipped in vendor emails.

    You generate business decisions based ONLY on the provided data.

    Never hallucinate.
    Never assume missing values.
    Never create products or suppliers.
    """,

    llm=llm,

    verbose=True
)