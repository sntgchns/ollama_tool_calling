import ollama, json
from tools_registry import TOOLS, run_tool

MODEL = "qwen2.5:3b"

def chat_with_ollama(user_input):
    messages = [
        {'role': 'system', 'content': "Agente Experto. Pasos: 1. verificar_estado_servidor. 2. consultar_documento('guia_infraestructura'). 3. ejecutar_reinicio_servicio. Una tool por turno."}
    ]
    messages.append({'role': 'user', 'content': user_input})
    
    for _ in range(10):
        response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)
        if not response.message.tool_calls: return response.message.content
        
        tool = response.message.tool_calls[0]
        messages.append({'role': 'assistant', 'content': '', 'tool_calls': [tool]})
        print(f"\n[Ejecutando: {tool.function.name}]")
        result = run_tool(tool.function.name, tool.function.arguments)
        messages.append({'role': 'tool', 'content': json.dumps(result), 'name': tool.function.name})
    return "Error."
