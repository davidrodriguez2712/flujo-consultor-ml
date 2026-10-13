# Evaluación final — churn sintético

Fecha: 2026-10-07. Etapa: validation. Revisión humana pendiente.

## Contrato y ejecución

Execution aprobado por David; evidencia en evidence/approvals/2026-10-07-execution.md. Evaluación del modelo por grupos congelado al 1 de julio de 2025 sobre julio–diciembre, sin refit ni tuning. 6.860 observaciones cliente-mes, 292 positivos y 50 seleccionados por mes. Enero 2026 excluido por labels pendientes. Modelo y policy conservan sus hashes de desarrollo.

## Resultado principal

| Métrica, media mensual | Desarrollo (9 meses) | Holdout (6 meses) | Aleatorio esperado, holdout |
|---|---:|---:|---:|
| Precision@50 | 13.56% | 10.67% | 4.28% |
| Recall@50 | 10.74% | 11.02% | 4.40% |
| Lift@50 | 3.49 | 2.52 | 1,00 |

La Precision@50 baja 2,89 puntos porcentuales respecto del desarrollo. La comparación no identifica la causa: los meses, población y prevalencia difieren, y desarrollo reentrena por fold mientras el holdout usa un modelo fijo. No atribuir el cambio exclusivamente a drift ni afirmar significancia sin otro análisis. El lift medio es la media de lifts mensuales, no el cociente de las precisiones medias.

## Por mes

| Mes | Clientes activos | Positivos | Positivos seleccionados / 50 | Precision@50 | Recall@50 | Lift@50 |
|---|---:|---:|---:|---:|---:|---:|
| 2025-07 | 1264 | 48 | 4 | 8.00% | 8.33% | 2.11 |
| 2025-08 | 1216 | 36 | 5 | 10.00% | 13.89% | 3.38 |
| 2025-09 | 1180 | 60 | 6 | 12.00% | 10.00% | 2.36 |
| 2025-10 | 1120 | 55 | 6 | 12.00% | 10.91% | 2.44 |
| 2025-11 | 1065 | 50 | 8 | 16.00% | 16.00% | 3.41 |
| 2025-12 | 1015 | 43 | 3 | 6.00% | 6.98% | 1.42 |

Se seleccionaron 300 observaciones cliente-mes y 32 fueron positivas; el contacto no fue simulado ni causó retención. Precision entre 6% y 16%; Recall medio 11,02%: la mayoría de cancelaciones queda fuera de la capacidad de 50. Existen empates por grupos, resueltos por customer_id ascendente. No se ajustó el desempate tras observar labels.

## Comprobaciones y trazabilidad

- 105 tests pasan: 92 del producto y 13 del piloto. Los cinco nuevos checks del runner cubren exclusión temporal, pending, duplicados, disponibilidad de features e integridad del modelo.
- Nueve checks globales de auditoría verdaderos; recálculo de scores desde el modelo congelado y métricas para seis meses.
- Un run de evaluación final, cero refits. Recálculo para verificar resultados, sin probar alternativas ni cambiar parámetros.
- Datos, generador, protocolo y cinco artefactos de desarrollo conservan hashes.
- Metadata, scores, resultados y summary guardados sin sobrescribir outputs previos.

[Audit](../analysis/outputs/holdout-audit.json), [metadata](../analysis/outputs/holdout-final/metadata.json), [resultados](../analysis/outputs/holdout-final/results.json), [runner](../analysis/evaluate_holdout.py), [plan analítico](../analysis/analysis_plan.md), [selección](../analysis/selection_plan.md) y [storyline propuesta](../delivery/storyline.md).

## Interpretación y límites

El baseline concentra más cancelaciones que la expectativa aleatoria en este fixture. No hay un umbral contractual de performance mínima: esta observación no convierte automáticamente validation en PASS. Tampoco demuestra calibración, beneficio de contactar, uplift, ROI, readiness de producción o generalización a clientes reales. El MRR seleccionado es exposición descriptiva.

El fixture reproduce relaciones fijadas por el generador; entrenamiento y evaluación comparten ese proceso sintético. No entran nuevos clientes después de junio de 2024. Los meses y las entidades repetidas no son observaciones independientes para una inferencia ingenua. No se reporta intervalo ni prueba de significancia. El autor también revisó el trabajo; falta review independiente.

El holdout ya está observado: futuros cambios motivados por estos resultados necesitarán otra evaluación reservada y un protocolo nuevo; no presentarlos como mejora en un test intacto.

## Decisión pendiente

Revisar gates validation, data_analysis-review, supervised_model-review, selection-review y executive_delivery-review. Aprobarlos acepta la evaluación y sus límites para preparar delivery; no certifica utilidad comercial ni producción. Después se preparará el decision memo y el contrato de entrega para su gate específico, seguido de handoff. Ninguna skill cambia de estado en Foundry por este piloto.
