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
    tree = "--- MODO CONOCIMIENTO (Rama: feature/markdown) ---\n"
    tree += "Herramientas Disponibles:\n"
    tree += "└── Documentación\n"
    tree += "    └── consultar_documento\n"
    tree += "\nConocimiento Disponible (Markdown):\n"
    tree += "└── conocimiento/computacion_cuantica.md\n"
    tree += "\nNOTA: Para cálculos matemáticos, usa la rama 'feature/tools'."
    return tree

def run_tool(name, args):
    """Ejecuta una herramienta basándose en el nombre de la función."""
    name_normalized = name.replace("_", "").lower()
    
    if name_normalized == "consultardocumento":
        nombre_archivo = ""
        if isinstance(args, dict):
            for key in ['nombre_archivo', 'archivo', 'doc']:
                if key in args:
                    nombre_archivo = args[key]
                    break
            if not nombre_archivo and len(args) == 1:
                nombre_archivo = list(args.values())[0]
        else:
            nombre_archivo = args
        return consultar_documento(nombre_archivo)
    
    # Error educativo si alucina herramientas de otras ramas
    return {
        "error": f"La herramienta '{name}' NO está disponible en esta rama (feature/markdown). "
                 f"Este es el 'Modo Conocimiento'. Para usar funciones matemáticas como '{name}', "
                 f"debes cambiar a la rama 'feature/tools' usando: git checkout feature/tools"
    }
