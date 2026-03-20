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
                "REGLA DE ORO: Si el usuario pregunta sobre conceptos científicos o tecnológicos "
                "(como computación cuántica), utiliza SIEMPRE la herramienta 'consultar_documento' de forma formal.\n"
                "NO expliques que vas a usar una herramienta. NO respondas con tus propios conocimientos.\n"
                "SIMPLEMENTE LLAMA A LA HERRAMIENTA."
            )
        },
        {'role': 'user', 'content': user_input}
    ]
    
    try:
        response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)
    except Exception as e:
        raise Exception(f"No se pudo conectar con Ollama (Modelo: {MODEL}). Error: {e}")

    if response.message.tool_calls:
        tool_call = response.message.tool_calls[0]
        name = tool_call.function.name
        args = tool_call.function.arguments
    else:
        # Fallback para modelos que responden con JSON en el contenido
        try:
            content = response.message.content.strip()
            # Si el contenido empieza con '{', intentamos parsearlo
            if content.startswith('{'):
                tool_data = json.loads(content)
                name = tool_data.get('name')
                args = tool_data.get('parameters', tool_data.get('arguments', {}))
                # Algunos modelos anidan los argumentos en 'object'
                if isinstance(args, dict) and 'object' in args:
                    try:
                        args = json.loads(args['object'])
                    except:
                        pass
            else:
                return response.message.content
        except:
            return response.message.content

    if name:
        messages.append(response.message)
        print(f"\n[Consultando base de conocimientos: {name}]")
        result = run_tool(name, args)
        messages.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
        
        try:
            final_response = ollama.chat(model=MODEL, messages=messages)
            return final_response.message.content
        except Exception as e:
            raise Exception(f"Error en la respuesta final de Ollama: {e}")
    
    return response.message.content
