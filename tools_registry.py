import os
from tools.documentacion import consultar_documento

TOOLS = [
    {
        'type': 'function',
        'function': {
            'name': 'consultar_documento',
            'description': 'Busca y lee información técnica o científica en la base de conocimientos (archivos Markdown). Úsalo para profundizar en conceptos específicos (como computación cuántica, IA o física).',
            'parameters': {
                'type': 'object',
                'properties': {
                    'nombre_archivo': {'type': 'string', 'description': 'El nombre del archivo .md (ej: "computacion_cuantica")'},
                },
                'required': ['nombre_archivo'],
            },
        },
    },
]

def get_tools_tree():
    """Devuelve una representación visual de las herramientas disponibles."""
    tree = "Herramientas Disponibles (Modo Conocimiento):\n"
    tree += "└── Documentación\n"
    tree += "    └── consultar_documento\n"
    tree += "\nConocimiento Disponible (Markdown):\n"
    tree += "└── conocimiento/computacion_cuantica.md"
    return tree

def run_tool(name, args):
    """Ejecuta una herramienta basándose en el nombre de la función."""
    # Normalizamos el nombre (Llama 3.2 a veces omite el guion bajo)
    name_normalized = name.replace("_", "").lower()
    
    if name_normalized == "consultardocumento":
        # Búsqueda agresiva de nombre_archivo
        nombre_archivo = ""
        if isinstance(args, dict):
            # Intentar varias claves posibles que el modelo podría inventar
            for key in ['nombre_archivo', 'archivo', 'doc', 'documento']:
                if key in args:
                    nombre_archivo = args[key]
                    break
            # Si sigue vacío pero hay un solo valor en el dict, lo tomamos
            if not nombre_archivo and len(args) == 1:
                nombre_archivo = list(args.values())[0]
        else:
            nombre_archivo = args
            
        return consultar_documento(nombre_archivo)
    
    return {"error": f"Herramienta '{name}' no encontrada"}
