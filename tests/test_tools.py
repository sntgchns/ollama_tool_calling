import unittest
import subprocess
import json
import os
from tools_registry import run_tool

class TestTools(unittest.TestCase):
    # Tests para la nueva clase Calculadora (Llamadas directas optimizadas)
    def test_sumar(self):
        data = run_tool("sumar", {"a": 10, "b": 25})
        self.assertEqual(data["result"], 35)

    def test_restar(self):
        data = run_tool("restar", {"a": 50, "b": 20})
        self.assertEqual(data["result"], 30)

    def test_multiplicar(self):
        data = run_tool("multiplicar", {"a": 5, "b": 4})
        self.assertEqual(data["result"], 20)

    def test_dividir(self):
        data = run_tool("dividir", {"a": 10, "b": 2})
        self.assertEqual(data["result"], 5)

    def test_potencia(self):
        data = run_tool("potencia", {"base": 2, "exponente": 3})
        self.assertEqual(data["result"], 8)

    def test_raiz_cuadrada(self):
        data = run_tool("raiz_cuadrada", {"numero": 16})
        self.assertEqual(data["result"], 4)

    def test_convertir_decimal_a_hex(self):
        data = run_tool("convertir_base", {"numero": "255", "base_origen": 10, "base_destino": 16})
        self.assertEqual(data["result"], "0xff")

    def test_convertir_binario_a_decimal(self):
        data = run_tool("convertir_base", {"numero": "1010", "base_origen": 2, "base_destino": 10})
        self.assertEqual(data["result"], 10)

    def test_convertir_decimal_a_binario(self):
        data = run_tool("convertir_base", {"numero": "10", "base_origen": 10, "base_destino": 2})
        self.assertEqual(data["result"], "1010")

    def test_convertir_hex_a_binario_directo(self):
        # Prueba la conversión directa de Hex a Binario (antes requería 2 pasos)
        data = run_tool("convertir_base", {"numero": "0xff", "base_origen": 16, "base_destino": 2})
        self.assertEqual(data["result"], "11111111")

    # Tests para la nueva clase Geometria
    def test_area_cuadrado(self):
        data = run_tool("area_cuadrado", {"lado": 5})
        self.assertEqual(data["result"], 25)

    def test_area_rectangulo(self):
        data = run_tool("area_rectangulo", {"base": 10, "altura": 5})
        self.assertEqual(data["result"], 50)

    def test_area_triangulo(self):
        data = run_tool("area_triangulo", {"base": 10, "altura": 5})
        self.assertEqual(data["result"], 25)

    def test_area_circulo(self):
        import math
        data = run_tool("area_circulo", {"radio": 3})
        self.assertAlmostEqual(data["result"], math.pi * 9)

    # Test para herramientas de base de datos
    def test_consultar_db(self):
        data = run_tool("consultar_db", {"id_pedido": "12345"})
        self.assertEqual(data["status"], "Enviado")
        self.assertEqual(data["cliente"], "Juan Pérez")

if __name__ == "__main__":
    unittest.main()
