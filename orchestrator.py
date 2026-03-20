import ollama
import json
import os
import re
from dotenv import load_dotenv
from tools_registry import TOOLS, run_tool

load_dotenv()

MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")

def chat_with_ollama(messages):
    """
    Orquestador matemático con soporte para memoria.
    """
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
                        # Búsqueda agresiva de números
                        nums = re.findall(r'(\d+\.?\d*)', content)
                        if nums:
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
                    final_answer = re.sub(r'\{.*\}', '', response.message.content, flags=re.DOTALL).strip()
                    messages.append({'role': 'assistant', 'content': final_answer})
                    return final_answer
            except:
                messages.append(response.message)
                return response.message.content

        if name:
            print(f"\n[Ejecutando herramienta: {name} con argumentos: {args}]")
            result = run_tool(name, args)
            messages.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
        else:
            final_answer = re.sub(r'\{.*\}', '', response.message.content, flags=re.DOTALL).strip()
            messages.append({'role': 'assistant', 'content': final_answer})
            return final_answer

    return "Se alcanzó el límite de pasos sin una respuesta final."
