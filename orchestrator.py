import ollama
import json
from tools_registry import TOOLS, run_tool

MODEL = "qwen2.5:3b"

def chat_with_ollama(user_input):
    messages = [
        {
            'role': 'system',
            'content': (
                "Eres un asistente especializado en extraer información de una base de conocimientos técnica.\n"
                "REGLA DE ORO: Si necesitas información sobre conceptos científicos o tecnológicos "
                "(como computación cuántica), utiliza SIEMPRE la herramienta 'consultar_documento'.\n\n"
                "Una vez obtenida la información, utilízala para dar una respuesta clara y estructurada."
            )
        },
        {'role': 'user', 'content': user_input}
    ]
    
    response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)

    if response.message.tool_calls:
        messages.append(response.message)
        tool = response.message.tool_calls[0]
        name = tool.function.name
        args = tool.function.arguments
        print(f"\n[Consultando base de conocimientos: {name}]")
        result = run_tool(name, args)
        messages.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
        
        final_response = ollama.chat(model=MODEL, messages=messages)
        return final_response.message.content
    
    return response.message.content
