from orchestrator import chat_with_ollama
from tools_registry import get_tools_tree

def main():
    print("--- Ollama Local (Modo Soporte Experto) ---")
    print(get_tools_tree())
    print("\nPrueba: '¿Puedes revisar el servidor y arreglarlo?'")
    print("Escribe 'salir' para terminar.\n")
    
    while True:
        try:
            user_input = input("Usuario: ")
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            break

        if user_input.lower() in ["salir", "exit", "quit"]: break
        
        if not user_input.strip():
            continue

        try:
            print(f"Ollama: {chat_with_ollama(user_input)}\n")
        except Exception as e:
            print(f"Error en la comunicación con Ollama: {e}\n")

if __name__ == "__main__":
    main()
