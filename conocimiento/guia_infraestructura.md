# Manual de Operaciones de Infraestructura - Nivel 2

## Protocolo Obligatorio de Soporte Técnico
Ante cualquier reporte de incidencia, el agente de soporte **DEBE** seguir este orden estrictamente:
1.  **Verificar el Estado:** Usar `verificar_estado_servidor` para obtener el código de error exacto.
2.  **Consultar este Manual:** Buscar el código de error en la tabla de abajo para identificar el servicio afectado.
3.  **Ejecutar Reinicio:** Usar `ejecutar_reinicio_servicio` con el nombre técnico del servicio encontrado.

## Matriz de Errores y Servicios

| Código de Error | Causa Probable | Servicio a Reiniciar |
| :--- | :--- | :--- |
| **ERR_501** | El servidor Apache ha dejado de responder. | `apache2` |
| **ERR_404_DB** | La conexión con la base de datos MySQL ha fallado. | `mysql-proxy` |
| **ERR_SSH_99** | Falla en el túnel de seguridad SSH. | `sshd-tunnel` |
| **ERR_MEM_FULL** | El caché de Redis está saturado. | `redis-server` |

---
*Nota: No intente reiniciar otros servicios sin antes verificar el código de error.*
