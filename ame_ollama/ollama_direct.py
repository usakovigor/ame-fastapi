import ollama
import asyncio
from ollama import AsyncClient, Client


async def ollama_ai_call(system_message, user_message, model="llama3", stream=True):
    response = ollama.chat(
        model=model,
        messages=[
            {
                'role': 'system',
                'content': system_message

            },
            {
                'role': 'user',
                'content': user_message
            }
        ],
        stream=stream,
    )

    if stream:
        for chunk in response:
            print(chunk['message']['content'], end='', flush=True)
    else:
        response_content = response['message']['content']
        return response_content


async def ollama_async_chat(system_message, user_message, model="llama3", stream=True):
    async for part in await AsyncClient().chat(
            model=model,
            messages=[
                {
                    'role': 'system',
                    'content': system_message

                },
                {
                    'role': 'user',
                    'content': user_message
                }
            ]
            ,
            stream=stream):
        print(part['message']['content'], end='', flush=True)


def custom_ollama_client(host, system_message, user_message, model="llama3", stream=True):
    client = Client(host=host)
    response = client.chat(
        model=model,
        messages=[
            {
                'role': 'system',
                'content': system_message

            },
            {
                'role': 'user',
                'content': user_message
            }
        ],
        stream=stream,
    )

    if stream:
        for chunk in response:
            print(chunk['message']['content'], end='', flush=True)
    else:
        response_content = response['message']['content']
        return response_content


def list_ollama_models():
    print(ollama.list())
    return


def run_ollama_task(task, params):
    model = params.get('model', 'llama3')
    stream = params.get('stream', True)
    system_message = params.get('system_message', 'You are a helpful assistant.')
    user_message = params.get('user_message')
    host = params.get('host', None)

    if task == "dynamic_call":
        return asyncio.run(ollama_ai_call(system_message=system_message, user_message=user_message, model=model, stream=stream))
    elif task == "async_chat":
        return asyncio.run(ollama_async_chat(system_message=system_message, user_message=user_message, model=model, stream=stream))
    elif task == "custom_client" and host:
        return custom_ollama_client(host=host, system_message=system_message, user_message=user_message, model=model, stream=stream)
    elif task == "custom_client" and not host:
        print("Host is required for custom_ollama_client task.")
    elif task == "list_models":
        return list_ollama_models()
    else:
        return None


if __name__ == "__main__":
    import asyncio

    all_models = ['llama3:instruct', 'llama3:latest', 'llama3:text', 'mistral:latest', 'phi3:instruct', 'phi3:latest', 'phi3:mini']

    model = "phi3:mini"
    stream = True
    system_message = "You provide very long and detailed answers. When I ask you a question, make sure to consider what I might be asking and provide as much information as possible."
    user_message = "Tell me everything you know about the history of the United States."

    # list_ollama_models()
    # ollama_async_chat
    # ollama_ai_call
    # custom_ollama_client
    # asyncio.run(ollama_ai_call(system_message=system_message, user_message=user_message, model=model, stream=stream))

    params = {
        "model": model,
        "stream": stream,
        "system_message": system_message,
        "user_message": user_message,
        "host": "http://localhost:11434"
    }
    task_options = ["dynamic_call", "async_chat", "custom_client", "list_models"]

    task = "dynamic_call"
    run_ollama_task(task, params)

    # asyncio.run(ollama_async_chat(system_message=system_message, user_message=user_message, model=model, stream=stream))

    # example host format: 'http://localhost:11434'
