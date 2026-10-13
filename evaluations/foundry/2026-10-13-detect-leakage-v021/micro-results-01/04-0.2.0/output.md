---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-13
modo: guia_textual
estado: auditoria_parcial_no_certificada
inputs:
- context.md
- dictionary.json
- observations.csv
---

## Resumen

No recomendar hoy usar complaint_count para scoring. Hay riesgo alto de leakage temporal: no existen fecha de disponibilidad, ventana de conteo ni código de construcción, y la exportación (2025-08-01) es posterior al scoring (2025-06-01). El conteo podría incluir reclamos posteriores al momento de predicción.

## Hallazgos

- **Riesgo (no confirmado):** disponibilidad temporal indeterminada. Mecanismo posible: conteo calculado al exportar. Severidad: alta. Acción: bloquear su uso en scoring.
- **No determinable:** ventana de conteo y versión histórica de la feature.

## Evidencia

Lectura de context.md y dictionary.json: feature_available_at y construction_code son nulos. Lectura de observations.csv: tres filas con exported_at posterior a prediction_at. No se ejecutaron checks deterministas ni se leyó código de construcción.

## Preguntas abiertas

- ¿Cuál es la ventana del conteo?
- ¿El valor refleja el estado al prediction_at o al momento de exportación?
- ¿Existe snapshot histórico disponible en producción?

## Recomendaciones

1. No usar complaint_count en scoring hasta resolver las preguntas abiertas.
2. Aportar el código de construcción, la ventana y la fecha de disponibilidad en producción, con cierre ≤ 2025-06-01T00:00:00Z.
3. Reconstruir la feature tal como existía al 2025-06-01 desde una fuente con corte verificable, y evaluar sin outcomes posteriores.
4. Conclusión cambiaría si se demuestra que el conteo usa solo reclamos anteriores al prediction_at y que estaba disponible en producción en esa fecha.