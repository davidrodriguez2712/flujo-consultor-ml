---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-13
modo: guia_textual
estado: no_recomendar_uso_para_scoring_aun
inputs: context.md, dictionary.json, observations.csv
---

## Resumen

No recomendaría usar complaint_count para scoring hoy. El expediente no acredita cuándo existía el dato ni qué ventana cubría; el conteo podría reflejar el estado al exportar (2025-08-01), posterior al scoring (2025-06-01). Un ejemplo de 3 filas no permite estimar riesgo ni generalización.

## Hallazgos

- **Riesgo alto, no confirmado:** disponibilidad temporal indeterminada. Mecanismo posible: feature construida con información posterior al prediction_at.
- **Riesgo alto:** ventana de conteo no documentada; no se puede verificar que termine antes del scoring.
- **Lectura de código/metadata:** `feature_available_at` y `construction_code` son null.

## Evidencia

- Lectura de context.md: scoring 2025-06-01, exportación 2025-08-01, outcomes conocidos post-scoring.
- Lectura de dictionary.json: ventana y disponibilidad no documentadas.
- Lectura de observations.csv: 3 filas; no hay comprobación de fechas por feature (no ejecutada).

## Preguntas abiertas

- ¿Cuándo se materializa complaint_count en producción y con qué corte?
- ¿Cuál es la ventana de conteo (inicio y fin)?
- ¿Existe código de construcción o versión histórica al 2025-06-01?
- ¿Qué valores tenía el conteo en la fecha de scoring?

## Recomendaciones

- Mantener complaint_count fuera del scoring hasta documentar disponibilidad y ventana.
- Reconstruir el feature con snapshot verificable al 2025-06-01T00:00:00Z.
- Aportar código de construcción y fuente de logs de producción.
- Evidencia que cambiaría la conclusión: log de producción con timestamp de disponibilidad anterior o igual al scoring, ventana cerrada antes del corte, y código que confirme esa lógica.