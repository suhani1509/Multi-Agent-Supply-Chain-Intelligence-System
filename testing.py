# from cerebras.cloud.sdk import Cerebras
#
# client = Cerebras(
#     api_key="csk-x6trv8e88techrx9ktnvh4tr22fxn3jd2jtc5n3n3t4crnc4"
# )
#
# models = client.models.list()
#
# print(models)


from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("GROQ_API_KEY")

print("Key exists:", key is not None)
print("Key starts with gsk:", key.startswith("gsk-") if key else False)
print("Key length:", len(key) if key else 0)