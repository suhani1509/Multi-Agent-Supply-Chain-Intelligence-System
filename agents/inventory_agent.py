from crewai import Agent
# from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import LLM
from dotenv import load_dotenv
import os

from tools.inventory_tool import check_inventory

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    max_retries=10
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