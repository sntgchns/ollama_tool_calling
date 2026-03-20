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
                "Eres un agente de búsqueda que NO sabe nada de computación cuántica.\n"
                "TU PROTOCOLO:\n"
                "1. SIEMPRE debes llamar a 'consultar_documento' antes de responder.\n"
                "2. Está PROHIBIDO responder con tu memoria. Usa SOLO el contenido del archivo.\n"
                "3. Tu primera respuesta técnica DEBE ser una llamada a la herramienta."
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
                        messages.append({'role': 'assistant', 'content': content, 'tool_calls': [{'function': {'name': name, 'arguments': args}}]})
                except: pass
            
            # 3. Si no hay llamada y es el inicio, forzamos al modelo
            if not name and i == 0:
                messages.append({'role': 'system', 'content': "ERROR: No has consultado el documento. Llama a 'consultar_documento' ahora."})
                continue
            
            # 4. Respuesta final (limpia de JSON)
            if not name:
                return re.sub(r'\{.*\}', '', response.message.content, flags=re.DOTALL).strip()

        if name:
            # AVISO VISUAL OBLIGATORIO
            print(f"\n[SISTEMA] Consultando herramienta: {name}...")
            result = run_tool(name, args)
            
            if isinstance(result, dict) and 'contenido' in result:
                print(f"[SISTEMA] Datos recuperados con éxito ({len(result['contenido'])} caracteres).\n")
            
            messages.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
            
    return "Se alcanzó el límite de pasos sin una respuesta final."
