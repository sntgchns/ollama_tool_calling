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
    Orquestador experto con Guía de Estado Activa.
    Mantiene al modelo enfocado en la secuencia: Verificar -> Consultar -> Reiniciar.
    """
    
    pensamiento = list(messages)
    pasos_completados = []
    
    # Normalizador de nombres para el chequeo de estado
    def norm(n): return n.replace("_", "").lower()

    for paso in range(10):
        try:
            response = ollama.chat(model=MODEL, messages=pensamiento, tools=TOOLS)
        except Exception as e:
            raise Exception(f"Error conectando con Ollama: {e}")

        name, args = None, None
        content = response.message.content.strip()
        
        # 1. Identificar llamada (Formal o Regex)
        if response.message.tool_calls:
            tool_call = response.message.tool_calls[0]
            name = tool_call.function.name
            args = tool_call.function.arguments
            pensamiento.append(response.message)
        else:
            if '{' in content and '"name"' in content:
                try:
                    name_match = re.search(r'"name":\s*"([^"]+)"', content)
                    if name_match:
                        name = name_match.group(1)
                        # Extracción básica de args
                        file_match = re.search(r'"nombre_archivo":\s*"([^"]+)"', content)
                        serv_match = re.search(r'"servicio":\s*"([^"]+)"', content)
                        args = {'nombre_archivo': file_match.group(1)} if file_match else ({'servicio': serv_match.group(1)} if serv_match else {})
                        
                        msg = {'role': 'assistant', 'content': f"Acción: {name}", 'tool_calls': [{'function': {'name': name, 'arguments': args}}]}
                        pensamiento.append(msg)
                except: pass

        if name:
            # Evitamos que repita herramientas innecesariamente
            if name in pasos_completados and name != "consultar_documento":
                pensamiento.append({'role': 'system', 'content': f"Ya ejecutaste {name}. Pasa al SIGUIENTE paso del protocolo."})
                continue

            print(f"\n[PASO {paso+1}] Ejecutando: {name}...")
            result = run_tool(name, args)
            pensamiento.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
            pasos_completados.append(name)
        else:
            # 2. Verificación de progreso si intenta dar respuesta final
            completados_norm = [norm(n) for n in pasos_completados]
            
            if "verificarestadoservidor" not in completados_norm:
                pensamiento.append({'role': 'system', 'content': "DEBES empezar usando 'verificar_estado_servidor'. No hables, solo actúa."})
            elif "consultardocumento" not in completados_norm:
                pensamiento.append({'role': 'system', 'content': "Ya tienes el error. Ahora DEBES usar 'consultar_documento' con 'guia_infraestructura'."})
            elif "ejecutarreinicioservicio" not in completados_norm:
                pensamiento.append({'role': 'system', 'content': "Ya sabes qué servicio falla. Ahora DEBES usar 'ejecutar_reinicio_servicio'."})
            else:
                # Si todo está hecho, aceptamos la respuesta final
                final_answer = re.sub(r'\{.*\}', '', content, flags=re.DOTALL).strip()
                if final_answer:
                    messages.append({'role': 'assistant', 'content': final_answer})
                    return final_answer
                else:
                    pensamiento.append({'role': 'user', 'content': "¡Excelente trabajo! Resume el éxito de la operación al usuario."})

    return "El agente no pudo completar el protocolo en 10 pasos."
