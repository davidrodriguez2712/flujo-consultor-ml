---
skill: detect-leakage
version: 0.2.1
fecha: 2026-10-13
modo: guia_textual
estado: No determinable (provisional)
inputs:
- context.md
- dictionary.json
- observations.csv
---

## Resumen

No se puede recomendar hoy usar complaint_count para scoring. El expediente no acredita cuándo existía el conteo ni qué ventana cubre. Recomendación provisional: no usarlo en producción hasta verificar disponibilidad.

## Hallazgos

- **Componente:** complaint_count.
- **Conclusión:** No determinable.
- **Brecha:** sin fecha de disponibilidad, ventana de conteo ni código de construcción; no se sabe si refleja el estado al scoring (2025-06-01) o al exportar (2025-08-01).
- **Fuente:** context.md; dictionary.json (feature_available_at y construction_code nulos).
- **Confianza:** baja en validez y en invalidez.
- **Severidad potencial:** alta, por posible información posterior al scoring.
- **Acción:** reserva de uso bajo autoridad del owner hasta verificar.

## Evidencia

- Lectura textual del expediente (no ejecutada): exportación posterior al scoring; la exportación solo fecha la extracción, no la feature.
- Lectura de observations.csv (no ejecutada): 3 filas, con complaint_count y cancelled_next_30d en la misma exportación. Muestra insuficiente para conclusiones de performance.
- Comprobaciones pendientes: timestamps de eventos de reclamo vs. prediction_at; conteo de reclamos con fecha ≤ 2025-06-01.

## Preguntas abiertas

1. ¿Cuándo se registró cada reclamo contabilizado?
2. ¿Qué ventana cubre el conteo (p. ej., últimos N días antes de prediction_at)?
3. ¿Existe versión histórica del conteo fechada al 2025-06-01?
4. ¿Cuál es el código de construcción y la disponibilidad efectiva en producción?

## Recomendaciones

- No aprobar complaint_count para scoring hoy.
- Solicitar código de construcción y fecha de disponibilidad al owner.
- Verificar por lectura que todos los reclamos contados tengan fecha ≤ prediction_at y que la ventana esté documentada.
- Reconstruir el conteo con corte 2025-06-01 solo si hay fuente verificable.
- Esta conclusión cambiaría a Confirmado si se demuestra uso de reclamos posteriores al scoring; a validez provisional si se demuestran fechas y ventana previas, y disponibilidad al scoring.