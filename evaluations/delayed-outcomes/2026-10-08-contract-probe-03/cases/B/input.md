# Churn con actualización retrospectiva

Todos los timestamps de los documentos están en UTC. Entrenamiento histórico: 2025-07-15T00:00:00Z. Extracción: 2025-08-15T00:00:00Z. La disponibilidad exactamente en el instante de entrenamiento o predicción está permitida. La población de los tres registros es válida. Salvo diferencias explícitas en cada expediente, la predicción ocurrió el 2025-06-01T00:00:00Z y todas las features usadas estaban disponibles el 2025-05-31T18:00:00Z. La disponibilidad de un label requiere el valor certificado en el sistema de entrenamiento, no solo la ocurrencia del evento.

## Extracto del equipo de datos
El CSV actual reemplaza valores anteriores y conserva fecha_evento como fecha del negocio. Eso no demuestra cuándo el label estuvo en el sistema. La ventana objetivo es [1 de junio, 1 de julio). Para las filas B1 y B2, Auditoría certificó definitivamente el resultado de esa ventana en las fechas descritas; la versión actual se publicó en el sistema ese mismo instante. No existen otros canales de publicación para esos labels.
## Registro de cambios y tickets
- B1: CSV actual churn=1, fecha_evento=20 de junio. El ticket indica: primera certificación y publicación del positivo el 5 de agosto a las 09:00; antes era un flag sin resolver.
- B2: CSV actual churn=0. Ticket cerrado: ausencia de churn certificada y publicada el 10 de julio a las 09:00, sin revisiones posteriores.
- B3: CSV actual churn=0, fecha_evento vacía. El export no incluye certificación, ticket ni historial de publicación; no se documentó la regla que produce este cero.
