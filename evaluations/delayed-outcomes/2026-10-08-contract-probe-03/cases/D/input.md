# Crédito con registros tardíos

Todos los timestamps de los documentos están en UTC. Entrenamiento histórico: 2025-07-15T00:00:00Z. Extracción: 2025-08-15T00:00:00Z. La disponibilidad exactamente en el instante de entrenamiento o predicción está permitida. La población de los tres registros es válida. Salvo diferencias explícitas en cada expediente, la predicción ocurrió el 2025-06-01T00:00:00Z y todas las features usadas estaban disponibles el 2025-05-31T18:00:00Z. La disponibilidad de un label requiere el valor certificado en el sistema de entrenamiento, no solo la ocurrencia del evento.

## Diccionario de riesgo
Target=1 indica entrar en mora de 30 días durante [1 de junio, 1 de julio). La mora de 30 días es irreversible para este target aunque después se pague. El supervisor debe certificar el evento, y el label solo está disponible al publicarse esa certificación en el almacén usado por entrenamiento. La fecha de entrada en mora no es la fecha de publicación. Para un negativo, el acta final certifica ausencia de mora en la ventana y también debe publicarse.
## Expedientes del supervisor y almacén
- D1: entrada en mora el 25 de junio; certificación firmada el 28 de junio; publicación en almacén el 18 de julio a las 06:00. Extracto target=1.
- D2: entrada en mora el 22 de junio; certificación y publicación el 24 de junio a las 06:00. Extracto target=1.
- D3: sin mora en toda la ventana; acta final negativa firmada el 2 de julio, publicada el 9 de julio a las 06:00. Extracto target=0.
