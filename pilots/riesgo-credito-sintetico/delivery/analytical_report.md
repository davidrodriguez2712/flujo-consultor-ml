# Informe analítico — resumen trazable

Versión 0.1.0 · 2026-10-08 · Datos 100 % sintéticos. Entregable local pendiente de aprobación de Delivery.

## Pregunta y método

Priorizar solicitudes para revisión manual bajo capacidad de hasta 100 por mes. Una fila por application_id; customer_id identifica recurrencia. Join 1:1 por solicitud, información disponible al scoring, target de 30DPD dentro de 90 días desde desembolso y label completa al día 97.

El generator produce cinco CSV reproducibles, seed 20261008. La concesión histórica simulada selecciona la población con outcomes. Pendientes/rechazadas mantienen targets ausentes. Se detectaron columnas posteriores y fan-out potencial al unir por cliente; el pipeline usa únicamente las cinco features admitidas.

## Flujo evaluado

| Fase | Train | Evaluation | Brier modelo / referencia | ROC-AUC modelo |
|---|---:|---:|---:|---:|
| Development | 1.248, labels disponibles al 2025-01-01 | 298 concedidas maduras, enero–febrero | 0,104092 / 0,116932 | 0,708430 |
| Final | 2.140, labels disponibles al 2025-07-01 | 447 concedidas maduras, julio–septiembre | 0,102487 / 0,116530 | 0,752283 |

Mismo algoritmo, features, hiperparámetros y bins; refit final único y referencia de train correspondiente. Scores finales persistidos antes de cargar labels de evaluation. No comparar el AUC entre fases como prueba de mejoría por versión: las poblaciones y el train son distintos.

## Hallazgos que afectan la decisión

- Mejora puntual de Brier frente a la referencia en la población final evaluable; sin significancia/generalización real demostradas.
- Desajustes de calibración y bins superiores pequeños; probabilidades no certificadas.
- 900 solicitudes finales puntuadas; 453 rechazadas sin outcome. Top-100 global con coverage de 26 %, 22 % y 26 %: métricas globales no identificadas.
- Benchmark mensual retrospectivo; sin una política online previa al desembolso ni efecto causal/ahorro identificado.

## Evidencia y reproducción

- [Diccionario](../data/dictionaries/README.md) y [manifest de fuentes](../data/raw/manifest.json).
- [Checks de Diagnosis](../analysis/outputs/diagnosis-checks.json) y [diseño temporal](../validation/validation_design.yaml).
- [Development](../reports/execution/development-report.md), [freeze](../reports/execution/development-freeze.json) y [manifest](../reports/execution/evidence-manifest.json).
- [Validación final](../validation/model_validation.md), [freeze final](../reports/final-validation/final-freeze.json), [audit](../reports/final-validation/output-audit.json), [review por otro agente](../reports/final-validation/agent-output-review.md) y [manifest](../reports/final-validation/evidence-manifest.json).

Los protocolos guardan comandos reproducibles y requieren outputs nuevos. No reusar este holdout para seleccionar una versión futura y presentarla como evaluación independiente. La suite combinada verificada en Validation pasó 191 pruebas; ese conteo no prueba calidad de negocio ni eficacia de skills.

## Conclusión

El piloto aporta un resultado técnico reproducible y una limitación operacional visible. La recomendación y el siguiente trabajo se detallan en el [decision memo](decision_memo.md). El proyecto aún no está cerrado; faltan aprobación de Delivery y handoff.
