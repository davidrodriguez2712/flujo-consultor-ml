# Contrato de entrega — Laboratorio de churn

**Fecha:** 2026-10-07.  
**Estado:** preparado para revisión humana del gate delivery.  
**Reviewer:** David Rodríguez.  
**Destinatario:** David como responsable del laboratorio; audiencia de negocio ficticia de retención.  
**Formato:** Markdown y evidencia JSON/CSV/código dentro del workspace local.

## Propósito

Entregar la recomendación y evidencia analítica del piloto sintético que prioriza 50 clientes activos por mes. El contrato cubre una entrega local de laboratorio; no constituye aceptación de producción, publicación ni envío a un cliente.

## Entregables

| Artefacto | Ruta | Función |
|---|---|---|
| Decision memo | decision/recommendation.md | Decisión, opciones, recomendación y límites |
| Informe analítico | validation/model_validation.md | Protocolo, resultados mensuales, variación y límites |
| Especificación | modeling/model_brief.md | Método y elecciones previas al holdout |
| Plan de selección | analysis/selection_plan.md | Top 50, empates y restricciones no evaluadas |
| Evidencia de evaluación | analysis/outputs/holdout-final/ | Metadata, scores, results y summary |
| Auditorías | analysis/outputs/baseline-audit.json y analysis/outputs/holdout-audit.json | Checks, hashes y recálculos |
| Modelo y policy | analysis/outputs/baseline-development/ | Baseline, parámetros y modelo congelado |
| Código | analysis/baseline.py y analysis/evaluate_holdout.py | Reproducción de desarrollo y evaluación fija |
| Datos y generador | data/raw/ y analysis/generate_synthetic_data.py | Fixture sintético v2, manifest y origen reproducible |
| Registro de entrega | delivery/delivery-manifest.json | Inventario local y hashes del subconjunto revisable |

La evaluación conserva su estado histórico al redactarse; su aprobación posterior está en evidence/approvals/2026-10-07-validation.md y .acos/state.yaml. La fuente de métricas son los JSON, no las vistas de estado.

## Criterios de aceptación propuestos

1. Memo coherente con decisión, K=50 y contrato de framing; KPI y opciones comprensibles para negocio.
2. Cifras del memo coinciden por redondeo con los JSON; distinguir media mensual, totales cliente-mes y clientes únicos.
3. Fuentes y artefactos locales accesibles; hashes del inventario correctos y modelo, policy y datos sin alteración.
4. Explicitar variación mensual, incertidumbre y alcance sintético; no convertir riesgo en efecto causal ni MRR en ROI.
5. Execution y validation aprobados con evidencia; delivery requiere su propia aprobación explícita y registrada.
6. Documentar siguiente paso a handoff sin declarar todavía el piloto completo o listo para producción.

No se ha acordado un umbral mínimo comercial de performance. Aprobar este contrato acepta la entrega del laboratorio y sus límites; no certifica utilidad en un negocio real.

## Uso y límites

Se puede inspeccionar la evidencia local y reproducir desarrollo en un destino vacío siguiendo MANUAL.md. La evaluación final autorizada ocurrió una vez; los outputs se conservan y se pueden auditar sin escoger otro modelo. El test observado no vuelve a ser una reserva intacta.

No se incluye dashboard, API, deck, integración con CRM, campaña o despliegue; los entregables confirmados son informe analítico y decision memo. No hay transferencia de datos ni publicación. El inventario no empaqueta por sí solo el workspace ni sustituye el runbook de handoff, que se preparará tras aprobación de delivery.

## Revisión y continuidad

David revisa memo, contrato y evidencia antes de marcar PASS. Después se avanza a handoff y se completan instrucciones de uso, reproducción, pendientes y feedback local de capabilities. Las skills permanecen experimental; el piloto no autoriza promoción ni cambios en el Foundry.
