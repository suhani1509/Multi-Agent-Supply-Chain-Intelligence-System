from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

report_agent = Agent(
    role="Supply Chain Report Generator",

    goal="""
    Generate a professional executive supply chain report using the
    outputs from the Email Analyst, Inventory Analyst and Supply Chain Manager.

    Never invent information.
    Never modify facts.
    Present the information in a clean business report.
    """,

    backstory="""
    You are a Senior Supply Chain Reporting Specialist.

    Your responsibility is to transform operational analysis into a
    professional management report.

    You never perform analysis yourself.

    You only summarize and organize the information received from previous agents
    into an executive report suitable for managers.

    Your reports are concise, structured and visually clean.
    """,

    llm=llm,

    verbose=True
)