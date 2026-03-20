import ollama
import json
from tools_registry import TOOLS, run_tool

MODEL = "qwen2.5:3b"

def chat_with_ollama(user_input):
    messages = [
        {
            'role': 'system',
            'content': (
                "Eres un asistente que resuelve problemas complejos paso a paso.\n"
                "REGLA DE ORO: Si necesitas usar varias herramientas, solicita SOLO LA PRIMERA.\n"
                "Cuando recibas el resultado, solicita la siguiente. NO intentes predecir resultados intermedios."
            )
        },
        {'role': 'user', 'content': user_input}
    ]
    
    max_intentos = 10
    for paso in range(max_intentos):
        response = ollama.chat(
            model=MODEL,
            messages=messages,
            tools=TOOLS
        )

        # Si el modelo no pide herramientas, es la respuesta final
        if not response.message.tool_calls:
            return response.message.content

        # MEMORIA DE PLAN Y EJECUCIÓN SECUENCIAL ESTRICTA
        # Si el modelo pide varias herramientas, detectamos que tiene un "plan"
        total_pedidas = len(response.message.tool_calls)
        if total_pedidas > 1:
            print(f"\n[Plan detectado: El modelo sugiere {total_pedidas} pasos. Ejecutando solo el primero para evitar errores.]")
        
        # Tomamos SOLO la primera herramienta (la única con argumentos fiables)
        tool = response.message.tool_calls[0]
        name = tool.function.name
        args = tool.function.arguments
        
        # Guardamos en el historial SOLO esta llamada (limpiando las alucinadas)
        messages.append({
            'role': 'assistant',
            'content': '',
            'tool_calls': [tool]
        })
        
        print(f"\n[Paso {paso + 1}] Ejecutando: {name}({args})")
        
        result = run_tool(name, args)
        print(f"[Resultado Real: {result}]")
        
        # Enviamos el resultado al modelo
        messages.append({
            'role': 'tool',
            'content': json.dumps(result),
            'name': name
        })
        
        # Si había más herramientas en el plan original, le damos una pista al modelo
        if total_pedidas > 1:
            messages.append({
                'role': 'user',
                'content': f"He ejecutado el primer paso ({name}). El resultado real es {result}. Ahora continúa con el siguiente paso de tu plan usando este valor real."
            })
            
    return "Error: Demasiados pasos de razonamiento."
