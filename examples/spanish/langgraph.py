# https://github.com/JRAlexander/IntroToAgents1-Oxford/blob/main/intro-langgraph/time-travel.ipynb

import os

import azure.identity
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode


@tool
def reproducir_cancion_en_spotify(cancion: str):
    """Reproducir una canción en Spotify"""
    # Llamar a la API de spotify ...
    return f"¡Reproduciendo exitosamente {cancion} en Spotify!"


@tool
def reproducir_cancion_en_apple(cancion: str):
    """Reproducir una canción en Apple Music"""
    # Llamar a la API de apple music ...
    return f"¡Reproduciendo exitosamente {cancion} en Apple Music!"


tools = [reproducir_cancion_en_apple, reproducir_cancion_en_spotify]
tool_node = ToolNode(tools)

# Configura el cliente para usar Azure OpenAI o GitHub Models
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")

if API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
    llm = AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
        openai_api_version=os.environ["AZURE_OPENAI_VERSION"],
        azure_ad_token_provider=token_provider,
    )
else:
    model = ChatOpenAI(model="gpt-4o-mini", base_url="https://models.inference.ai.azure.com", api_key=os.environ["GITHUB_TOKEN"])

model = model.bind_tools(tools, parallel_tool_calls=False)


# Define la función que determina si continuar o no
def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    # Si no hay llamada a función, terminamos
    if not last_message.tool_calls:
        return "end"
    # De lo contrario, si hay, continuamos
    else:
        return "continue"


# Define la función que llama al modelo
def call_model(state):
    messages = state["messages"]
    response = model.invoke(messages)
    # Devolvemos una lista, porque esto se agregará a la lista existente
    return {"messages": [response]}


# Define un nuevo grafo
workflow = StateGraph(MessagesState)

# Define los dos nodos entre los que vamos a alternar
workflow.add_node("agent", call_model)
workflow.add_node("action", tool_node)

# Establece el punto de entrada como `agent`
# Esto significa que este nodo es el primero en ser llamado
workflow.add_edge(START, "agent")

# Ahora agregamos un borde condicional
workflow.add_conditional_edges(
    # Primero, definimos el nodo de inicio. Usamos `agent`.
    # Esto significa que estos son los bordes que se toman después de que se llama al nodo `agent`.
    "agent",
    # Luego, pasamos la función que determinará qué nodo se llamará a continuación.
    should_continue,
    # Finalmente pasamos un mapeo.
    # Las claves son strings y los valores son otros nodos.
    # END es un nodo especial que marca que el grafo debe terminar.
    # Lo que sucederá es que llamaremos a `should_continue`, y luego la salida de eso
    # se comparará con las claves en este mapeo.
    # Según con cuál coincida, ese nodo será llamado a continuación.
    {
        # Si `tools`, entonces llamamos al nodo de herramientas.
        "continue": "action",
        # De lo contrario terminamos.
        "end": END,
    },
)

# Ahora agregamos un borde normal de `tools` a `agent`.
# Esto significa que después de llamar a `tools`, el nodo `agent` se llama a continuación.
workflow.add_edge("action", "agent")

# Configura la memoria
memory = MemorySaver()

# ¡Finalmente, lo compilamos!
# Esto lo compila en un LangChain Runnable,
# lo que significa que puedes usarlo como cualquier otro runnable

# Agregamos `interrupt_before=["action"]`
# Esto agregará un punto de interrupción antes de que se llame al nodo `action`
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}
input_message = HumanMessage(content="¿Puedes reproducir la canción más popular de Taylor Swift?")
for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
    event["messages"][-1].pretty_print()
