# Baseline de desarrollo — churn sintético

Fecha: 2026-10-07. Etapa: execution. Revisión humana pendiente.

## Resultado

Baseline de riesgo por grupos, descrito en [model brief](../../modeling/model_brief.md). Política fijada antes de la primera ejecución y sin tuning. Nueve folds walk-forward; comparación contra expectativa analítica de selección aleatoria, no contra una campaña real.

| Métrica, media mensual | Baseline | Aleatorio esperado |
|---|---:|---:|
| Precision@50 | 13.56% | 3.85% |
| Recall@50 | 10.74% | 3.13% |
| Lift@50 | 3.49 | 1,00 |

Son medias macro: cada mes pesa igual; el lift medio no es el cociente de las precisiones medias. En total se seleccionaron 450 observaciones cliente-mes y 61 fueron positivas; no son necesariamente 450 clientes distintos.

## Por mes

| Mes | Train | Scoring | Positivos seleccionados / 50 | Precision@50 | Recall@50 | Lift@50 |
|---|---:|---:|---:|---:|---:|---:|
| 2024-09 | 10394 | 1878 | 10 | 20.00% | 13.33% | 5.01 |
| 2024-10 | 12329 | 1803 | 8 | 16.00% | 11.76% | 4.24 |
| 2024-11 | 14207 | 1735 | 8 | 16.00% | 10.96% | 3.80 |
| 2024-12 | 16010 | 1662 | 8 | 16.00% | 11.43% | 3.80 |
| 2025-01 | 17745 | 1592 | 4 | 8.00% | 8.00% | 2.55 |
| 2025-02 | 19407 | 1542 | 4 | 8.00% | 7.41% | 2.28 |
| 2025-03 | 20999 | 1488 | 7 | 14.00% | 12.96% | 3.86 |
| 2025-04 | 22541 | 1434 | 7 | 14.00% | 12.07% | 3.46 |
| 2025-05 | 24029 | 1376 | 5 | 10.00% | 8.77% | 2.41 |

## Comprobaciones

- Suite local completa: 100 tests pasan (92 de ACOS + 8 del piloto), en 2,69 s. Evidencia: analysis/outputs/execution-test-results.json.
- 8 tests unitarios del baseline pasan: maduración de labels, cutoff de entrenamiento, exclusión de outcomes/ID, imputación, scoring sin target, empate y métricas exactas, ausencia de positivos y capacidad efectiva.
- Cinco JSON reproducidos idénticos byte a byte en otro destino.
- Nueve folds: train anterior al scoring, labels disponibles al entrenar, claves train/validation sin solape, mediana exclusivamente del train y métricas recalculadas por separado.
- Datos v2 y protocolo conservan los hashes revisados.
- Modelo final congelado con 26.839 filas disponibles al 1 de julio de 2025; última observación de mayo. No se ha puntuado ni evaluado el holdout de julio–diciembre.

Evidencia: [audit](../../analysis/outputs/baseline-audit.json), [policy](../../analysis/outputs/baseline-development/policy.json), [resultados](../../analysis/outputs/baseline-development/results.json), [modelo final](../../analysis/outputs/baseline-development/final-model.json) y [auditoría del pipeline](../leakage/leakage-audit-2026-10-07-02.md).

## Límites y revisión

Los resultados solo describen el fixture sintético. No demuestran generalización real, calibración, significancia estadística ni efecto causal de retención. La prevalencia y el tamaño de la cohorte cambian; no entran nuevos clientes después de junio de 2024. Hay empates por tratarse de un modelo por grupos, resueltos por ID; no se optimizó ese criterio. El MRR de positivos seleccionados es exposición descriptiva, no ingreso recuperado.

El mismo asistente construyó y revisó el baseline: no es review independiente ni evaluación comparativa de la skill detect-leakage. La evidencia no permite promover skills del Foundry.

Siguiente decisión: revisión humana del gate execution. Si se aprueba, avanzar a validation y evaluar una vez el modelo ya congelado sobre julio–diciembre, sin refit ni selección por resultados del test. Enero 2026 continúa pendiente y excluido de evaluación.
