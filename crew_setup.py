# # crew_setup.py
# import os
# import warnings
# from dotenv import load_dotenv
#
# # 1. Load Environment Variables
# load_dotenv()
#
# # 2. Quiet down warnings
# warnings.filterwarnings("ignore", category=UserWarning)
# warnings.filterwarnings("ignore", category=DeprecationWarning)
# os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
#
# # 3. Direct Environment Overrides for Gemini API
# # Yeh variables direct backend hit karne mein help karenge bina LiteLLM wrapper ke
# os.environ["GEMINI_API_VERSION"] = "v1"
#
# api_key = os.getenv("GEMINI_API_KEY")
# if not api_key:
#     raise ValueError("Error: GEMINI_API_KEY .env file se load nahi ho paayi!")
#
# from crewai import Agent, Task, Crew
#
# print("--- Using Direct Native Gemini String Config ---")
#
# print("--- 1. Single Test Agent Ban Raha Hai ---")
# test_agent = Agent(
#     role="Test Analyst",
#     goal="Say hello and confirm connection",
#     backstory="You are a helper agent testing the API connection.",
#     # Direct string passing syntax jo binary built-in parser use karega
#     llm="gemini/gemini-1.5-flash",
#     verbose=True
# )
#
# test_task = Task(
#     description="Respond with exactly the phrase: 'API Connection Successful!'",
#     agent=test_agent,
#     expected_output="A confirmation string."
# )
#
# print("--- 2. Crew Object Ban Raha Hai ---")
# crew = Crew(
#     agents=[test_agent],
#     tasks=[test_task],
#     verbose=True
# )
#
# def run_analysis():
#     print("--- 3. run_analysis() Ke Andar Aa Gaye Hain ---")
#     result = crew.kickoff()
#     print("--- 4. crew.kickoff() Se Response Aa Gaya! ---")
#     return result