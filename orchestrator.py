import ollama
import os
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")

def chat_with_ollama(messages):
    """
    Orquestador simple con soporte para memoria.
    Recibe la lista completa de mensajes.
    """
    try:
        # Llamada simple a Ollama sin herramientas
        response = ollama.chat(
            model=MODEL,
            messages=messages
        )
        return response.message.content
    except Exception as e:
        raise Exception(f"No se pudo conectar con Ollama (Modelo: {MODEL}). Error: {e}")
