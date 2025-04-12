import os
from typing import Literal

import azure.identity
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI, AsyncOpenAI
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.usage import Usage, UsageLimits
from rich.prompt import Prompt

# Configura el cliente para usar Azure OpenAI o GitHub Models
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")

if API_HOST == "github":
    client = AsyncOpenAI(api_key=os.environ["GITHUB_TOKEN"], base_url="https://models.inference.ai.azure.com")
    model = OpenAIModel("gpt-4o", provider=OpenAIProvider(openai_client=client))
elif API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
    client = AsyncAzureOpenAI(
        api_version=os.environ["AZURE_OPENAI_VERSION"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_ad_token_provider=token_provider,
    )
    model = OpenAIModel(os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"], provider=OpenAIProvider(openai_client=client))


class FlightDetails(BaseModel):
    flight_number: str


class Failed(BaseModel):
    """No se pudo encontrar una opción satisfactoria."""


flight_search_agent = Agent(
    model,
    result_type=FlightDetails | Failed,
    system_prompt=('Usa la herramienta "flight_search" para encontrar un vuelo ' "desde el origen dado hasta el destino dado."),
)


@flight_search_agent.tool
async def flight_search(ctx: RunContext[None], origin: str, destination: str) -> FlightDetails | None:
    # en realidad, esto llamaría a una API de búsqueda de vuelos o
    # usaría un navegador para extraer datos de un sitio web de búsqueda de vuelos
    return FlightDetails(flight_number="AK456")


usage_limits = UsageLimits(request_limit=15)


async def find_flight(usage: Usage) -> FlightDetails | None:
    message_history: list[ModelMessage] | None = None
    for _ in range(3):
        prompt = Prompt.ask(
            "¿Desde dónde y hacia dónde te gustaría volar?",
        )
        result = await flight_search_agent.run(
            prompt,
            message_history=message_history,
            usage=usage,
            usage_limits=usage_limits,
        )
        if isinstance(result.data, FlightDetails):
            return result.data
        else:
            message_history = result.all_messages(result_tool_return_content="Por favor, intenta de nuevo.")


class SeatPreference(BaseModel):
    row: int = Field(ge=1, le=30)
    seat: Literal["A", "B", "C", "D", "E", "F"]


# Este agente es responsable de extraer la selección de asiento del usuario
seat_preference_agent = Agent(
    model,
    result_type=SeatPreference | Failed,
    system_prompt=("Extrae la preferencia de asiento del usuario. " "Los asientos A y F son asientos de ventana. " "La fila 1 es la primera fila y tiene espacio adicional para las piernas. " "Las filas 14 y 20 también tienen espacio adicional para las piernas. "),
)


async def find_seat(usage: Usage) -> SeatPreference:
    message_history: list[ModelMessage] | None = None
    while True:
        answer = Prompt.ask("¿Qué asiento te gustaría?")

        result = await seat_preference_agent.run(
            answer,
            message_history=message_history,
            usage=usage,
            usage_limits=usage_limits,
        )
        if isinstance(result.data, SeatPreference):
            return result.data
        else:
            print("No se pudo entender la preferencia de asiento. Por favor intenta de nuevo.")
            message_history = result.all_messages()


async def main():
    usage: Usage = Usage()

    opt_flight_details = await find_flight(usage)
    if opt_flight_details is not None:
        print(f"Vuelo encontrado: {opt_flight_details.flight_number}")
        # > Vuelo encontrado: AK456
        seat_preference = await find_seat(usage)
        print(f"Preferencia de asiento: {seat_preference}")
        # > Preferencia de asiento: row=1 seat='A'


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
