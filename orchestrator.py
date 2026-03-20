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
                "Eres un Agente Experto de Soporte Técnico.\n"
                "TU MISIÓN: Solucionar problemas del servidor siguiendo un protocolo ESTRICTO.\n\n"
                "PASOS OBLIGATORIOS (UNO POR TURNO):\n"
                "1. Ejecuta 'verificar_estado_servidor' para obtener el código de error.\n"
                "2. Ejecuta 'consultar_documento' con nombre_archivo='guia_infraestructura' para buscar qué servicio corresponde al código de error.\n"
                "3. Ejecuta 'ejecutar_reinicio_servicio' con el nombre del servicio que encontraste.\n\n"
                "REGLAS CRÍTICAS:\n"
                "- NO adivines el error. DEBES verificarlo primero.\n"
                "- NO asumas el servicio. DEBES consultarlo en el manual.\n"
                "- NO des una respuesta final hasta que hayas completado los 3 pasos.\n"
                "- IMPORTANTE: Envía la respuesta final en lenguaje natural, sin bloques JSON."
            )
        }
    ]
    messages.append({'role': 'user', 'content': user_input})
    
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
                    # Si no hay JSON, es respuesta final (limpiamos posibles residuos)
                    return re.sub(r'\{.*\}', '', response.message.content).strip()
            except:
                return response.message.content

        if name:
            print(f"\n[Ejecutando herramienta: {name}]")
            result = run_tool(name, args)
            messages.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
        else:
            # Respuesta final limpia de JSON
            return re.sub(r'\{.*\}', '', response.message.content).strip()

    return "Error: Se alcanzó el límite de pasos del agente sin obtener una respuesta final."
