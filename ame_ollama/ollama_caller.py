import ollama
import asyncio
from ollama import AsyncClient, Client
import pprint
import asyncio


class OllamaManager:
    def __init__(self):
        self.async_client = AsyncClient()

    def list_models(self):
        models = ollama.list()
        pprint.pprint(models)
        return models

    def show_models(self, model):
        model_show = ollama.show(model)
        pprint.pprint(model_show)
        return model_show

    def pull_model(self, model):
        print(f"\n[AI MATRIX ENGINE OLLAMA] Pulling model: {model}")
        print(f"This can take some time...")
        model_pull = ollama.pull(model)
        print(f"Model pulled: {model} | {model_pull}")
        return model_pull

    def get_current_model_names(self):
        model_name_list = []
        models = ollama.list()
        for model in models['models']:
            model_name_list.append(model['model'])

        print(f"[AI MATRIX ENGINE OLLAMA] Current models: {model_name_list}")
        return model_name_list

    def pretty_mobile_model_names(self):
        model_name_list = []
        models = ollama.list()
        output = "\nWELCOME TO AI MATRIX ENGINE\n"
        output += "\nAI MATRIX ENGINE OLLAMA Current Local AI Models:\n"
        for model in models['models']:
            model_name_list.append(model['model'])
            output += f"Model: {model['model']}\n"

        output += "\nAI MATRIX ENGINE Local Model Endpoints:\n"
        output += "/list_models - You are here!\n"
        output += "/show_model/{model} - Show details for a specific model\n"
        output += "/pull_model/{model} - Add a new specific model from Ollama\n"
        output += "/current_model_names - Get current model names\n"
        output += "/ollama_call - Call Ollama with a model and params\n"
        output += "/simple_chat - Chat with Ollama using a model and just a user_message prompt\n"
        output += "/ollama_ai_call - Chat with Ollama using a model and system_message and user_message prompts\n"
        output += "/ollama_async_chat - Chat with Ollama using a model and system_message and user_message prompts\n"
        output += "/custom_ollama_client - Chat with Ollama using a 'host' address\n"
        output += "/create_embeddings - Create embeddings using a model and text\n"
        output += "\nThey haven't all been fully tested, but they should work or may need a small change\n"

        return output

    async def ollama_call(self, model, messages, stream=True):
        response = ollama.chat(model=model, messages=messages, stream=stream)
        if stream:
            for chunk in response:
                print(chunk['message']['content'], end='', flush=True)
        else:
            response_content = response['message']['content']
            return response_content

    async def simple_chat(self, model, user_message, stream=True):
        messages = [{'role': 'user', 'content': user_message}]
        response = await self.async_client.chat(model=model, messages=messages, stream=stream)
        if stream:
            response_content = ""
            async for chunk in response:
                content = chunk['message']['content']
                if content:
                    print(content, end="")  # Print each piece of content without a new line
                    response_content += content  # Optionally accumulate if needed elsewhere
        else:
            response_content = await response['message']['content']
            print(response_content)  # Print the whole response if not streaming
        return response_content  # Optionally return the complete response for further use

    async def ollama_param_call(self, params):
        model = params.get('model', 'llama3')
        messages = params.get('messages', [])
        stream = params.get('stream', True)
        return await self.ollama_call(model=model, messages=messages, stream=stream)

    def create_embeddings(self, model, text, options=None, keep_alive=False):
        embeddings = ollama.embeddings(model=model, prompt=text, options=options, keep_alive=keep_alive)
        return embeddings

    async def ollama_ai_call(self, system_message, user_message, model="llama3", stream=True):
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

    async def ollama_async_chat(self, system_message, user_message, model="llama3", stream=True):
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

    def custom_ollama_client(self, host, system_message, user_message, model="llama3", stream=True):
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

    def run_ollama_task(self, task, params):
        model = params.get('model', 'llama3')
        stream = params.get('stream', True)
        system_message = params.get('system_message', 'You are a helpful assistant.')
        user_message = params.get('user_message')
        host = params.get('host', None)

        if task == "dynamic_call":
            return asyncio.run(self.ollama_ai_call(system_message=system_message, user_message=user_message, model=model, stream=stream))


if __name__ == "__main__":
    all_models = ['llama3:instruct', 'llama3:latest', 'llama3:text', 'mistral:latest', 'phi3:instruct', 'phi3:latest', 'phi3:mini']
    model = "phi3:mini"
    stream = True
    system_message = "You provide very long and detailed answers. When I ask you a question, make sure to consider what I might be asking and provide as much information as possible."
    user_message = "Tell me everything you know about the history of the United States."
    messages = [{
        'role': 'system',
        'content': system_message
    }, {
        'role': 'user',
        'content': user_message
    }]
    ollama_manager = OllamaManager()
    #ollama_manager.pull_model(model)
    asyncio.run(ollama_manager.simple_chat(model=model, user_message=user_message, stream=stream))
