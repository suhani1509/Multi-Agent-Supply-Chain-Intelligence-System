from crewai import Agent
# from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from crewai import LLM

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

manager_agent = Agent(
    role="Supply Chain Manager",
    goal="Make final supply chain decisions and recommendations",
    backstory="""
    You are a senior supply chain manager.
    You review email findings and inventory findings,
    identify risks, prioritize issues, and provide
    actionable business recommendations.
    """,
    llm=llm,
    verbose=False
)