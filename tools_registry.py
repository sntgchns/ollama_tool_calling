import os
from tools.sistema import SistemaTools
from tools.documentacion import consultar_documento

SISTEMA = SistemaTools()

TOOLS = [
    {'type': 'function', 'function': {'name': 'verificar_estado_servidor', 'description': 'Detecta códigos de error.', 'parameters': {'type': 'object', 'properties': {}}}},
    {'type': 'function', 'function': {'name': 'consultar_documento', 'description': 'Lee manuales (.md).', 'parameters': {'type': 'object', 'properties': {'nombre_archivo': {'type': 'string'}}, 'required': ['nombre_archivo']}}},
    {'type': 'function', 'function': {'name': 'ejecutar_reinicio_servicio', 'description': 'Reinicia servicios.', 'parameters': {'type': 'object', 'properties': {'servicio': {'type': 'string'}}, 'required': ['servicio']}}},
]

def get_tools_tree():
    tree = "Herramientas Disponibles (Modo Soporte Experto):\n"
    tree += "├── verificar_estado_servidor\n"
    tree += "├── consultar_documento\n"
    tree += "└── ejecutar_reinicio_servicio\n"
    tree += "\nConocimiento Disponible (Markdown):\n"
    tree += "└── conocimiento/guia_infraestructura.md"
    return tree

def run_tool(name, args):
    if name == "verificar_estado_servidor": return SISTEMA.verificar_estado_servidor()
    if name == "consultar_documento": 
        nombre_archivo = args.get('nombre_archivo', '') if isinstance(args, dict) else args
        return consultar_documento(nombre_archivo)
    if name == "ejecutar_reinicio_servicio": 
        servicio = args.get('servicio', '') if isinstance(args, dict) else args
        return SISTEMA.ejecutar_reinicio_servicio(servicio)
    return {"error": "TOOL_NOT_FOUND"}
