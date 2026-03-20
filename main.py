import time
from orchestrator import chat_with_ollama
from tools_registry import get_tools_tree

def main():
    print("--- Ollama Local (Modo Conocimiento) ---")
    print(get_tools_tree())
    print("\nPrueba preguntando: '¿Qué es la descoherencia cuántica?'")
    print("Escribe 'salir' para terminar.\n")
    
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

        try:
            start_time = time.time()
            response = chat_with_ollama(user_input)
            end_time = time.time()
            
            print(f"Ollama: {response}")
            print(f"Tiempo de respuesta: {end_time - start_time:.2f} segundos\n")
        except Exception as e:
            print(f"Error en la comunicación con Ollama: {e}\n")

if __name__ == "__main__":
    main()
