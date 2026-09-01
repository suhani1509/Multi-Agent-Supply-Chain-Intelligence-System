from crewai import Agent, LLM
from dotenv import load_dotenv
import os
import streamlit as st

from tools.email_tool import read_vendor_emails

load_dotenv()

# Get API key
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

email_agent = Agent(
    role="Email Analyst",
    goal="Extract factual supply-chain information from vendor emails.",
    backstory="""
    You are a strict email extraction agent.
    Use the Email Reader Tool as the only source of information.
    Never invent, infer, predict, or estimate information.
    """,
    tools=[read_vendor_emails],
    llm=llm,
    allow_delegation=False,
    verbose=True
)