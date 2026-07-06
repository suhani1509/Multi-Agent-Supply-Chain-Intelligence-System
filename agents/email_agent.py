from crewai import Agent
# from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import LLM
from dotenv import load_dotenv
import os

from tools.email_tool import read_vendor_emails

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile"
          "",
    api_key=os.getenv("GROQ_API_KEY")
)

email_agent = Agent(
    role="Email Analyst",
    goal="Extract facts from vendor emails. Do not infer.Do not predict.Do not create new supplier issues.",
    backstory="""
    You are an expert supply chain email analyst.
    Your job is to read vendor communications and identify
    delays, shortages, urgent requests, and supply chain risks.
    """,
    tools=[read_vendor_emails],
    llm=llm,
    verbose=False
)