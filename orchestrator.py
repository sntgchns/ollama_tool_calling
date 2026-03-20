import ollama
import json
import os
import re
from dotenv import load_dotenv
from tools_registry import TOOLS, run_tool

load_dotenv()

MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")

def chat_with_ollama(user_input):
    messages = [
        {'role': 'system', 'content': "Eres un asistente matemático y de base de datos. Si necesitas realizar cálculos o consultas, utiliza las herramientas proporcionadas. Si respondes con un JSON, asegúrate de que sea una llamada a herramienta válida siguiendo el formato esperado."}
    ]
    messages.append({'role': 'user', 'content': user_input})
    
    try:
        response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)
    except Exception as e:
        raise Exception(f"No se pudo conectar con Ollama (Modelo: {MODEL}). Error: {e}")

    tool_calls_to_process = []
    
    if response.message.tool_calls:
        for tc in response.message.tool_calls:
            tool_calls_to_process.append((tc.function.name, tc.function.arguments))
        messages.append(response.message)
    else:
        # Fallback para JSON en contenido (Robusto con Regex)
        try:
            content = response.message.content.strip()
            if '{' in content:
                # Intentar encontrar múltiples JSONs o llamadas
                name_match = re.search(r'"name":\s*"([^"]+)"', content)
                if name_match:
                    name = name_match.group(1)
                    # Extracción simple de argumentos (básica para esta rama)
                    args = {}
                    # Ejemplo: "a": 5, "b": 10
                    matches = re.findall(r'"(\w+)":\s*([\d\.]+|"[^"]+")', content)
                    for k, v in matches:
                        if k != "name":
                            args[k] = json.loads(v)
                    
                    if name:
                        tool_calls_to_process.append((name, args))
                        # Inyectamos mensaje para consistencia
                        fake_message = {
                            'role': 'assistant', 
                            'content': f"Calculando {name}...",
                            'tool_calls': [{'function': {'name': name, 'arguments': args}}]
                        }
                        messages.append(fake_message)
        except:
            pass

    if tool_calls_to_process:
        for name, args in tool_calls_to_process:
            print(f"\n[Ejecutando herramienta: {name}]")
            result = run_tool(name, args)
            messages.append({'role': 'tool', 'content': str(result), 'name': name})
        
        try:
            final_response = ollama.chat(model=MODEL, messages=messages)
            return final_response.message.content
        except Exception as e:
            raise Exception(f"Error en la respuesta final de Ollama: {e}")
    
    return response.message.content
