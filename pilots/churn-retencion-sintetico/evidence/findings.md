# Hallazgos preparatorios — datos sintéticos v1

- [Hecho] 35990 snapshots sobre 24 períodos; claves sin duplicados.
- [Hecho] 35018 labels observadas y 972 pendientes; estas últimas están vacías.
- [Hecho] 1428 positivos; churn observado 4.08%.
- [Hecho] 730 valores de actividad missing; no imputar cero por defecto.
- [Hecho] El join directo de tickets produciría 36853 filas frente a 35990 snapshots. Agregar antes del join.
- [Hecho] Checks corregidos de actividad/tickets anteriores al alta: todos cero. Primera versión falló en estos checks; borrador conservado.
- [Límite] Sin datos reales, población renovada ni tratamiento/control. No extrapolar tasa, ranking o impacto a un cliente real.

Evidencia: `analysis/outputs/data-checks.json`, `data/raw/manifest.json` y diccionario. No se aprobaron gates.

## Diagnóstico v2 — 2026-10-07

Se detectó una cancelación posterior al corte de extracción en v1 y se corrigió. V2 supera 26 checks sin infracciones. Datos observados y demás CSV no cambiaron. Reports de comprensión y leakage preparados; pipeline de entrenamiento todavía no auditable. Ver reports/dataset y reports/leakage, diagnosis-checks.json y generator-v2-regression.json. Diagnosis/data-quality siguen pendientes de revisión humana.
