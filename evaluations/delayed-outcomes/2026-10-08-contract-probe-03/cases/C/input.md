# Retención con seguimiento incompleto

Todos los timestamps de los documentos están en UTC. Entrenamiento histórico: 2025-07-15T00:00:00Z. Extracción: 2025-08-15T00:00:00Z. La disponibilidad exactamente en el instante de entrenamiento o predicción está permitida. La población de los tres registros es válida. Salvo diferencias explícitas en cada expediente, la predicción ocurrió el 2025-06-01T00:00:00Z y todas las features usadas estaban disponibles el 2025-05-31T18:00:00Z. La disponibilidad de un label requiere el valor certificado en el sistema de entrenamiento, no solo la ocurrencia del evento.

## Definición acordada del target
churn=1 es pérdida del servicio durante la ventana; churn=0 es no perderlo. Para el negativo se requiere seguimiento completo de toda la ventana y un acta de conciliación. La publicación de esa acta certifica el negativo y lo hace disponible. Un cero en un expediente todavía abierto es un valor provisional. En esta muestra no se registraron eventos positivos ni pérdida de seguimiento distinta de la ventana aún abierta.
## Actas y expedientes
- C1: ventana [1 de junio, 1 de julio), seguimiento completo; acta negativa publicada el 5 de julio a las 08:00. CSV churn=0.
- C2: ventana [1 de junio, 1 de septiembre), seguimiento aún en curso al extraer; acta prevista no antes del cierre. CSV churn=0.
- C3: ventana [1 de junio, 1 de julio), seguimiento completo; acta negativa publicada el 20 de julio a las 08:00. CSV churn=0.
