---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-13
modo: guia_textual
estado: no_concluyente_bloqueado
inputs: context.md, dictionary.json, observations.csv
---

## Resumen

No recomendaría usar complaint_count para scoring hoy. El expediente no demuestra que el conteo estuviera disponible en 2025-06-01T00:00:00Z: no hay ventana, fecha de disponibilidad ni código, y la exportación es posterior (2025-08-01). El riesgo de leakage temporal no es determinable, con sospecha razonable.

## Hallazgos

- **Temporal/disponibilidad (Riesgo, severidad alta):** el conteo podría incluir reclamos posteriores al scoring. Fuente: context.md y dictionary.json (feature_available_at nulo). Acción: obtener ventana y corte.
- **Muestra (No determinable):** tres filas no permiten evaluar utilidad ni generalización.

## Evidencia

Comprobación por lectura, no ejecución: en las tres filas exported_at es posterior a prediction_at. No se ejecutaron checks deterministas.

## Preguntas abiertas

¿Cuál es la ventana del conteo? ¿Existe snapshot versionado al momento del scoring? ¿Qué código construye la feature?

## Recomendaciones

No usar en scoring hoy. La conclusión cambiaría con: código con ventana cerrada antes de prediction_at; registro de disponibilidad anterior o igual a 2025-06-01; snapshot histórico verificable del conteo; y auditoría de cutoff sobre el expediente completo.