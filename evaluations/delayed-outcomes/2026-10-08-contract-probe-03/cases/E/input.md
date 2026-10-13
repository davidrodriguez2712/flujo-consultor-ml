# Crédito con features reconstruidas

Todos los timestamps de los documentos están en UTC. Entrenamiento histórico: 2025-07-15T00:00:00Z. Extracción: 2025-08-15T00:00:00Z. La disponibilidad exactamente en el instante de entrenamiento o predicción está permitida. La población de los tres registros es válida. Salvo diferencias explícitas en cada expediente, la predicción ocurrió el 2025-06-01T00:00:00Z y todas las features usadas estaban disponibles el 2025-05-31T18:00:00Z. La disponibilidad de un label requiere el valor certificado en el sistema de entrenamiento, no solo la ocurrencia del evento.

## Acta común
Los tres labels son negativos definitivos para [1 de junio, 1 de julio), publicados y certificados el 5 de julio a las 08:00. El máximo de disponibilidad de features indicado en el contexto general queda reemplazado por los registros siguientes. Todas las demás features estaban disponibles al predecir. El modelo se habría puntuado el 1 de junio a las 00:00.
## Diccionario del export y bitácora
- E1: saldo_historico tiene fecha_referencia=31 de mayo. El valor exportado se reconstruyó y estuvo disponible por primera vez el 2 de junio a las 08:00, incorporando una corrección recibida ese día. Esa es la feature usada; no se usa una versión anterior.
- E2: saldo_historico con fecha_referencia=31 de mayo. Una captura archivada prueba que el mismo valor exportado ya estaba disponible el 31 de mayo a las 18:00.
- E3: saldo_historico con fecha_referencia=31 de mayo. No se conserva historial ni captura y el equipo desconoce cuándo estuvo disponible el valor exportado.
