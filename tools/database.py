class DatabaseTools:
    """Clase para interactuar con la base de datos de pedidos."""

    def __init__(self):
        # Mock de base de datos
        self._db = {
            "12345": {"status": "Enviado", "cliente": "Juan Pérez", "fecha": "2024-03-20"},
            "67890": {"status": "Pendiente", "cliente": "María López", "fecha": "2024-03-21"}
        }

    def consultar_db(self, id_pedido):
        return self._db.get(id_pedido, {"error": "Pedido no encontrado"})
