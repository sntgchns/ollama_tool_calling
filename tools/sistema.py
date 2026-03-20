import random
class SistemaTools:
    def verificar_estado_servidor(self):
        return {'estado': 'ERR_501', 'mensaje': 'Alerta: ERR_501'}
    def ejecutar_reinicio_servicio(self, servicio: str):
        return {'resultado': 'EXITO', 'mensaje': f'Servicio {servicio} reiniciado.'}