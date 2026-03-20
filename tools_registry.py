import subprocess
import json
import os
from tools.aritmetica import AritmeticaTools
from tools.geometria import GeometriaTools
from tools.conversor import ConversorTools
from tools.database import DatabaseTools

# Instanciar clases de herramientas
ARITMETICA = AritmeticaTools()
GEOMETRIA = GeometriaTools()
CONVERSOR = ConversorTools()
DATABASE = DatabaseTools()

# Mapeo directo de herramientas
TOOL_MAPPING = {
    "sumar": ARITMETICA.sumar,
    "restar": ARITMETICA.restar,
    "multiplicar": ARITMETICA.multiplicar,
    "dividir": ARITMETICA.dividir,
    "potencia": ARITMETICA.potencia,
    "raizcuadrada": ARITMETICA.raiz_cuadrada,
    "convertirbase": CONVERSOR.convertir_base,
    "areacuadrado": GEOMETRIA.area_cuadrado,
    "arearectangulo": GEOMETRIA.area_rectangulo,
    "areatriangulo": GEOMETRIA.area_triangulo,
    "areacirculo": GEOMETRIA.area_circulo,
    "consultardb": DATABASE.consultar_db,
}

def run_tool(name, args):
    """Ejecuta una herramienta con extracción robusta de parámetros numéricos."""
    name_normalized = name.replace("_", "").lower()
    
    if name_normalized in TOOL_MAPPING:
        try:
            # Si args es un dict, intentamos extraer los valores numéricos
            if isinstance(args, dict):
                # Extraer todos los números del dict en orden
                numeros = [v for v in args.values() if isinstance(v, (int, float))]
                
                # Caso específico para raíz cuadrada (espera un 'x')
                if name_normalized == "raizcuadrada":
                    x = args.get('x', args.get('numero', numeros[0] if numeros else 0))
                    return ARITMETICA.raiz_cuadrada(x)
                
                # Caso para ID de pedido (string)
                if name_normalized == "consultardb":
                    id_p = args.get('id_pedido', list(args.values())[0] if args else "")
                    return DATABASE.consultar_db(id_p)

                # Para el resto, pasamos los argumentos tal cual o los números encontrados
                if not args and numeros:
                    return TOOL_MAPPING[name_normalized](*numeros)
                return TOOL_MAPPING[name_normalized](**args)
            
            return TOOL_MAPPING[name_normalized](args)
        except Exception as e:
            return {"error": f"Error en {name}: {str(e)}"}
            
    return {"error": f"Herramienta '{name}' no encontrada"}

def get_tools_tree():
    """Devuelve una representación visual de las herramientas disponibles."""
    instancias = {"Aritmética": ARITMETICA, "Geometría": GEOMETRIA, "Conversor": CONVERSOR, "Database": DATABASE}
    tree = "Herramientas Disponibles (Modo Algorítmico):\n"
    for categoria, instancia in instancias.items():
        tree += f"├── {categoria}\n"
        metodos = [m for m in dir(instancia) if not m.startswith('_')]
        for i, metodo in enumerate(metodos):
            prefijo = "│   ├──" if i < len(metodos) - 1 else "│   └──"
            tree += f"{prefijo} {metodo}\n"
    tree += "\nConocimiento Disponible:\n└── Lógica Interna y Funciones Algorítmicas"
    return tree
