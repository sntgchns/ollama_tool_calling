import time
from orchestrator import chat_with_ollama
from tools_registry import get_tools_tree

def main():
    print("--- Ollama Local (Modo Soporte Experto) ---")
    print(get_tools_tree())
    print("\nPrueba: '¿Puedes revisar el servidor y arreglarlo?'")
    print("Escribe 'salir' para terminar.\n")
    
    # Memoria de la conversación
    historial = [
        {
            'role': 'system', 
            'content': (
                "Eres un Agente Experto de Soporte Técnico.\n"
                "TU MISIÓN: Solucionar problemas del servidor siguiendo un protocolo ESTRICTO.\n\n"
                "PASOS OBLIGATORIOS (UNO POR TURNO):\n"
                "1. Ejecuta 'verificar_estado_servidor' para obtener el código de error.\n"
                "2. Ejecuta 'consultar_documento' con nombre_archivo='guia_infraestructura' para buscar qué servicio corresponde al código de error.\n"
                "3. Ejecuta 'ejecutar_reinicio_servicio' con el nombre del servicio que encontraste.\n\n"
                "REGLAS CRÍTICAS:\n"
                "- NO adivines el error. DEBES verificarlo primero.\n"
                "- NO asumas el servicio. DEBES consultarlo en el manual.\n"
                "- NO des una respuesta final hasta que hayas completado los 3 pasos.\n"
                "- IMPORTANTE: Envía la respuesta final en lenguaje natural, sin bloques JSON."
            )
        }
    ]
    
    while True:
        try:
            user_input = input("Usuario: ")
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            break

        if user_input.lower() in ["salir", "exit", "quit"]: break
        
        if not user_input.strip():
            continue

        # Añadimos al historial
        historial.append({'role': 'user', 'content': user_input})

        try:
            # Pasamos historial completo
            response = chat_with_ollama(historial)
            print(f"Ollama: {response}\n")
        except Exception as e:
            print(f"Error en la comunicación con Ollama: {e}\n")

if __name__ == "__main__":
    main()
