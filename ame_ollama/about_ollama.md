# Ollama Python Library

The Ollama Python library provides the easiest way to integrate Python 3.8+ projects with Ollama.

pip install ollama


import ollama

response = ollama.chat(model='llama2', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])

print(response['message']['content'])


## Streaming responses
Response streaming can be enabled by setting stream=True, modifying function calls to return a Python generator where each part is an object in the stream.

import ollama

stream = ollama.chat(
    model='llama2',
    messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)

## API
- The Ollama Python library's API is designed around the Ollama REST API

ollama.chat(model='llama2', messages=[{'role': 'user', 'content': 'Why is the sky blue?'}])

### Generate
ollama.generate(model='llama2', prompt='Why is the sky blue?')

### List
ollama.list()

### Show
ollama.show('llama2')

### Create
modelfile='''
FROM llama2
SYSTEM You are mario from super mario bros.
'''

ollama.create(model='example', modelfile=modelfile)

### Copy
ollama.copy('llama2', 'user/llama2')

### Delete
ollama.delete('llama2')

### Pull
ollama.pull('llama2')

### Push
ollama.push('user/llama2')

### Embeddings
ollama.embeddings(model='llama2', prompt='The sky is blue because of rayleigh scattering')

### Custom client
- A custom client can be created with the following fields:
- host: The Ollama host to connect to
- timeout: The timeout for requests

- from ollama import Client
client = Client(host='http://localhost:11434')
response = client.chat(model='llama2', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])

### Async client
import asyncio
from ollama import AsyncClient

async def chat():
  message = {'role': 'user', 'content': 'Why is the sky blue?'}
  response = await AsyncClient().chat(model='llama2', messages=[message])

asyncio.run(chat())

Setting stream=True modifies functions to return a Python asynchronous generator:

import asyncio
from ollama import AsyncClient

async def chat():
  message = {'role': 'user', 'content': 'Why is the sky blue?'}
  async for part in await AsyncClient().chat(model='llama2', messages=[message], stream=True):
    print(part['message']['content'], end='', flush=True)

asyncio.run(chat())
Errors
Errors are raised if requests return an error status or if an error is detected while streaming.

model = 'does-not-yet-exist'

try:
  ollama.chat(model)
except ollama.ResponseError as e:
  print('Error:', e.error)
  if e.status_code == 404:
    ollama.pull(model)
