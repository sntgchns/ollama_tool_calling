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
    Orquestador experto con memoria optimizada para agentes ReAct.
    Evita que el modelo se pierda en charlas innecesarias.
    """
    
    # Creamos una copia de trabajo para el bucle de pensamiento (scratchpad)
    pensamiento = list(messages)
    
    for paso in range(10):
        try:
            response = ollama.chat(model=MODEL, messages=pensamiento, tools=TOOLS)
        except Exception as e:
            raise Exception(f"Error conectando con Ollama: {e}")

        name, args = None, None
        content = response.message.content.strip()
        
        # 1. Intentar obtener llamada formal
        if response.message.tool_calls:
            tool_call = response.message.tool_calls[0]
            name = tool_call.function.name
            args = tool_call.function.arguments
            pensamiento.append(response.message)
        else:
            # 2. Fallback robusto con Regex
            if '{' in content and '"name"' in content:
                try:
                    name_match = re.search(r'"name":\s*"([^"]+)"', content)
                    if name_match:
                        name = name_match.group(1)
                        # Extracción de argumentos específica para experto
                        if r'"nombre_archivo":\s*"([^"]+)"' in content:
                            args = {'nombre_archivo': re.search(r'"nombre_archivo":\s*"([^"]+)"', content).group(1)}
                        elif r'"servicio":\s*"([^"]+)"' in content:
                            args = {'servicio': re.search(r'"servicio":\s*"([^"]+)"', content).group(1)}
                        else:
                            args = {}
                        
                        msg = {
                            'role': 'assistant', 
                            'content': f"Acción: {name}", 
                            'tool_calls': [{'function': {'name': name, 'arguments': args}}]
                        }
                        pensamiento.append(msg)
                except: pass

        if name:
            print(f"\n[PASO {paso+1}] Ejecutando: {name}...")
            result = run_tool(name, args)
            pensamiento.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
            # El loop continúa...
        else:
            # 3. Si no hay herramienta, es la respuesta final.
            # Limpiamos el texto de basura JSON
            final_answer = re.sub(r'\{.*\}', '', content, flags=re.DOTALL).strip()
            
            if not final_answer:
                # Si el modelo se queda mudo, le obligamos a cerrar el caso
                if paso > 0:
                    pensamiento.append({'role': 'user', 'content': "Ya tienes todos los datos. Da tu respuesta final al usuario ahora."})
                    continue
                return "Lo siento, no pude procesar la solicitud."
            
            # Guardamos SOLO la respuesta final en la memoria real de la conversación
            messages.append({'role': 'assistant', 'content': final_answer})
            return final_answer

    return "Se alcanzó el límite de pasos del agente."
