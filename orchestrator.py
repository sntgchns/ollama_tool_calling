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
    Orquestador con soporte para memoria. 
    Recibe la lista completa de mensajes de la conversación.
    """
    for i in range(5):
        try:
            response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)
        except Exception as e:
            raise Exception(f"No se pudo conectar con Ollama: {e}")

        name, args = None, None
        
        # 1. Detectar llamada formal
        if response.message.tool_calls:
            tool_call = response.message.tool_calls[0]
            name = tool_call.function.name
            args = tool_call.function.arguments
            messages.append(response.message)
        else:
            # 2. Detectar intención de llamada en texto (fallback Regex)
            content = response.message.content.strip()
            if '{' in content and '"name"' in content:
                try:
                    name_match = re.search(r'"name":\s*"([^"]+)"', content)
                    if name_match:
                        name = name_match.group(1)
                        file_match = re.search(r'"nombre_archivo":\s*"([^"]+)"', content)
                        args = {'nombre_archivo': file_match.group(1) if file_match else "computacion_cuantica"}
                        
                        msg = {'role': 'assistant', 'content': content, 'tool_calls': [{'function': {'name': name, 'arguments': args}}]}
                        messages.append(msg)
                except: pass
            
            # 3. Si no hay llamada y es el primer turno del loop (i=0), forzamos si es necesario
            # Nota: En modo memoria, i=0 no significa necesariamente el inicio de la charla
            
            # 4. Respuesta final (limpia de JSON)
            if not name:
                final_answer = re.sub(r'\{.*\}', '', response.message.content, flags=re.DOTALL).strip()
                # Añadimos la respuesta final a la historia
                messages.append({'role': 'assistant', 'content': final_answer})
                return final_answer

        if name:
            print(f"\n[SISTEMA] Consultando herramienta: {name}...")
            result = run_tool(name, args)
            
            if isinstance(result, dict) and 'contenido' in result:
                print(f"[SISTEMA] Datos recuperados con éxito ({len(result['contenido'])} caracteres).\n")
            
            messages.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
            
    return "Se alcanzó el límite de pasos sin una respuesta final."
