# Demos de Frameworks de Agentes de IA en Python

[![Open in GitHub Codespaces](https://img.shields.io/static/v1?style=for-the-badge&label=GitHub+Codespaces&message=Open&color=brightgreen&logo=github)](https://codespaces.new/Azure-Samples/python-ai-agent-frameworks-demos)
[![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Azure-Samples/python-ai-agent-frameworks-demos)

Este repositorio contiene ejemplos de muchos frameworks populares de agentes de IA en Python usando LLMs de [GitHub Models](https://github.com/marketplace/models). Estos modelos son gratuitos, con un [límite diario](https://docs.github.com/github-models/prototyping-with-ai-models#rate-limits), solo necesitas una cuenta de GitHub, .

* [Cómo empezar](#cómo-empezar)
    * [GitHub Codespaces](#github-codespaces)
    * [VS Code Dev Containers](#vs-code-dev-containers)
    * [Entorno local](#entorno-local)
* [Ejecutando los ejemplos de Python](#ejecutando-los-ejemplos-de-python)
* [Configurando GitHub Models](#configurando-github-models)
* [Aprovisionando recursos de Azure AI](#aprovisionando-recursos-de-azure-ai)
* [Recursos](#recursos)

## Cómo empezar

Tienes varias opciones para empezar con este repositorio.
La forma más rápida es usar GitHub Codespaces, ya que todo se configurará automaticamente, pero también puedes [configurarlo localmente](#local-environment).

### GitHub Codespaces

Puedes ejecutar este repositorio virtualmente usando GitHub Codespaces. El botón abrirá una instancia de VS Code basada en web en tu navegador:

1. Presiona este botón para abrir el repositorio en un codespace (esto puede tardar varios minutos, ya que se está configurando el entorno):

    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Azure-Samples/python-ai-agent-frameworks-demos)

2. Abre una ventana de terminal
3. Continúa con los pasos para ejecutar los ejemplos

### VS Code Dev Containers

Una opción similar es VS Code Dev Containers, que abrirá el proyecto en tu VS Code local usando la [extensión Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers):

1. Inicia Docker Desktop (instálalo si aún no lo tienes)
2. Abre el proyecto:

    [![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Azure-Samples/python-ai-agent-frameworks-demos)

3. En la ventana de VS Code que se abre, una vez que aparezcan los archivos del proyecto (esto puede tardar varios minutos), abre una ventana de terminal.
4. Continúa con los pasos para ejecutar los ejemplos

### Entorno local

1. Asegúrate de tener instaladas las siguientes herramientas:

    * [Python 3.10+](https://www.python.org/downloads/)
    * Git

2. Clona el repositorio:

    ```shell
    git clone https://github.com/Azure-Samples/python-ai-agent-frameworks-demos
    cd python-ai-agents-demos
    ```

3. Configura un entorno virtual:

    ```shell
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

4. Instala los requisitos:

    ```shell
    pip install -r requirements.txt
    ```

## Ejecutando los ejemplos de Python

Puedes ejecutar los ejemplos en este repositorio ejecutando los scripts en el directorio `examples\spanish`. Cada script demuestra un patrón o framework de agente de IA diferente.

| Ejemplo | Descripción |
| ------- | ----------- |
| [autogen_magenticone.py](autogen_magenticone.py) | Usa AutoGen con el agente orquestador MagenticOne para planificación de viajes. |
| [autogen_swarm.py](autogen_swarm.py) | Usa AutoGen con el agente orquestador Swarm para solicitudes de reembolso de vuelos. |
| [langgraph.py](langgraph.py) | Usa LangGraph para construir un agente con StateGraph para reproducir canciones. |
| [llamaindex.py](llamaindex.py) | Usa LlamaIndex para construir un agente ReAct para RAG en múltiples índices. |
| [openai_agents.py](openai_agents.py) | Usa el framework OpenAI Agents para transferir entre varios agentes con herramientas. |
| [openai_functioncalling.py](openai_functioncalling.py) | Usa OpenAI Function Calling para llamar funciones basadas en la salida del LLM. |
| [pydanticai.py](pydanticai.py) | Usa PydanticAI para construir un flujo de trabajo secuencial de dos agentes para planificación de vuelos. |
| [semantickernel.py](semantickernel.py) | Usa Semantic Kernel para construir un flujo de trabajo de dos agentes escritor/editor. |
| [smolagents_codeagent.py](smolagents_codeagent.py) | Usa SmolAgents para construir un agente de respuesta a preguntas que puede buscar en la web y ejecutar código. |

## Configurando GitHub Models

Si abres este repositorio en GitHub Codespaces, puedes ejecutar los scripts gratuitamente usando GitHub Models sin pasos adicionales, ya que tu `GITHUB_TOKEN` ya está configurado en el entorno de Codespaces.

Si quieres ejecutar los scripts localmente, necesitas configurar la variable de entorno `GITHUB_TOKEN` con un token de acceso personal (PAT) de GitHub. Puedes crear un PAT siguiendo estos pasos:

1. Ve a la configuración de tu cuenta de GitHub.
2. Haz clic en "Developer settings" en la barra lateral izquierda.
3. Haz clic en "Personal access tokens" en la barra lateral izquierda.
4. Haz clic en "Tokens (classic)" o "Fine-grained tokens" según tu preferencia.
5. Haz clic en "Generate new token".
6. Dale un nombre a tu token y selecciona los permisos que quieres otorgar. Para este proyecto, no necesitas permisos específicos.
7. Haz clic en "Generate token".
8. Copia el token generado.
9. Configura la variable de entorno `GITHUB_TOKEN` en tu terminal o IDE:

    ```shell
    export GITHUB_TOKEN=your_personal_access_token
    ```

## Aprovisionando recursos de Azure AI

Puedes ejecutar todos los ejemplos en este repositorio usando GitHub Models. Si quieres ejecutar los ejemplos usando modelos de Azure OpenAI, necesitas aprovisionar los recursos de Azure AI, lo que implicará costos.

Este proyecto incluye infraestructura como código (IaC) para aprovisionar despliegues de Azure OpenAI de "gpt-4o" y "text-embedding-3-large". La IaC está definida en el directorio `infra` y usa el Azure Developer CLI para aprovisionar los recursos.

1. Asegúrate de tener instalado el [Azure Developer CLI (azd)](https://aka.ms/install-azd).

2. Inicia sesión en Azure:

    ```shell
    azd auth login
    ```

    Para usuarios de GitHub Codespaces, si el comando anterior falla, intenta:

   ```shell
    azd auth login --use-device-code
    ```

3. Aprovisiona la cuenta de OpenAI:

    ```shell
    azd provision
    ```

    Te pedirá que proporciones un nombre de entorno `azd` (como "agents-demos"), selecciones una suscripción de tu cuenta de Azure y selecciones una ubicación. Luego aprovisionará los recursos en tu cuenta.

4. Una vez que los recursos estén aprovisionados, deberías ver un archivo `.env` local con todas las variables de entorno necesarias para ejecutar los scripts.
5. Para eliminar los recursos, ejecuta:

    ```shell
    azd down
    ```

## Recursos

* [Documentación de AutoGen](https://microsoft.github.io/autogen/)
* [Documentación de LangGraph](https://langchain-ai.github.io/langgraph/tutorials/introduction/)
* [Documentación de LlamaIndex](https://docs.llamaindex.ai/en/latest/)
* [Documentación de OpenAI Agents](https://openai.github.io/openai-agents-python/)
* [Documentación de OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling?api-mode=chat)
* [Documentación de PydanticAI](https://ai.pydantic.dev/multi-agent-applications/)
* [Documentación de Semantic Kernel](https://learn.microsoft.com/semantic-kernel/overview/)
* [Documentación de SmolAgents](https://huggingface.co/docs/smolagents/index)
