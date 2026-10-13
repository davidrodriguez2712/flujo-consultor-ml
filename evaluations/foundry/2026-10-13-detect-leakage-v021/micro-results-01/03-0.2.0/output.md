---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-13
modo: guia_textual
estado: borrador_no_determinable
inputs: context.md, dictionary.json, observations.csv
---

## Resumen
No es posible recomendar usar complaint_count para scoring hoy. El expediente no acredita cuándo estaba disponible el conteo ni qué ventana cubre. Riesgo de leakage temporal no determinable, con sospecha material por el conteo al exportar (2025-08-01) posterior al scoring (2025-06-01). Comprobación ejecutada solo por lectura.

## Hallazgos
- **H1 – Disponibilidad temporal (Riesgo, severidad alta):** `feature_available_at` es null. No se sabe si el conteo existía al 2025-06-01T00:00:00Z.
- **H2 – Ventana indefinida (Riesgo, severidad alta):** la ventana de conteo no está documentada; podría incluir reclamos posteriores al scoring.
- **H3 – Snapshot posterior (Probable, severidad alta):** el conteo podría reflejar el estado a la exportación, que es posterior al scoring.

## Evidencia
- Lectura de `context.md`: scoring 2025-06-01, exportación 2025-08-01, outcomes posteriores disponibles solo para evaluación.
- Lectura de `dictionary.json`: ventana y disponibilidad no documentadas; código de construcción null.
- Lectura de `observations.csv` (3 filas): complaint_count 3, 0, 2; no permite validar ventana ni disponibilidad.

## Preguntas abiertas
- ¿Cuál es la fecha efectiva de disponibilidad del conteo en producción?
- ¿Qué ventana temporal cubre complaint_count?
- ¿El valor almacenado corresponde al estado al scoring o a la exportación?
- ¿Existe código o log de construcción versionado?

## Recomendaciones
- No usar complaint_count en scoring hasta documentar disponibilidad y ventana.
- Evidencia que cambiaría la conclusión: fecha de disponibilidad ≤ 2025-06-01T00:00:00Z, ventana cerrada antes del scoring y código o snapshot histórico verificable.
- Reevaluar con un snapshot reconstruido con corte verificable.