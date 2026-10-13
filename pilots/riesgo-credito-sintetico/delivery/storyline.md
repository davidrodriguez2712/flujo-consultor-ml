# Storyline propuesto para Delivery

## Decisión

Qué solicitudes priorizar para revisión manual con capacidad de hasta100por mes. El piloto aporta evidencia de riesgo en concedidas; no valida una política sobre todas las solicitudes.

## Mensaje central

El baseline supera puntualmente a una referencia constante en concedidas maduras del periodo final: Brier0.102487vs0.116530,ROC-AUC0.752283 sobre447solicitudes. Hay desajustes de calibración y tamaños de bin reducidos; no declarar probabilidades certificadas.

## Evidencia que limita la recomendación

900solicitudes puntuadas;453rechazadas sin outcome. En el Top-100 de todas las solicitudes, solo22–26%tiene label observado. Precision/Recall/Lift globales no identificados. Las métricas favorables de concedidas no se transfieren a esa lista. La selección mensual es retrospectiva, no revisión online; el ahorro no se identifica.

## Recomendación propuesta

Conservar prototipo y evidencia reproducible como aprendizaje de laboratorio. Antes de una política real, definir decisión/momento de revisión, datos disponibles, población evaluable y cómo medir resultados. Sin aprobación automática de crédito, despliegue, ahorro demostrado ni promoción de skills.

## Entregable

Decision memo con findings, acción propuesta, límites y siguientes evidencias necesarias; runbook y handoff. Este storyline está para revisión de Validation, no es un memo final aprobado ni publicación al cliente.

## Fuentes

`validation/model_validation.md`, `analysis/outputs/baseline-final/results.json`, `reports/final-validation/output-audit.json` y auditoría de pipeline `reports/leakage/leakage-audit-2026-10-08-02.md`.
