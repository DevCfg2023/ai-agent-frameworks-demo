import asyncio
import os

import azure.identity
import openai
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled
from dotenv import load_dotenv

# Disable tracing since we're not using OpenAI.com models
set_tracing_disabled(disabled=True)

# Configura el cliente para usar Azure OpenAI o GitHub Models
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")

if API_HOST == "github":
    client = openai.AsyncOpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.environ["GITHUB_TOKEN"])
    MODEL_NAME = "gpt-4o"
elif API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
    client = openai.AsyncAzureOpenAI(
        api_version=os.environ["AZURE_OPENAI_VERSION"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_ad_token_provider=token_provider,
    )
    MODEL_NAME = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]


@function_tool
def obtener_clima(ciudad: str) -> str:
    return {
        "ciudad": ciudad,
        "temperatura": 72,
        "descripcion": "Soleado",
    }


agente_clima = Agent(
    name="Agente del Clima",
    instructions="Solo puedes proporcionar información del clima.",
    tools=[obtener_clima],
)

agente_espanol = Agent(
    name="Agente Español",
    instructions="Solo hablas español.",
    tools=[obtener_clima],
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)

agente_ingles = Agent(
    name="Agente Inglés",
    instructions="Solo hablas inglés",
    tools=[obtener_clima],
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)

agente_triaje = Agent(
    name="Agente de Triaje",
    instructions="Transfiere al agente apropiado según el idioma de la solicitud.",
    handoffs=[agente_espanol, agente_ingles],
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)


async def main():
    result = await Runner.run(agente_triaje, input="Hola, ¿cómo estás? ¿Puedes darme el clima para San Francisco CA?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
