import asyncio

from fastapi import FastAPI, HTTPException
from ollama import AsyncClient
from starlette.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
from ame_ollama.ollama_caller import OllamaManager
from fastapi.responses import PlainTextResponse
import ngrok
import uvicorn
from pyngrok import ngrok
from fastapi.responses import HTMLResponse, PlainTextResponse
import os

app = FastAPI()
manager = OllamaManager()


class ChatMessage(BaseModel):
    user_message: str


class OllamaParam(BaseModel):
    model: str = "llama3"
    messages: List[str] = []
    stream: bool = True


@app.get("/", response_class=PlainTextResponse)
def get_current_model_names():
    try:
        pretty_models = manager.pretty_mobile_model_names()
        return pretty_models
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/list_models")
def list_models():
    try:
        models = manager.list_models()
        return models
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/show_model/{model}")
def show_model(model: str):
    try:
        model_info = manager.show_models(model)
        return model_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pull_model/{model}")
def pull_model(model: str):
    try:
        model_info = manager.pull_model(model)
        return model_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/current_model_names")
def get_current_model_names():
    try:
        model_names = manager.get_current_model_names()
        return model_names
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def async_chat(user_message, model="llama3", stream=True):
    client = AsyncClient()
    async for part in await client.chat(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': user_message
                    }
            ],
            stream=stream):
        yield part['message']['content']


@app.post("/chat")
async def simple_chat(chat_message: ChatMessage):
    try:
        return StreamingResponse(async_chat(chat_message.user_message, model="llama3", stream=True), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ollama_call")
async def ollama_call(params: OllamaParam):
    try:
        return await manager.ollama_call(model=params.model, messages=params.messages, stream=params.stream)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ollama_param_call")
async def ollama_param_call(params: OllamaParam):
    try:
        return await manager.ollama_param_call(params=params.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create_embeddings")
def create_embeddings(model: str, text: str, options: Optional[dict] = None, keep_alive: bool = False):
    try:
        embeddings = manager.create_embeddings(model, text, options, keep_alive)
        return embeddings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def setup_ngrok():
    ngrok.set_auth_token("2bdirkXuBrXeF1gJU7YX4VsUrNE_7CDy4KG3CQXVkHimREjgp")
    tunnel = ngrok.connect(8500)
    print(f"Ingress established at: {tunnel.public_url}")


if __name__ == "__main__":
    setup_ngrok()
    uvicorn.run(app, host="0.0.0.0", port=8500)
