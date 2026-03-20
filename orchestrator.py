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
                "Estás en el MODO CONOCIMIENTO (Rama: feature/markdown).\n"
                "Tu propósito educativo es demostrar la 'Recuperación Dinámica de Conocimiento' (RAG).\n\n"
                "HERRAMIENTA PERMITIDA: Solo 'consultar_documento'.\n"
                "REGLA: Si el usuario pide cálculos matemáticos o acciones de sistema, explícale que en este "
                "paso del tutorial solo puedes leer archivos Markdown, y que debe cambiar a 'feature/tools' "
                "o 'feature/expert' para ver otras funcionalidades."
            )
        },
        {'role': 'user', 'content': user_input}
    ]
    
    for _ in range(5):
        try:
            response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)
        except Exception as e:
            raise Exception(f"No se pudo conectar con Ollama: {e}")

        name, args = None, None
        
        # 1. Intentar obtener llamada formal
        if response.message.tool_calls:
            tool_call = response.message.tool_calls[0]
            name = tool_call.function.name
            args = tool_call.function.arguments
            messages.append(response.message)
        else:
            # 2. Fallback robusto con Regex
            try:
                content = response.message.content.strip()
                if '{' in content:
                    name_match = re.search(r'"name":\s*"([^"]+)"', content)
                    if name_match:
                        name = name_match.group(1)
                        # Buscamos nombre_archivo en el texto si no hay JSON limpio
                        file_match = re.search(r'"nombre_archivo":\s*"([^"]+)"', content)
                        args = {'nombre_archivo': file_match.group(1)} if file_match else {}
                    
                    if name:
                        fake_message = {
                            'role': 'assistant',
                            'content': f"Intentando ejecutar '{name}'...",
                            'tool_calls': [{'function': {'name': name, 'arguments': args}}]
                        }
                        messages.append(fake_message)
                else:
                    return re.sub(r'\{.*\}', '', response.message.content).strip()
            except:
                return response.message.content

        if name:
            # Ejecutamos la herramienta (si no existe, devolverá el error educativo)
            result = run_tool(name, args)
            messages.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
            # El loop sigue para que el modelo nos dé el mensaje final educativo
        else:
            return re.sub(r'\{.*\}', '', response.message.content).strip()
            
    return "Se alcanzó el límite de pasos sin una respuesta final."
