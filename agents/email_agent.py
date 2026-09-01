from crewai import Agent
# from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import LLM
from dotenv import load_dotenv
import os

from tools.email_tool import read_vendor_emails

load_dotenv()

# llm = LLM(
#     model="groq/openai/gpt-oss-120b",
#     api_key=os.getenv("GROQ_API_KEY"),
#     max_tokens=15000
# )

llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),

)

# llm = LLM(
#     model="cerebras/gemma-4-31b",
#     api_key=os.getenv("CEREBRAS_API_KEY")
# )

# llm = LLM(
#     model="cerebras/gpt-oss-120b",
#     api_key=os.getenv("CEREBRAS_API_KEY")
# )

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