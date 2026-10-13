# Crédito con documentación contradictoria

Todos los timestamps de los documentos están en UTC. Entrenamiento histórico: 2025-07-15T00:00:00Z. Extracción: 2025-08-15T00:00:00Z. La disponibilidad exactamente en el instante de entrenamiento o predicción está permitida. La población de los tres registros es válida. Salvo diferencias explícitas en cada expediente, la predicción ocurrió el 2025-06-01T00:00:00Z y todas las features usadas estaban disponibles el 2025-05-31T18:00:00Z. La disponibilidad de un label requiere el valor certificado en el sistema de entrenamiento, no solo la ocurrencia del evento.

## Estado de los expedientes
Los tres outcomes son definitivos en la extracción, sin discrepancia sobre su valor ni certificación en ese momento. La fecha exacta de disponibilidad en el sistema de entrenamiento figura en documentos distintos. Las fuentes sin prioridad declarada tienen igual autoridad: no se presume que la más reciente sustituya a otra. Solo F2 tiene una resolución de autoridad explícita. La ventana es [1 de junio, 1 de julio).
## Documentos
- F1: positivo definitivo. Acta del almacén: primera disponibilidad el 10 de julio a las 08:00. Registro de publicación: primera disponibilidad el 20 de julio a las 08:00. No hay resolución ni prioridad entre esas dos fuentes.
- F2: positivo definitivo. Hoja antigua dice disponible el 20 de julio; resolución firmada declara errónea esa hoja y certifica primera disponibilidad el 10 de julio a las 08:00. El acta firmada tiene prioridad explícita.
- F3: negativo definitivo. Ambas fuentes concuerdan en primera disponibilidad el 20 de julio a las 08:00. Las bitácoras de una feature discrepan: una dice disponible el 31 de mayo a las 18:00 y otra el 2 de junio a las 08:00; ninguna tiene prioridad.
