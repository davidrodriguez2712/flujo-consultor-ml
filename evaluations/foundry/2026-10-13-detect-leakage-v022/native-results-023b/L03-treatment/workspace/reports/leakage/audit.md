---
skill: detect-leakage
version: 0.2.3
fecha: 2026-10-13
inputs:
  - path: case.md
    sha256: db7f2572bc7e591a8d537735dade9cdbcc1da74a100ecb2dd245673b3540e951
  - path: inputs/context.md
    sha256: ae79d0d67bdd4f71349d51644732c99ae1ce547ad618a6d663a30195042b1c7e
  - path: inputs/dictionary.json
    sha256: 72636cf89cf406c70e90c0c1325ddcb7c89229a915199153c35c9f167c414fe3
  - path: inputs/observations.csv
    sha256: 32ae7c42472e440093583da2798aba677eb2ceae58289e5d5dc77f3e46354532
estado: auditoría con brecha abierta (No determinable); no aprobada; sin gates aceptados
condicion: treatment
---

## Resumen
Para la feature complaint_count, el resultado es No determinable. El expediente no demuestra información posterior usada ilegítimamente, ni demuestra que el conteo estuviera disponible al scoring del 2025-06-01. La exportación del 2025-08-01 no satisface ninguna de las dos condiciones. Uso provisional: reservado bajo autoridad del owner hasta recibir evidencia de disponibilidad.

## Hallazgos
1. **Componente:** feature complaint_count (ventana, disponibilidad y construcción).
   - **Conclusión:** No determinable.
   - **Brecha:** no existe fecha de disponibilidad (`feature_available_at: null`), código de construcción (`construction_code: null`) ni ventana de conteo; el diccionario declara "ventana y disponibilidad no documentadas" (`inputs/dictionary.json`). Context indica que no se sabe si el conteo refleja el estado al scoring o al exportar (`inputs/context.md`).
   - **Fuente:** inputs/context.md; inputs/dictionary.json; inputs/observations.csv (3 filas, todas con prediction_at 2025-06-01 y exported_at 2025-08-01).
   - **Confianza en la brecha:** alta. Confianza en leakage: no evaluable.
   - **Severidad:** no estimable; no hay evidencia de impacto ni de tamaño de población (3 filas sintéticas).
   - **Acción propuesta:** aplicar las condiciones de Recomendaciones; no tratar la feature como válida ni como inválida.

## Evidencia
- Hashes y conteos: utility `.runtime/check_inputs.py` ejecutada una vez. Confirmó los cuatro inputs, sus tamaños y columnas (customer_id, prediction_at, exported_at, complaint_count, cancelled_next_30d) y 3 filas en observations.csv.
- Lectura directa de inputs/context.md, inputs/dictionary.json e inputs/observations.csv.
- Skill detect-leakage 0.2.3 cargada mediante Skill antes de auditar.
- Observaciones válidas: el target cancelled_next_30d es un outcome retrospectivo legítimo y no se trata como feature. IDs, fechas y target son metadata.
- Límites de inspección: no se ejecutó pipeline.py, no hubo joins, split, preprocessing ni CV, y no se entrenó nada. No se leyó código de construcción porque no existe en el expediente. No se leyó plugin.json. Ningún check de linaje temporal se ejecutó más allá de comparar timestamps de las filas.

## Preguntas abiertas
- ¿Cuándo existía complaint_count en producción respecto al scoring del 2025-06-01?
- ¿Cuál es la ventana de conteo (por ejemplo, reclamos previos al scoring o acumulados hasta la extracción)?
- ¿Existe un corte o versión histórica del conteo con timestamp verificable al scoring?
- ¿Cuál es el código de construcción y el linaje de la tabla de reclamos?
- ¿Quién es el owner que acepta la definición de la feature?

## Recomendaciones
- **Condición de confirmación (no cumplida):** demostrar que se usó información posterior al scoring, o que una disponibilidad posterior se trató como disponible al scoring. Requeriría evidencia de construcción o eventos posteriores.
- **Condición de posible validez temporal (no cumplida):** ventana previa al scoring y disponibilidad efectiva al scoring, con linaje verificable. Esto no certifica otras familias de leakage.
- **Acción provisional:** pedir la evidencia de disponibilidad, ventana y código de construcción. Mantener el uso de complaint_count reservado bajo autoridad del owner.
- Si no existe un corte histórico verificable, retirar la feature o sustituirla por una alternativa con corte documentado, sin adelantar valores futuros.
- Revisión humana del proceso antes de cualquier uso productivo. Esta auditoría no certifica predictor ni generalización.
