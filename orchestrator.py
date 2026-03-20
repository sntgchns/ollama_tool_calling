import ollama
import json
import os
import re
from dotenv import load_dotenv
from tools_registry import TOOLS, run_tool

load_dotenv()

MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")

def chat_with_ollama(messages):
    """
    Orquestador experto con soporte para memoria.
    """
    for _ in range(10):
        try:
            response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)
        except Exception as e:
            raise Exception(f"Error conectando con Ollama: {e}")

        name, args = None, None
        
        # 1. Intentar obtener llamada formal
        if response.message.tool_calls:
            tool_call = response.message.tool_calls[0]
            name = tool_call.function.name
            args = tool_call.function.arguments
            messages.append(response.message)
        else:
            # 2. Fallback para JSON en contenido (incluso si está mal formado)
            try:
                content = response.message.content.strip()
                if '{' in content:
                    # Intentar extraer el nombre de la función con Regex (Raw strings)
                    name_match = re.search(r'"name":\s*"([^"]+)"', content)
                    if name_match:
                        name = name_match.group(1)
                        if r'"nombre_archivo":\s*"([^"]+)"' in content:
                            args = {'nombre_archivo': re.search(r'"nombre_archivo":\s*"([^"]+)"', content).group(1)}
                        elif r'"servicio":\s*"([^"]+)"' in content:
                            args = {'servicio': re.search(r'"servicio":\s*"([^"]+)"', content).group(1)}
                        else:
                            args = {}
                    
                    if name:
                        # Limpiamos el contenido del mensaje del asistente para evitar confusiones al modelo
                        fake_message = {
                            'role': 'assistant',
                            'content': f"Llamando a {name}...",
                            'tool_calls': [{'function': {'name': name, 'arguments': args}}]
                        }
                        messages.append(fake_message)
                else:
                    final_answer = re.sub(r'\{.*\}', '', response.message.content, flags=re.DOTALL).strip()
                    messages.append({'role': 'assistant', 'content': final_answer})
                    return final_answer
            except:
                messages.append(response.message)
                return response.message.content

        if name:
            print(f"\n[Ejecutando herramienta: {name}]")
            result = run_tool(name, args)
            messages.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
        else:
            final_answer = re.sub(r'\{.*\}', '', response.message.content, flags=re.DOTALL).strip()
            messages.append({'role': 'assistant', 'content': final_answer})
            return final_answer

    return "Error: Se alcanzó el límite de pasos del agente sin obtener una respuesta final."
