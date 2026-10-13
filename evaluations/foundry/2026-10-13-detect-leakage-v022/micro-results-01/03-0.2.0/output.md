---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-13
modo: guia_textual
estado: no_concluyente
inputs:
- context.md
- dictionary.json
- observations.csv
---
## Resumen
No recomendar hoy `complaint_count` para scoring. El expediente no permite establecer que el conteo existiera al 2025-06-01T00:00:00Z. Conclusión provisional, basada en lectura del expediente; no se ejecutaron pipelines ni checks deterministas.

## Hallazgos
- Riesgo de leakage temporal (no confirmado): el conteo podría reflejar reclamos hasta la exportación (2025-08-01), posteriores al scoring y al periodo del target.
- Severidad: alta para uso operacional. Confianza: media-baja.
- Acción: bloquear el uso en scoring hasta verificar disponibilidad y ventana.

## Evidencia
- Lectura: `exported_at` (2025-08-01) es posterior a `prediction_at` (2025-06-01) en las 3 filas.
- Lectura: `dictionary.json` tiene `feature_available_at` y `construction_code` nulos; la ventana no está documentada.
- Lectura: `context.md` indica que no se sabe si el conteo corresponde al scoring o a la exportación.
- Muestra de 3 filas: insuficiente para estimar efectos; no se verificó igualdad feature-target.

## Preguntas abiertas
- ¿Desde cuándo y con qué corte existe `complaint_count` en producción?
- ¿Cuál es la ventana de conteo?
- ¿Existe código de construcción y versión histórica?

## Recomendaciones
- No usar para scoring hoy.
- Para reconsiderar, aportar: `feature_available_at` ≤ 2025-06-01; ventana cerrada antes de `prediction_at`; código con filtro temporal; snapshot as-of reproducible.
- Pendiente: checks deterministas de ventana, join y cardinalidad sobre el código real.