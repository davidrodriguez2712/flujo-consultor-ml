# Findings de Diagnosis

## F01 — Joins y grain

Hecho: application_id único, grain solicitud; cinco tablas con 7.200 filas y mismas claves. Join por cliente produciría 35.914 filas. Acción: unir por application_id con validación1:1. Evidencia: `analysis/outputs/diagnosis-checks.json` y reporte de dataset.

## F02 — Fuentes posteriores

Hecho: max_dpd_90d reproduce el target y llega después del scoring; decisiones/desembolso también posteriores. Acción: separar features/labels/metadatos conforme al diseño. No hay modelo que haya usado estas columnas. Evidencia: reporte de leakage.

## F03 — Labels y cutoff

Hecho: 390 pendientes, 3.726 rechazadas sin target; 455 outcomes de solicitudes anteriores al fit final solo llegaron después de ese cutoff. Acción: filtros de disponibilidad; no completar con0. Evidencia: checks y contrato de datos.

## F04 — Población y acción

Hecho del generator: la concesión selecciona la población observada. Desempeño en concedidas no identifica el de rechazadas. Benchmark Top-K mensual es retrospectivo; no simula revisión online antes del desembolso. Acción: conservar ambos límites en métricas y memo.

## F05 — Diseño temporal propuesto

Train development al2025-01-01:1.248 filas. Validation enero–febrero, selección al2025-06-15:298. Refit final al2025-07-01:2.140. Periodo final julio–septiembre:900 solicitudes,447 concedidas maduras,453 rechazadas. Modelo fijo, features disponibles al scoring, sin labels futuros al fit. Evidencia: `reports/validation/validation-design-2026-10-08.md`.

## Decisión pendiente

Aprobar contenido de Diagnosis y data-quality antes de pasar a Execution. No se calcularon métricas de modelo ni se demuestra eficacia de skills. Los reports no sustituyen la revisión humana.
