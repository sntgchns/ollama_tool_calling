import ollama

MODEL = "qwen2.5:3b"

def chat_with_ollama(user_input):
    messages = [{'role': 'user', 'content': user_input}]
    
    # Llamada simple a Ollama sin herramientas
    response = ollama.chat(
        model=MODEL,
        messages=messages
    )

    return response.message.content
