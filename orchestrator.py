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
                "Eres un experto en computación cuántica que consulta manuales técnicos.\n"
                "REGLA: Si te preguntan algo técnico, usa 'consultar_documento'.\n"
                "Una vez que tengas el contenido, explica el concepto de forma clara basándote en el texto.\n"
                "NO respondas con JSON, responde con lenguaje natural."
            )
        },
        {'role': 'user', 'content': user_input}
    ]
    
    for i in range(5):
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
            # 2. Fallback robusto con Regex
            content = response.message.content.strip()
            if '{' in content and '"name"' in content:
                try:
                    name_match = re.search(r'"name":\s*"([^"]+)"', content)
                    if name_match:
                        name = name_match.group(1)
                        file_match = re.search(r'"nombre_archivo":\s*"([^"]+)"', content)
                        args = {'nombre_archivo': file_match.group(1) if file_match else "computacion_cuantica"}
                        
                        fake_message = {
                            'role': 'assistant',
                            'content': content,
                            'tool_calls': [{'function': {'name': name, 'arguments': args}}]
                        }
                        messages.append(fake_message)
                except: pass
            
            # Si no hay nombre de herramienta detectado, es la respuesta final
            if not name:
                # Limpiamos posibles residuos de JSON que el modelo a veces deja al final
                final_answer = re.sub(r'\{.*"name":.*\}', '', response.message.content, flags=re.DOTALL).strip()
                if not final_answer and i > 0:
                    # Si el modelo se quedó callado después de la herramienta, le pedimos que hable
                    messages.append({'role': 'user', 'content': "Por favor, resume la información que encontraste."})
                    continue
                return final_answer

        if name:
            print(f"\n[Consultando base de conocimientos: {name}]")
            result = run_tool(name, args)
            messages.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
            
    return "Se alcanzó el límite de pasos sin una respuesta final."
