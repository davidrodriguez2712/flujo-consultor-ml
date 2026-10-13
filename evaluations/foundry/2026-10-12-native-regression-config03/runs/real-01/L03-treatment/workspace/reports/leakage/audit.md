---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-12
inputs:
  - path: case.md
    sha256: db7f2572bc7e591a8d537735dade9cdbcc1da74a100ecb2dd245673b3540e951
  - path: inputs/context.md
    sha256: ae79d0d67bdd4f71349d51644732c99ae1ce547ad618a6d663a30195042b1c7e
  - path: inputs/dictionary.json
    sha256: 72636cf89cf406c70e90c0c1325ddcb7c89229a915199153c35c9f167c414fe3
  - path: inputs/observations.csv
    sha256: 32ae7c42472e440093583da2798aba677eb2ceae58289e5d5dc77f3e46354532
estado: auditoría completada con preguntas abiertas; no aprueba gates
condicion: treatment
---

## Resumen
La feature complaint_count no puede considerarse válida para scoring al 2025-06-01 con la evidencia del expediente. Su ventana, fecha de disponibilidad y código de construcción no están documentados, y la exportación es posterior al scoring (2025-08-01). No se confirma leakage; el riesgo es alto y no determinable con lo disponible.

## Hallazgos
1. **complaint_count — riesgo de información posterior al scoring.**
   - Componente: feature complaint_count (inputs/dictionary.json, inputs/context.md).
   - Mecanismo: el conteo podría reflejar el estado al exportar (2025-08-01), no al scoring (2025-06-01). Context.md indica que no se conoce cuál.
   - Fuente: inputs/context.md; inputs/dictionary.json (feature_available_at y construction_code en null).
   - Confianza: media.
   - Severidad: alta.
   - Acción: no usar en scoring hasta documentar ventana, corte y disponibilidad; retirar si el conteo es intrínsecamente posterior.
2. **Señal perfecta o igualdad feature-target: no determinable.** En tres filas (U01: 3 reclamos/cancela=1; U02: 0/0; U03: 2/0) no hay patrón concluyente. Tamaño de muestra insuficiente; no es prueba de ausencia de leakage.

## Evidencia
- Lectura de case.md, inputs/context.md, inputs/dictionary.json e inputs/observations.csv.
- Ejecución de la utility autorizada check_inputs.py: hashes y tamaños de los cuatro archivos; observations.csv con 3 filas y columnas customer_id, prediction_at, exported_at, complaint_count, cancelled_next_30d.
- Observado: prediction_at = 2025-06-01T00:00:00Z; exported_at = 2025-08-01T00:00:00Z en todas las filas.
- Skill detect-leakage 0.2.0 cargada vía Skill antes de auditar.
- No ejecutado: pipeline, entrenamiento, joins, splits, cross-validation, preprocessing (no hay código en el expediente).

## Preguntas abiertas
- ¿complaint_count refleja el estado al 2025-06-01 o al 2025-08-01?
- ¿Cuál es la ventana de conteo (p. ej., 30 días previos al scoring)?
- ¿Cuándo estuvo disponible la feature en producción (feature_available_at)?
- ¿Existe código de construcción para verificar el corte temporal?
- ¿Hay versión histórica de la feature con corte verificable?
- Qué cambiaría la conclusión: evidencia de corte ≤ 2025-06-01 con ventana previa documentada reduciría el riesgo; un conteo con fecha de exportación lo confirmaría como leakage.

## Recomendaciones
- Solicitar al owner de datos la ventana, la fecha de disponibilidad y el código de construcción de complaint_count.
- Mientras tanto, excluir complaint_count del scoring; puede conservarse solo para evaluación retrospectiva.
- Si se reconstruye histórica, hacerlo con fuente y corte verificables, y repetir esta auditoría.
- Revisión humana del proceso de construcción sigue siendo necesaria. Esta auditoría no demuestra generalización ni ausencia universal de leakage.
