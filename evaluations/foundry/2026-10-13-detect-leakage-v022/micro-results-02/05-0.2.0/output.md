---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-13
modo: guia_textual
estado: no_recomendado_hoy
inputs:
  - context.md
  - dictionary.json
  - observations.csv
---

## Resumen
No recomendar usar complaint_count para scoring hoy. El expediente no demuestra que el conteo estuviera disponible al 2025-06-01T00:00:00Z. La exportación es posterior (2025-08-01) y no certifica el estado histórico. Riesgo de leakage temporal: no determinable.

## Hallazgos
- **Riesgo (no determinable):** disponibilidad temporal de complaint_count. Mecanismo posible: el conteo refleja el estado al exportar, no al scoring. Confianza: media. Severidad: alta. Acción: bloquear el uso hasta verificar.
- **Target leakage no confirmado:** en las tres filas no se identifica igualdad ni señal perfecta. Esto no descarta leakage.

## Evidencia
- Lectura (no ejecutada): dictionary.json tiene feature_available_at y construction_code en null; la ventana no está documentada.
- Lectura: exported_at (2025-08-01) es posterior a prediction_at (2025-06-01).
- Lectura: context.md indica que la exportación no certifica disponibilidad en producción.

## Preguntas abiertas
- ¿Cuándo estaba disponible complaint_count en producción?
- ¿Qué ventana cubre el conteo y termina antes del scoring?
- ¿El conteo se reconstruyó con corte 2025-06-01?

## Recomendaciones
- No usar complaint_count para scoring hoy.
- Solicitar código de construcción, ventana y timestamp de disponibilidad.
- Reconstruir la feature con un snapshot verificable al 2025-06-01, si existe.
- La conclusión cambiaría con evidencia de disponibilidad ≤ prediction_at y ventana cerrada antes del corte.