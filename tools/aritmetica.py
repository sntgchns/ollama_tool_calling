import math

class AritmeticaTools:
    """Clase para operaciones matemáticas básicas."""

    def sumar(self, a, b):
        return {"result": a + b}

    def restar(self, a, b):
        return {"result": a - b}

    def multiplicar(self, a, b):
        return {"result": a * b}

    def dividir(self, a, b):
        if b == 0:
            return {"error": "División por cero"}
        return {"result": a / b}

    def potencia(self, base, exponente):
        return {"result": math.pow(base, exponente)}

    def raiz_cuadrada(self, numero):
        if numero < 0:
            return {"error": "No se puede calcular raíz de un número negativo"}
        return {"result": math.sqrt(numero)}
