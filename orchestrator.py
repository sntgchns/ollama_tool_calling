import ollama
import json
import os
from dotenv import load_dotenv
from tools_registry import TOOLS, run_tool

load_dotenv()

MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")

def chat_with_ollama(user_input):
    messages = [
        {'role': 'system', 'content': "Eres un Agente Experto de Soporte. Pasos obligatorios: 1. verificar_estado_servidor. 2. consultar_documento('guia_infraestructura'). 3. ejecutar_reinicio_servicio.\nREGLA: Usa las herramientas de forma formal. Si respondes con un JSON, asegúrate de que sea una llamada a herramienta válida."}
    ]
    messages.append({'role': 'user', 'content': user_input})
    
    for _ in range(10):
        try:
            response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)
        except Exception as e:
            raise Exception(f"Error conectando con Ollama: {e}")

        name, args = None, None
        if response.message.tool_calls:
            tool_call = response.message.tool_calls[0]
            name = tool_call.function.name
            args = tool_call.function.arguments
        else:
            # Fallback para JSON en contenido
            try:
                content = response.message.content.strip()
                if content.startswith('{'):
                    tool_data = json.loads(content)
                    name = tool_data.get('name')
                    args = tool_data.get('parameters', tool_data.get('arguments', {}))
                    if isinstance(args, dict) and 'object' in args:
                        try: args = json.loads(args['object'])
                        except: pass
                else:
                    return response.message.content
            except:
                return response.message.content

        if name:
            # Simulamos el mensaje del asistente con la llamada
            messages.append({'role': 'assistant', 'content': response.message.content, 'tool_calls': response.message.tool_calls or []})
            print(f"\n[Ejecutando: {name}]")
            
            try:
                result = run_tool(name, args)
                messages.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
            except Exception as e:
                messages.append({'role': 'tool', 'content': json.dumps({"error": str(e)}), 'name': name})
        else:
            return response.message.content

    return "Error: Se alcanzó el límite de pasos del agente sin obtener una respuesta final."
