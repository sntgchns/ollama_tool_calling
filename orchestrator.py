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
                "Eres un asistente matemático y de base de datos experto.\n"
                "PASOS:\n"
                "1. Si el usuario pide un cálculo o consulta, usa la herramienta adecuada.\n"
                "2. Recibe el resultado y úsalo para responder de forma natural.\n"
                "REGLA: NO inventes resultados. Usa siempre las herramientas si están disponibles."
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
            # 2. Fallback robusto con Regex para capturar JSON "sucio"
            try:
                content = response.message.content.strip()
                if '{' in content:
                    # Extraer el nombre de la función con Regex (Raw strings)
                    name_match = re.search(r'"name":\s*"([^"]+)"', content)
                    if name_match:
                        name = name_match.group(1)
                        # Intentamos capturar números en el JSON para los argumentos
                        nums = re.findall(r'"\w+":\s*([\d\.]+)', content)
                        if nums:
                            # Creamos un dict genérico con los números encontrados
                            args = {f"arg{i}": float(v) for i, v in enumerate(nums)}
                        else:
                            args = {}
                    
                    if name:
                        # Inyectamos mensaje formal para mantener la coherencia de la historia
                        fake_message = {
                            'role': 'assistant',
                            'content': f"Calculando {name}...",
                            'tool_calls': [{'function': {'name': name, 'arguments': args}}]
                        }
                        messages.append(fake_message)
                else:
                    # Si no hay JSON, es la respuesta final. Limpiamos posibles residuos.
                    final_text = re.sub(r'\{.*\}', '', response.message.content).strip()
                    return final_text
            except:
                return response.message.content

        if name:
            print(f"\n[Ejecutando herramienta: {name}]")
            result = run_tool(name, args)
            messages.append({'role': 'tool', 'content': json.dumps(result), 'name': name})
            # El loop continúa para que el modelo genere la respuesta final con el resultado
        else:
            # Respuesta final limpia de JSON
            return re.sub(r'\{.*\}', '', response.message.content).strip()

    return "Se alcanzó el límite de pasos sin una respuesta final."
