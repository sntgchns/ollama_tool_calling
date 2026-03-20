import ollama
import os
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")

def chat_with_ollama(user_input):
    messages = [{'role': 'user', 'content': user_input}]
    
    try:
        # Llamada simple a Ollama sin herramientas
        response = ollama.chat(
            model=MODEL,
            messages=messages
        )
        return response.message.content
    except Exception as e:
        raise Exception(f"No se pudo conectar con Ollama (Modelo: {MODEL}). Asegúrate de que el servidor esté corriendo. Error: {e}")
