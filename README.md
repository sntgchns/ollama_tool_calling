# Ollama Local con Llamadas a Herramientas Externas (Python)

Este proyecto muestra cómo integrar **Ollama** con scripts externos. El modelo detecta cuándo se necesita una función, el orquestador ejecuta el script correspondiente y devuelve el resultado al modelo para generar la respuesta final.

## Estructura del Proyecto

```text
.
├── main.py                 # Punto de entrada (CLI)
├── orchestrator.py         # Lógica de detección y loop con Ollama
├── tools_registry.py       # Manifiesto y ejecución de scripts
├── requirements.txt        # Dependencias (ollama, pytest)
├── tools/                  # Carpeta con scripts independientes
│   ├── sumar.py
│   └── consultar_db.py
└── tests/                  # Tests unitarios
    └── test_tools.py
```

## Requisitos

1.  **Ollama instalado** y corriendo localmente.
2.  Tener el modelo **llama3.1** (o similar que soporte tool calling) descargado:
    ```bash
    ollama pull llama3.1
    ```
3.  **Python 3.10+** instalado.

## Instalación

1.  Crea un entorno virtual (opcional):
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/Mac
    ```
2.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Ejecución

Corre el servicio interactivo:
```bash
python main.py
```

### Ejemplos de uso
-   "¿Cuánto es 123 + 456?" (Llamará a `sumar.py`)
-   "¿En qué estado está mi pedido 12345?" (Llamará a `consultar_db.py`)
-   "Hola, ¿cómo estás?" (Respuesta normal, sin herramientas)

## Tests

Verifica que los scripts de herramientas funcionan correctamente:
```bash
python -m unittest tests/test_tools.py
```
