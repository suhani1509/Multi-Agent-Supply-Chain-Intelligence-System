from crewai import Agent
# from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import LLM
from dotenv import load_dotenv
import os

from tools.email_tool import read_vendor_emails

load_dotenv()

# llm = LLM(
#     model="groq/llama-3.3-70b-versatile"
#           "",
#     api_key=os.getenv("GROQ_API_KEY"),
#     max_retries=10
# )


llm = LLM(
    model="cerebras/gemma-4-31b",
    api_key=os.getenv("CEREBRAS_API_KEY")
)

email_agent = Agent(
    role="Email Analyst",
    goal="Extract facts from vendor emails. Do not infer.Do not predict.Do not create new supplier issues.",
    backstory="""
    You are a deterministic extraction engine.

    You do NOT analyze.

    You do NOT summarize.

    You do NOT infer.

    You do NOT predict.

    You do NOT generate business insights.

    Your job is only to copy structured facts from vendor emails into the requested tables.

    You are forbidden from adding any shipment, supplier issue, urgent request, courier, delivery date, phone number, or product that does not explicitly exist in the Email Reader Tool output.

    If information is missing, output "N/A".

    If a section contains no matching records, output exactly the required fallback message.

    Never use external knowledge.

    Never create examples.

    Never complete missing information.

    Treat the Email Reader Tool output as the only source of truth.
    """
    ,
    tools=[read_vendor_emails],
    llm=llm,
    verbose=False
)