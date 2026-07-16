from cerebras.cloud.sdk import Cerebras

client = Cerebras(
    api_key="csk-x6trv8e88techrx9ktnvh4tr22fxn3jd2jtc5n3n3t4crnc4"
)

models = client.models.list()

print(models)