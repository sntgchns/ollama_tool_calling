import time
from orchestrator import chat_with_ollama
from tools_registry import get_tools_tree

def main():
    print("--- Ollama Local (Modo Algorítmico) ---")
    print(get_tools_tree())
    print("\nPrueba preguntando: '¿Cuánto es 123 * 456?' o 'Área de un círculo de radio 5'")
    print("Escribe 'salir' para terminar.\n")
    
    # Memoria de la conversación
    historial = [
        {
            'role': 'system', 
            'content': (
                "Eres un asistente matemático experto.\n"
                "REGLA DE ORO: Si usas una herramienta, DEBES incluir los números en el JSON.\n"
                "REGLA 2: El resultado de la herramienta es la VERDAD ABSOLUTA.\n"
                "REGLA 3: Mantén el contexto de los cálculos anteriores para responder preguntas de seguimiento."
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

        # Añadimos la pregunta al historial
        historial.append({'role': 'user', 'content': user_input})

        try:
            start_time = time.time()
            # Pasamos el historial completo
            response = chat_with_ollama(historial)
            end_time = time.time()
            
            print(f"Ollama: {response}")
            print(f"Tiempo de respuesta: {end_time - start_time:.2f} segundos\n")
        except Exception as e:
            print(f"Error en la comunicación con Ollama: {e}\n")

if __name__ == "__main__":
    main()
