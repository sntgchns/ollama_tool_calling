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
                "Eres un asistente con AMNESIA TOTAL sobre ciencia y tecnología.\n"
                "TU REGLA ABSOLUTA: No puedes responder NADA sobre temas técnicos (como física o computación) "
                "usando tu propia memoria. Estás OBLIGADO a usar 'consultar_documento' para CUALQUIER pregunta técnica.\n\n"
                "Si el usuario pregunta algo técnico, tu ÚNICA respuesta permitida es llamar a la herramienta.\n"
                "Solo después de leer el documento podrás hablar con el usuario."
            )
        },
        {'role': 'user', 'content': user_input}
    ]
    
    for _ in range(5):
        try:
            # Forzamos a Ollama a considerar las herramientas en cada paso
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
            # 2. Fallback robusto con Regex (Llama 3.2 a veces escribe el JSON directamente)
            content = response.message.content.strip()
            if '{' in content:
                try:
                    name_match = re.search(r'"name":\s*"([^"]+)"', content)
                    if name_match:
                        name = name_match.group(1)
                        file_match = re.search(r'"nombre_archivo":\s*"([^"]+)"', content)
                        # Si no encuentra 'nombre_archivo', intentamos adivinarlo del contexto técnico
                        nombre_archivo = file_match.group(1) if file_match else "computacion_cuantica"
                        args = {'nombre_archivo': nombre_archivo}
                        
                        fake_message = {
                            'role': 'assistant',
                            'content': f"Consultando base de datos para: {name}...",
                            'tool_calls': [{'function': {'name': name, 'arguments': args}}]
                        }
                        messages.append(fake_message)
                except:
                    pass

        if name:
            print(f"\n[Consultando base de conocimientos: {name}]")
            result = run_tool(name, args)
            messages.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
        else:
            # Si no hay llamada a herramienta y es el primer turno, forzamos al modelo
            if len(messages) <= 2:
                 # El modelo intentó responder sin herramienta, le recordamos su amnesia
                 messages.append({'role': 'system', 'content': "ERROR: No usaste la herramienta. Recuerda que no sabes nada, DEBES usar 'consultar_documento'."})
                 continue
            
            # Respuesta final limpia de JSON
            return re.sub(r'\{.*\}', '', response.message.content).strip()
            
    return "Se alcanzó el límite de pasos sin una respuesta final."
