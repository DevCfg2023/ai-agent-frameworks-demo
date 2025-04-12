import os

import azure.identity
from dotenv import load_dotenv
from smolagents import AzureOpenAIServerModel, CodeAgent, DuckDuckGoSearchTool, OpenAIServerModel

# Configura el cliente para usar Azure OpenAI o GitHub Models
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")

if API_HOST == "github":
    model = OpenAIServerModel(
        model_id="gpt-4o", api_base="https://models.inference.ai.azure.com", api_key=os.environ["GITHUB_TOKEN"]
    )
elif API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    model = AzureOpenAIServerModel(
        model_id=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
        api_version=os.environ["AZURE_OPENAI_VERSION"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        client_kwargs={"azure_ad_token_provider": token_provider}
    )


agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model)

agent.run("¿Cuántos segundos le tomaría a un leopardo corriendo a máxima velocidad en atravesar el Pont des Arts?")