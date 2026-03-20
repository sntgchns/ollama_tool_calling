import math

class GeometriaTools:
    """Clase para cálculos geométricos como superficies."""

    def area_cuadrado(self, lado):
        return {"result": lado * lado}

    def area_rectangulo(self, base, altura):
        return {"result": base * altura}

    def area_triangulo(self, base, altura):
        return {"result": (base * altura) / 2}

    def area_circulo(self, radio):
        return {"result": math.pi * (radio ** 2)}
