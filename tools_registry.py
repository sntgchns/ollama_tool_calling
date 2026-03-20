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
    if name == "consultar_documento":
        return consultar_documento(**args)
    return {"error": "TOOL_NOT_FOUND (Esta rama solo permite 'consultar_documento')"}
