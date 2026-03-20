import time
from orchestrator import chat_with_ollama
from tools_registry import get_tools_tree

def main():
    print("--- Ollama Local (Modo Conocimiento) ---")
    print(get_tools_tree())
    print("\nPrueba preguntando: '¿Qué es la descoherencia cuántica?'")
    print("Escribe 'salir' para terminar.\n")
    
    # Memoria de la conversación
    historial = [
        {
            'role': 'system',
            'content': (
                "Eres un agente de búsqueda que NO sabe nada de computación cuántica.\n"
                "TU PROTOCOLO:\n"
                "1. SIEMPRE debes llamar a 'consultar_documento' antes de responder temas técnicos.\n"
                "2. Está PROHIBIDO responder con tu memoria. Usa SOLO el contenido del archivo.\n"
                "3. Una vez que tengas la información, mantenla en memoria para preguntas de seguimiento."
            )
        }
    ]
    
    while True:
        try:
            user_input = input("Usuario: ")
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            break

        if user_input.lower() in ["salir", "exit", "quit"]:
            break
        
        if not user_input.strip():
            continue

        # Añadimos la pregunta del usuario al historial
        historial.append({'role': 'user', 'content': user_input})

        try:
            start_time = time.time()
            # Pasamos el historial completo al orquestador
            response = chat_with_ollama(historial)
            end_time = time.time()
            
            print(f"Ollama: {response}")
            print(f"Tiempo de respuesta: {end_time - start_time:.2f} segundos\n")
        except Exception as e:
            print(f"Error en la comunicación con Ollama: {e}\n")

if __name__ == "__main__":
    main()
