import ollama
import os
from tools_registry import TOOLS, run_tool

MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

def chat_with_ollama(user_input):
    messages = [{'role': 'user', 'content': user_input}]
    
    try:
        response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)
    except Exception as e:
        raise Exception(f"No se pudo conectar con Ollama (Modelo: {MODEL}). Error: {e}")

    if response.message.tool_calls:
        messages.append(response.message)
        for tool in response.message.tool_calls:
            name = tool.function.name
            args = tool.function.arguments
            print(f"\n[Ejecutando herramienta: {name}]")
            result = run_tool(name, args)
            messages.append({'role': 'tool', 'content': str(result), 'name': name})
        
        try:
            final_response = ollama.chat(model=MODEL, messages=messages)
            return final_response.message.content
        except Exception as e:
            raise Exception(f"Error en la respuesta final de Ollama: {e}")
    
    return response.message.content
