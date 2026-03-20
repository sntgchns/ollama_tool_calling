class ConversorTools:
    """Clase para conversiones universales entre bases numéricas (Decimal, Binario, Hexadecimal)."""

    def convertir_base(self, numero, base_origen, base_destino):
        """
        Convierte un número entre diferentes bases numéricas.
        :param numero: El número o cadena a convertir (ej: '10', '1010', '0xa')
        :param base_origen: Base actual del número (2, 10, 16)
        :param base_destino: Base a la que se desea convertir (2, 10, 16)
        """
        try:
            # 1. Convertir todo primero a Decimal (Base 10) como puente
            # int() puede manejar prefijos como '0x' si se le indica la base correcta
            num_str = str(numero).strip()
            
            # Limpiar prefijo 0x si viene de otra herramienta o del usuario
            if num_str.lower().startswith("0x") and int(base_origen) == 16:
                decimal = int(num_str, 16)
            else:
                decimal = int(num_str, int(base_origen))
            
            # 2. Convertir del puente Decimal a la base destino
            destino = int(base_destino)
            
            if destino == 10:
                return {"result": decimal}
            elif destino == 2:
                return {"result": bin(decimal)[2:]} # Quitar prefijo '0b'
            elif destino == 16:
                return {"result": hex(decimal)} # Mantenemos '0x' para claridad hexadecimal
            else:
                return {"error": f"Base destino {base_destino} no soportada (usar 2, 10 o 16)"}
                
        except ValueError:
            return {"error": f"El valor '{numero}' no es válido para la base {base_origen}"}
        except Exception as e:
            return {"error": f"Error en la conversión: {str(e)}"}
