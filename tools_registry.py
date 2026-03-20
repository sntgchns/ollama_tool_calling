import os
from tools.sistema import SistemaTools
from tools.documentacion import consultar_documento

SISTEMA = SistemaTools()

TOOLS = [
    {'type': 'function', 'function': {'name': 'verificar_estado_servidor', 'description': 'Detecta códigos de error técnicos en el servidor.', 'parameters': {'type': 'object', 'properties': {}}}},
    {'type': 'function', 'function': {'name': 'consultar_documento', 'description': 'Lee manuales de infraestructura (.md) para buscar soluciones.', 'parameters': {'type': 'object', 'properties': {'nombre_archivo': {'type': 'string'}}, 'required': ['nombre_archivo']}}},
    {'type': 'function', 'function': {'name': 'ejecutar_reinicio_servicio', 'description': 'Reinicia un servicio específico del sistema.', 'parameters': {'type': 'object', 'properties': {'servicio': {'type': 'string'}}, 'required': ['servicio']}}},
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
    """Ejecuta una herramienta basándose en el nombre de la función."""
    name_normalized = name.replace("_", "").lower()
    
    if name_normalized == "verificarestadoservidor":
        return SISTEMA.verificar_estado_servidor()
        
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
        
    if name_normalized == "ejecutarreinicioservicio":
        servicio = ""
        if isinstance(args, dict):
            for key in ['servicio', 'name', 'service']:
                if key in args:
                    servicio = args[key]
                    break
            if not servicio and len(args) == 1:
                servicio = list(args.values())[0]
        else:
            servicio = args
        return SISTEMA.ejecutar_reinicio_servicio(servicio)
        
    return {"error": f"Herramienta '{name}' no encontrada"}
