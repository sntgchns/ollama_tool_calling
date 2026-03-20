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
                "Eres un asistente que responde basándose EXCLUSIVAMENTE en documentos.\n"
                "REGLA DE ORO: Empieza tu respuesta mencionando el archivo que consultaste.\n"
                "Ejemplo: 'Basado en el documento computacion_cuantica.md, un qubit es...'\n"
                "Si la información no está en el documento, di: 'No encontré esa información en el manual'."
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
        
        if response.message.tool_calls:
            tool_call = response.message.tool_calls[0]
            name = tool_call.function.name
            args = tool_call.function.arguments
            messages.append(response.message)
        else:
            content = response.message.content.strip()
            if '{' in content and '"name"' in content:
                try:
                    name_match = re.search(r'"name":\s*"([^"]+)"', content)
                    if name_match:
                        name = name_match.group(1)
                        file_match = re.search(r'"nombre_archivo":\s*"([^"]+)"', content)
                        args = {'nombre_archivo': file_match.group(1) if file_match else "computacion_cuantica"}
                        fake_message = {'role': 'assistant', 'content': content, 'tool_calls': [{'function': {'name': name, 'arguments': args}}]}
                        messages.append(fake_message)
                except: pass
            
            if not name:
                return re.sub(r'\{.*"name":.*\}', '', response.message.content, flags=re.DOTALL).strip()

        if name:
            print(f"\n[SISTEMA] Leyendo archivo: {args.get('nombre_archivo', 'desconocido')}...")
            result = run_tool(name, args)
            
            # Mostramos una pequeña prueba visual de lo que se leyó
            if isinstance(result, dict) and 'contenido' in result:
                tamano = len(result['contenido'])
                print(f"[SISTEMA] ¡Éxito! Se han recuperado {tamano} caracteres de conocimiento real.\n")
            
            messages.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
            
    return "Se alcanzó el límite de pasos sin una respuesta final."
