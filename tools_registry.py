import subprocess
import json
import os
from tools.aritmetica import AritmeticaTools
from tools.geometria import GeometriaTools
from tools.conversor import ConversorTools
from tools.database import DatabaseTools

# Instanciar clases de herramientas una vez para mejorar eficiencia
ARITMETICA = AritmeticaTools()
GEOMETRIA = GeometriaTools()
CONVERSOR = ConversorTools()
DATABASE = DatabaseTools()

# Definición de herramientas para Ollama
TOOLS = [
    {
        'type': 'function',
        'function': {
            'name': 'sumar',
            'description': 'Suma dos números (a + b)',
            'parameters': {
                'type': 'object',
                'properties': {
                    'a': {'type': 'number'},
                    'b': {'type': 'number'},
                },
                'required': ['a', 'b'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'restar',
            'description': 'Resta dos números (a - b)',
            'parameters': {
                'type': 'object',
                'properties': {
                    'a': {'type': 'number'},
                    'b': {'type': 'number'},
                },
                'required': ['a', 'b'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'multiplicar',
            'description': 'Multiplica dos números (a * b)',
            'parameters': {
                'type': 'object',
                'properties': {
                    'a': {'type': 'number'},
                    'b': {'type': 'number'},
                },
                'required': ['a', 'b'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'dividir',
            'description': 'Divide dos números (a / b)',
            'parameters': {
                'type': 'object',
                'properties': {
                    'a': {'type': 'number'},
                    'b': {'type': 'number'},
                },
                'required': ['a', 'b'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'potencia',
            'description': 'Calcula la potencia de una base a un exponente',
            'parameters': {
                'type': 'object',
                'properties': {
                    'base': {'type': 'number'},
                    'exponente': {'type': 'number'},
                },
                'required': ['base', 'exponente'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'raiz_cuadrada',
            'description': 'Calcula la raíz cuadrada de un número',
            'parameters': {
                'type': 'object',
                'properties': {
                    'numero': {'type': 'number'},
                },
                'required': ['numero'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'convertir_base',
            'description': 'Convierte un número entre diferentes bases numéricas (Base 2, 10 o 16)',
            'parameters': {
                'type': 'object',
                'properties': {
                    'numero': {'type': 'string', 'description': 'El número o cadena a convertir (ej: "1010", "15", "0xff")'},
                    'base_origen': {'type': 'number', 'description': 'Base actual (2, 10 o 16)'},
                    'base_destino': {'type': 'number', 'description': 'Base a la que se desea convertir (2, 10 o 16)'},
                },
                'required': ['numero', 'base_origen', 'base_destino'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'area_cuadrado',
            'description': 'Calcula la superficie de un cuadrado dado su lado',
            'parameters': {
                'type': 'object',
                'properties': {
                    'lado': {'type': 'number'},
                },
                'required': ['lado'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'area_rectangulo',
            'description': 'Calcula la superficie de un rectángulo dada su base y altura',
            'parameters': {
                'type': 'object',
                'properties': {
                    'base': {'type': 'number'},
                    'altura': {'type': 'number'},
                },
                'required': ['base', 'altura'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'area_triangulo',
            'description': 'Calcula la superficie de un triángulo dada su base y altura',
            'parameters': {
                'type': 'object',
                'properties': {
                    'base': {'type': 'number'},
                    'altura': {'type': 'number'},
                },
                'required': ['base', 'altura'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'area_circulo',
            'description': 'Calcula la superficie de un círculo dado su radio',
            'parameters': {
                'type': 'object',
                'properties': {
                    'radio': {'type': 'number'},
                },
                'required': ['radio'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'consultar_db',
            'description': 'Consulta información de un pedido por su ID',
            'parameters': {
                'type': 'object',
                'properties': {
                    'id_pedido': {'type': 'string'},
                },
                'required': ['id_pedido'],
            },
        },
    },
]

def get_tools_tree():
    """Devuelve una representación visual de las herramientas disponibles."""
    instancias = {
        "Aritmética": ARITMETICA,
        "Geometría": GEOMETRIA,
        "Conversor": CONVERSOR,
        "Database": DATABASE
    }
    
    tree = "Herramientas Disponibles (Modo Algorítmico):\n"
    for categoria, instancia in instancias.items():
        tree += f"├── {categoria}\n"
        # Listar métodos públicos de la clase
        metodos = [m for m in dir(instancia) if not m.startswith('_')]
        for i, metodo in enumerate(metodos):
            prefijo = "│   ├──" if i < len(metodos) - 1 else "│   └──"
            tree += f"{prefijo} {metodo}\n"
    
    tree += "\nConocimiento Disponible:\n"
    tree += "└── Lógica Interna y Funciones Algorítmicas"
    return tree

def run_tool(name, args):
    """Ejecuta una herramienta basándose en el nombre de la función."""
    
    # Lista de instancias para buscar el método
    instancias = [ARITMETICA, GEOMETRIA, CONVERSOR, DATABASE]
    
    for instancia in instancias:
        if hasattr(instancia, name):
            try:
                method = getattr(instancia, name)
                return method(**args)
            except Exception as e:
                return {"error": f"Error ejecutando {name} en {instancia.__class__.__name__}: {str(e)}"}

    # Scripts externos individuales (si quedara alguno)
    script_path = os.path.join("tools", f"{name}.py")
    if os.path.exists(script_path):
        cmd_args = [str(v) for v in args.values()]
        try:
            result = subprocess.run(
                ["python3", script_path] + cmd_args,
                capture_output=True,
                text=True
            )
            return json.loads(result.stdout)
        except Exception as e:
            return {"error": f"Error ejecutando script {name}: {str(e)}"}
            
    return {"error": "TOOL_NOT_FOUND"}
