import ollama
from tools_registry import TOOLS, run_tool

MODEL = "qwen2.5:3b"

def chat_with_ollama(user_input):
    messages = [{'role': 'user', 'content': user_input}]
    response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)

    if response.message.tool_calls:
        messages.append(response.message)
        for tool in response.message.tool_calls:
            name = tool.function.name
            args = tool.function.arguments
            print(f"\n[Ejecutando herramienta: {name}]")
            result = run_tool(name, args)
            messages.append({'role': 'tool', 'content': str(result), 'name': name})
        
        final_response = ollama.chat(model=MODEL, messages=messages)
        return final_response.message.content
    
    return response.message.content
