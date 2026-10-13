---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-13
modo: guia_textual
estado: parcial_no_concluyente
inputs: context.md, dictionary.json, observations.csv
---

## Resumen

No recomendar hoy usar `complaint_count` para scoring. El expediente no permite confirmar que el conteo existiera al scoring (2025-06-01) ni que cubra solo reclamos anteriores a esa fecha. La exportación es posterior (2025-08-01), por lo que el valor podría incluir reclamos ocurridos después del scoring.

## Hallazgos

1. **Riesgo alto, disponibilidad no determinable:** `feature_available_at` es null y la ventana de conteo no está documentada. Mecanismo posible: target leakage por conteo posterior al scoring. Fuente: dictionary.json. Confianza: media. Severidad: alta. Acción: bloquear uso hasta documentar disponibilidad.
2. **Sin código de construcción:** `construction_code` es null; no se puede verificar la lógica del conteo. Severidad: alta.

## Evidencia

Lectura de metadatos (no ejecutada): `exported_at` (2025-08-01) es posterior a `prediction_at` (2025-06-01) en las tres filas. Las filas U01 (3 reclamos, cancelación 1), U02 (0, 0) y U03 (2, 0) no bastan para estimar relación ni validar generalización. Comprobaciones pendientes: ventana, versión histórica, orden temporal de eventos y split.

## Preguntas abiertas

- ¿Cuándo estaba disponible el conteo en producción?
- ¿Qué ventana cubre el conteo y termina antes de 2025-06-01?
- ¿Existe historia de reclamos versionada al scoring?
- ¿Cuál es el código de construcción?

## Recomendaciones

- No usar `complaint_count` para scoring hasta cerrar las preguntas anteriores.
- Evidencia que cambiaría la conclusión: código que filtre eventos con timestamp ≤ 2025-06-01, `feature_available_at` documentado ≤ prediction_at, y una extracción histórica con corte verificable.