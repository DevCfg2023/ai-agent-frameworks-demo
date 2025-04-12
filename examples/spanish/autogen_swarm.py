import asyncio
import os

import azure.identity
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import HandoffTermination, TextMentionTermination
from autogen_agentchat.messages import HandoffMessage
from autogen_agentchat.teams import Swarm
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient, OpenAIChatCompletionClient
from dotenv import load_dotenv

# Configura el cliente para usar Azure OpenAI o GitHub Models
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")


if API_HOST == "github":
    client = OpenAIChatCompletionClient(model="gpt-4o", api_key=os.environ["GITHUB_TOKEN"], base_url="https://models.inference.ai.azure.com")
elif API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
    client = AzureOpenAIChatCompletionClient(
        model=os.environ["AZURE_OPENAI_CHAT_MODEL"],
        api_version=os.environ["AZURE_OPENAI_VERSION"],
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_ad_token_provider=token_provider,
    )

agente_viajes = AssistantAgent(
    "agente_viajes",
    model_client=client,
    handoffs=["reembolsador_vuelos", "usuario"],
    system_message="""Eres un agente de viajes.
    El reembolsador_vuelos está a cargo de reembolsar vuelos.
    Si necesitas información del usuario, primero debes enviar tu mensaje, luego puedes transferir al usuario.
    Usa TERMINATE cuando la planificación del viaje esté completa.""",
)


def reembolsar_vuelo(id_vuelo: str) -> str:
    """Reembolsar un vuelo"""
    return f"Vuelo {id_vuelo} reembolsado"


reembolsador_vuelos = AssistantAgent(
    "reembolsador_vuelos",
    model_client=client,
    handoffs=["agente_viajes", "usuario"],
    tools=[reembolsar_vuelo],
    system_message="""Eres un agente especializado en reembolsar vuelos.
    Solo necesitas los números de referencia de vuelo para reembolsar un vuelo.
    Tienes la capacidad de reembolsar un vuelo usando la herramienta reembolsar_vuelo.
    Si necesitas información del usuario, primero debes enviar tu mensaje, luego puedes transferir al usuario.
    Cuando la transacción esté completa, transfiere al agente de viajes para finalizar.""",
)


async def ejecutar_equipo_stream(tarea: str) -> None:
    terminacion = HandoffTermination(target="usuario") | TextMentionTermination("TERMINATE")
    equipo = Swarm([agente_viajes, reembolsador_vuelos], termination_condition=terminacion)

    resultado_tarea = await Console(equipo.run_stream(task=tarea))
    ultimo_mensaje = resultado_tarea.messages[-1]

    while isinstance(ultimo_mensaje, HandoffMessage) and ultimo_mensaje.target == "usuario":
        mensaje_usuario = input("Usuario: ")

        resultado_tarea = await Console(equipo.run_stream(task=HandoffMessage(source="usuario", target=ultimo_mensaje.source, content=mensaje_usuario)))
        ultimo_mensaje = resultado_tarea.messages[-1]


if __name__ == "__main__":
    asyncio.run(ejecutar_equipo_stream("Necesito reembolsar mi vuelo."))
