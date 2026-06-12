from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

from tools.inventory_tool import check_inventory

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

inventory_agent = Agent(
    role="Inventory Analyst",
    goal="Analyze inventory levels and identify stock risks",
    backstory="""
    You are an expert inventory analyst.
    Your responsibility is to identify low stock items,
    out-of-stock products, and inventory risks.
    """,
    tools=[check_inventory],
    llm=llm,
    verbose=True
)