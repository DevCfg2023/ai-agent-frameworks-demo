import asyncio
import os

import azure.identity
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient, OpenAIChatCompletionClient
from dotenv import load_dotenv

# Configura el cliente para usar Azure OpenAI o GitHub Models
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")


if API_HOST == "github":
    client = OpenAIChatCompletionClient(
        model="gpt-4o", api_key=os.environ["GITHUB_TOKEN"], base_url="https://models.inference.ai.azure.com"
    )
elif API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(
        ), "https://cognitiveservices.azure.com/.default"
    )
    client = AzureOpenAIChatCompletionClient(
        model=os.environ["AZURE_OPENAI_CHAT_MODEL"],
        api_version=os.environ["AZURE_OPENAI_VERSION"],
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_ad_token_provider=token_provider,
    )

agente_planificador = AssistantAgent(
    "agente_planificador",
    model_client=client,
    description="Un asistente útil que puede planificar viajes.",
    system_message="Eres un asistente útil que puede sugerir un plan de viaje para un usuario según su solicitud.",
)

agente_local = AssistantAgent(
    "agente_local",
    model_client=client,
    description="Un asistente local que puede sugerir actividades o lugares para visitar.",
    system_message="Eres un asistente útil que puede sugerir actividades o lugares auténticos e interesantes para que un usuario visite y puedes utilizar cualquier información contextual proporcionada.",
)

agente_idioma = AssistantAgent(
    "agente_idioma",
    model_client=client,
    description="Un asistente útil que puede proporcionar consejos de idioma para un destino específico.",
    system_message="Eres un asistente útil que puede revisar planes de viaje, proporcionando comentarios sobre consejos importantes/críticos sobre cómo abordar mejor los desafíos de idioma o comunicación para el destino dado. Si el plan ya incluye consejos de idioma, puedes mencionar que el plan es satisfactorio, con fundamento.",
)

agente_resumen_viaje = AssistantAgent(
    "agente_resumen_viaje",
    model_client=client,
    description="Un asistente útil que puede resumir el plan de viaje.",
    system_message="Eres un asistente útil que puede tomar todas las sugerencias y consejos de los otros agentes y proporcionar un plan de viaje final detallado. Debes asegurarte de que el plan final esté integrado y completo. TU RESPUESTA FINAL DEBE SER EL PLAN COMPLETO. Cuando el plan esté completo y todas las perspectivas estén integradas, puedes responder con TERMINATE.",
)

async def ejecutar_agentes():
    terminacion = TextMentionTermination("TERMINATE")
    chat_grupal = MagenticOneGroupChat(
        [agente_planificador, agente_local, agente_idioma, agente_resumen_viaje],
        termination_condition=terminacion,
        model_client=client,
    )
    await Console(chat_grupal.run_stream(task="Planifica un viaje de 3 dias a Egipto"))


if __name__ == "__main__":
    asyncio.run(ejecutar_agentes())
