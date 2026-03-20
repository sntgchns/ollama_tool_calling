import ollama
import json
import os
from tools_registry import TOOLS, run_tool

MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

def chat_with_ollama(user_input):
    messages = [
        {'role': 'system', 'content': "Agente Experto. Pasos: 1. verificar_estado_servidor. 2. consultar_documento('guia_infraestructura'). 3. ejecutar_reinicio_servicio. Una tool por turno."}
    ]
    messages.append({'role': 'user', 'content': user_input})
    
    for _ in range(10):
        try:
            response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)
        except Exception as e:
            raise Exception(f"Error conectando con Ollama: {e}")

        if not response.message.tool_calls:
            return response.message.content
        
        tool = response.message.tool_calls[0]
        messages.append({'role': 'assistant', 'content': '', 'tool_calls': [tool]})
        print(f"\n[Ejecutando: {tool.function.name}]")
        
        try:
            result = run_tool(tool.function.name, tool.function.arguments)
            messages.append({'role': 'tool', 'content': json.dumps(result), 'name': tool.function.name})
        except Exception as e:
            messages.append({'role': 'tool', 'content': json.dumps({"error": str(e)}), 'name': tool.function.name})

    return "Error: Se alcanzó el límite de pasos del agente sin obtener una respuesta final."
