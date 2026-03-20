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
                "Eres un asistente matemático experto.\n"
                "REGLA DE ORO: Si usas una herramienta, DEBES incluir los números en el JSON.\n"
                "EJEMPLO: {\"name\": \"raiz_cuadrada\", \"parameters\": {\"x\": 83}}\n"
                "REGLA 2: El resultado de la herramienta es la VERDAD ABSOLUTA. No lo calcules tú mismo."
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
        
        if response.message.tool_calls:
            tool_call = response.message.tool_calls[0]
            name = tool_call.function.name
            args = tool_call.function.arguments
            messages.append(response.message)
        else:
            try:
                content = response.message.content.strip()
                if '{' in content:
                    name_match = re.search(r'"name":\s*"([^"]+)"', content)
                    if name_match:
                        name = name_match.group(1)
                        # Búsqueda agresiva: si no hay números en el JSON, buscamos en todo el texto del mensaje
                        nums = re.findall(r'(\d+\.?\d*)', content)
                        if nums:
                            # Usamos el último número encontrado como argumento probable
                            args = {'x': float(nums[-1]), 'a': float(nums[0])}
                        else:
                            args = {}
                    
                    if name:
                        fake_message = {
                            'role': 'assistant',
                            'content': f"Calculando {name}...",
                            'tool_calls': [{'function': {'name': name, 'arguments': args}}]
                        }
                        messages.append(fake_message)
                else:
                    return re.sub(r'\{.*\}', '', response.message.content).strip()
            except:
                return response.message.content

        if name:
            # DEBUG para el usuario (puedes quitarlo luego)
            print(f"\n[Ejecutando herramienta: {name} con argumentos: {args}]")
            result = run_tool(name, args)
            messages.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
        else:
            return re.sub(r'\{.*\}', '', response.message.content).strip()

    return "Se alcanzó el límite de pasos sin una respuesta final."
