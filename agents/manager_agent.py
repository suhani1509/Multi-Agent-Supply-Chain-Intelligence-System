from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

# llm = LLM(
#     model="groq/llama-3.3-70b-versatile",
#     api_key=os.getenv("GROQ_API_KEY"),
#     max_retries=10
# )

llm = LLM(
    model="cerebras/gemma-4-31b",
    api_key=os.getenv("CEREBRAS_API_KEY")
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