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
                "Eres un asistente especializado en extraer información de una base de conocimientos técnica.\n"
                "TU UNICA FUENTE DE VERDAD: La herramienta 'consultar_documento'.\n"
                "REGLA: Si el usuario pregunta algo técnico, usa la herramienta. NO respondas con tus conocimientos previos.\n"
                "Una vez que recibas el contenido del documento, resume la información para responder al usuario."
            )
        },
        {'role': 'user', 'content': user_input}
    ]
    
    for _ in range(5):
        try:
            response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)
        except Exception as e:
            raise Exception(f"No se pudo conectar con Ollama: {e}")

        name, args, tool_call_id = None, None, None
        
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
                    # Extraer JSON si hay texto alrededor
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    tool_data = json.loads(content[start:end])
                    name = tool_data.get('name')
                    args = tool_data.get('parameters', tool_data.get('arguments', {}))
                    if isinstance(args, dict) and 'object' in args:
                        try: args = json.loads(args['object'])
                        except: pass
                    
                    # Truco: Inyectamos una llamada formal en la historia para que Ollama no se pierda
                    fake_message = {
                        'role': 'assistant',
                        'content': '',
                        'tool_calls': [{'function': {'name': name, 'arguments': args}}]
                    }
                    messages.append(fake_message)
                else:
                    return response.message.content
            except:
                return response.message.content

        if name:
            print(f"\n[Consultando base de conocimientos: {name}]")
            result = run_tool(name, args)
            messages.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
            # Continuamos el loop para que Ollama procese el resultado
        else:
            return response.message.content
            
    return "Se alcanzó el límite de pasos sin una respuesta final."
