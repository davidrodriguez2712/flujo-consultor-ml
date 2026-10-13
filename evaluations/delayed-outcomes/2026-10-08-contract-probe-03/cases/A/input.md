# Churn con cancelación reversible

Todos los timestamps de los documentos están en UTC. Entrenamiento histórico: 2025-07-15T00:00:00Z. Extracción: 2025-08-15T00:00:00Z. La disponibilidad exactamente en el instante de entrenamiento o predicción está permitida. La población de los tres registros es válida. Salvo diferencias explícitas en cada expediente, la predicción ocurrió el 2025-06-01T00:00:00Z y todas las features usadas estaban disponibles el 2025-05-31T18:00:00Z. La disponibilidad de un label requiere el valor certificado en el sistema de entrenamiento, no solo la ocurrencia del evento.

## Nota de Operaciones
En este servicio, una petición de baja puede retirarse durante siete periodos de 24 horas desde su recepción. Solo cuando vence ese plazo sin retirada se certifica churn=1 y el label entra al sistema de entrenamiento inmediatamente. La petición provisional no constituye churn definitivo. Para estos expedientes la predicción fue el 1 de julio a las 00:00 y las features estaban listas el 30 de junio a las 18:00. La ventana objetivo es [1 de julio, 15 de agosto). No hay retrasos adicionales ni otras bajas.
## Expedientes
- A1: petición recibida el 3 de julio a las 10:00. No se retiró. El extracto actual muestra churn=1.
- A2: petición recibida el 12 de julio a las 10:00. No se retiró. El extracto actual muestra churn=1.
- A3: petición recibida el 12 de agosto a las 10:00. Todavía no se retiró; el extracto muestra flag_baja=1 y expediente abierto.
