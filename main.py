from orchestrator import chat_with_ollama
from tools_registry import get_tools_tree

def main():
    print("--- Ollama Local con Herramientas (Scripts) ---")
    print(get_tools_tree())
    print("Escribe 'salir' para terminar.\n")
    
    while True:
        user_input = input("Usuario: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            break
        
        try:
            import time
            start_time = time.time()
            response = chat_with_ollama(user_input)
            end_time = time.time()
            
            print(f"Ollama: {response}")
            print(f"Tiempo de respuesta: {end_time - start_time:.2f} segundos\n")
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()
