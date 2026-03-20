from orchestrator import chat_with_ollama

def main():
    print("--- Ollama Local (Modo Solo Modelo) ---")
    print("Herramientas Disponibles:")
    print("└── Ninguna (Razonamiento puro)\n")
    print("Conocimiento Disponible:")
    print("└── Interno del Modelo (Pre-entrenamiento)\n")
    print("Prueba preguntando cualquier cosa. El modelo responderá sin usar herramientas externas.")
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
