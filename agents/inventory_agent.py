from crewai import Agent, LLM
from dotenv import load_dotenv
import os
import streamlit as st

from tools.inventory_tool import check_inventory

load_dotenv()

# Get API key - works locally and on Streamlit Cloud
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found")

llm = LLM(
    model="groq/qwen/qwen3.6-27b",
    api_key=api_key
)

inventory_agent = Agent(
    role="Inventory Analyst",

    goal="""
    Extract factual inventory information from inventory records.
    Never invent information.
    Never estimate values.
    Never make predictions.
    """,

    backstory="""
    You are a data analyst.
    You only report facts present in the inventory data.
    You do not perform forecasting, business assumptions,
    market analysis, supplier analysis, or demand estimation.
    """,

    tools=[check_inventory],
    llm=llm,
    verbose=False
)