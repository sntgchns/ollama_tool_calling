import ollama
import json
import os
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
                "- Si respondes con un JSON, asegúrate de que sea una llamada a herramienta válida."
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
            # 2. Fallback para JSON en contenido
            try:
                content = response.message.content.strip()
                if '{' in content:
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    tool_data = json.loads(content[start:end])
                    name = tool_data.get('name')
                    args = tool_data.get('parameters', tool_data.get('arguments', {}))
                    if isinstance(args, dict) and 'object' in args:
                        try: args = json.loads(args['object'])
                        except: pass
                    
                    # Inyectamos llamada formal para consistencia de la historia
                    fake_message = {
                        'role': 'assistant',
                        'content': content,
                        'tool_calls': [{'function': {'name': name, 'arguments': args}}]
                    }
                    messages.append(fake_message)
                else:
                    return response.message.content
            except:
                return response.message.content

        if name:
            print(f"\n[Ejecutando herramienta: {name}]")
            result = run_tool(name, args)
            messages.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
        else:
            return response.message.content

    return "Error: Se alcanzó el límite de pasos del agente sin obtener una respuesta final."
