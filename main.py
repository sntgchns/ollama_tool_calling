from orchestrator import chat_with_ollama
from tools_registry import get_tools_tree

def main():
    print("--- Ollama Local (Modo Soporte Experto) ---")
    print(get_tools_tree())
    print("\nPrueba: '¿Puedes revisar el servidor y arreglarlo?'")
    print("Escribe 'salir' para terminar.\n")
    
    while True:
        user_input = input("Usuario: ")
        if user_input.lower() in ["salir", "exit", "quit"]: break
        try:
            print(f"Ollama: {chat_with_ollama(user_input)}\n")
        except Exception as e: print(f"Error: {e}\n")

if __name__ == "__main__": main()
