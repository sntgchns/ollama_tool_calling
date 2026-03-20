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
        {
            'role': 'system',
            'content': (
                "Eres un asistente especializado en extraer información de una base de conocimientos técnica.\n"
                "TU UNICA FUENTE DE VERDAD: La herramienta 'consultar_documento'.\n"
                "REGLA: Si el usuario pregunta algo técnico, usa la herramienta. NO respondas con tus conocimientos previos.\n"
                "Una vez que recibas el contenido del documento, resume la información para responder al usuario de forma natural.\n"
                "IMPORTANTE: Envía solo la respuesta final en lenguaje natural, sin bloques JSON."
            )
        },
        {'role': 'user', 'content': user_input}
    ]
    
    for _ in range(5):
        try:
            response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)
        except Exception as e:
            raise Exception(f"No se pudo conectar con Ollama: {e}")

        name, args = None, None
        
        # 1. Intentar obtener llamada formal
        if response.message.tool_calls:
            tool_call = response.message.tool_calls[0]
            name = tool_call.function.name
            args = tool_call.function.arguments
            messages.append(response.message)
        else:
            # 2. Fallback para JSON en contenido (Robusto con Regex)
            try:
                content = response.message.content.strip()
                if '{' in content:
                    name_match = re.search(r'"name":\s*"([^"]+)"', content)
                    if name_match:
                        name = name_match.group(1)
                        # Búsqueda de argumentos
                        if r'"nombre_archivo":\s*"([^"]+)"' in content:
                            args = {'nombre_archivo': re.search(r'"nombre_archivo":\s*"([^"]+)"', content).group(1)}
                        else:
                            args = {}
                    
                    if name:
                        fake_message = {
                            'role': 'assistant',
                            'content': f"Consultando {name}...",
                            'tool_calls': [{'function': {'name': name, 'arguments': args}}]
                        }
                        messages.append(fake_message)
                else:
                    # Si no hay JSON, es respuesta final (limpiamos posibles residuos)
                    return re.sub(r'\{.*\}', '', response.message.content).strip()
            except:
                return response.message.content

        if name:
            print(f"\n[Consultando base de conocimientos: {name}]")
            result = run_tool(name, args)
            messages.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
        else:
            # Respuesta final limpia de JSON
            return re.sub(r'\{.*\}', '', response.message.content).strip()
            
    return "Se alcanzó el límite de pasos sin una respuesta final."
