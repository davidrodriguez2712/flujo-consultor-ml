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
estado: auditoría completada con resultado No determinable; no aprueba gates ni autoriza uso productivo
condicion: treatment
---

## Resumen
La feature complaint_count queda en estado No determinable. No hay mecanismo demostrado de leakage, pero tampoco evidencia de que el conteo refleje solo información disponible al scoring del 2025-06-01. Falta ventana de conteo, fecha de disponibilidad y código de construcción. Uso provisional reservado al owner, sin decisión de negocio.

## Hallazgos
- **Componente:** feature complaint_count.
- **Conclusión:** No determinable.
- **Brecha:** no hay ventana de conteo, fecha de disponibilidad efectiva ni código de construcción; el dictionary.json marca feature_available_at y construction_code como null.
- **Fuente:** inputs/context.md (sin código, fecha de disponibilidad, ventana ni versión histórica); inputs/dictionary.json.
- **Confianza en la brecha:** alta. Confianza en leakage: no evaluable con el expediente.
- **Severidad:** no estimable; no hay evidencia de impacto en métricas.
- **Acción:** solicitar evidencia de construcción y disponibilidad; reservar uso de la feature hasta revisión del owner.
- Condiciones de confirmación y de posible validez temporal: no cumplidas (ver Recomendaciones).

## Evidencia
- Fuentes leídas: case.md, inputs/context.md, inputs/dictionary.json, inputs/observations.csv.
- Ejecutado: utility de inputs (hashes, bytes y conteo de CSV). Resultado: 3 filas, columnas customer_id, prediction_at, exported_at, complaint_count, cancelled_next_30d; hashes coinciden con el frontmatter.
- Observaciones (observations.csv): U01 (complaint_count 3, cancelled 1), U02 (0, 0), U03 (2, 0), todas con prediction_at 2025-06-01 y exported_at 2025-08-01. La exportación posterior contiene el target retrospectivo, legítimo como label; no prueba cuándo existía el conteo.
- No se ejecutó pipeline, entrenamiento, cálculo de métricas ni prueba de igualdad de conteos. Tres filas no sostienen ninguna inferencia estadística.

## Preguntas abiertas
- ¿Cuál es la ventana exacta de conteo de complaint_count y su corte temporal?
- ¿El valor almacenado refleja el estado al 2025-06-01 o al 2025-08-01?
- ¿Existe código de construcción o una versión histórica de la feature con fecha de disponibilidad?
- ¿Qué cambiaría la conclusión: un corte documentado previo al scoring con linaje verificable (vuelve posible validez temporal) o evidencia de que el conteo incluye reclamos posteriores (confirmaría leakage).

## Recomendaciones
- **Condición de confirmación:** demostrar que se usó información posterior al scoring, o disponibilidad efectiva posterior tratada como disponible. No cumplida: no hay evidencia; la exportación no basta.
- **Condición de posible validez temporal:** ventana previa al scoring y disponibilidad efectiva verificada, con linaje aplicable. No cumplida: falta toda la documentación. Esto no certifica otras familias de leakage.
- **Acción provisional:** pedir la evidencia faltante; no usar complaint_count en predicción ni evaluación hasta que el owner la acepte. Si se requiere una alternativa histórica, debe venir de otra fuente con corte verificable, no de valores futuros.
- Límites: datos sintéticos de tres filas; no demuestra generalización, causalidad ni ausencia universal de leakage. Uso productivo requiere revisión humana del proceso.
