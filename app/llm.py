import httpx
import asyncio

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "llama3.1:8b"

async def call_ollama(prompt: str, temperature: float = 0.2) -> str:
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "stream": False
    }
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]

def sync_call_ollama(prompt: str, temperature: float = 0.2) -> str:
    return asyncio.run(call_ollama(prompt, temperature))