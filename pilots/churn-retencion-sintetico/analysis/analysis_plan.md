# Plan analítico vigente — revisión de validation

## Decisión y fuentes

Priorizar 50 clientes activos al inicio del mes según riesgo de cancelar durante ese mes. Usar data/raw v2 y contrato aprobado. Fixture 100% sintético; manifest, diccionario y diagnosis son trazables. No usar borradores interim.

## Trabajo ejecutado

1. Discovery y framing: decisión, KPI, unidad cliente-mes y maduración de labels aceptados.
2. Diagnosis: checks de claves, cardinalidad de joins, disponibilidad, alta y target; generador v2 corregido y aprobado.
3. Execution: baseline por grupos, cuatro features históricas, mediana del train y suavizado; nueve folds septiembre 2024–mayo 2025; revisión humana aprobada.
4. Validation: modelo fijo entrenado con labels disponibles al 1 de julio de 2025; seis meses de holdout sin refit, sin tuning y sin enero pendiente.
5. Comparación: Precision@50, Recall@50 y Lift@50 mensual frente a expectativa analítica de selección aleatoria, con medias macro.

## Evidencia y límites

Model brief, policy, baseline-audit.json, holdout-audit.json y validation/model_validation.md. 105 tests pasan. No hay inferencia causal, significancia demostrada o evaluación de clientes nuevos. Gate data_analysis-review pendiente; preparar decision memo tras revisión humana.
