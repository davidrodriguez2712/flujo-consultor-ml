# Manual — Piloto sintético de churn y retención

## Decisión y contrato vigente

Priorizar 50 clientes activos para revisión de retención mensual. Churn es cancelar durante el mes del scoring. KPI: Precision@50 y Recall@50 mensual; Lift@50 complementario. MRR es exposición descriptiva, no recupero ni ROI. Datos 100% sintéticos. Reviewer: David Rodríguez; equipo operativo ficticio de retención.

El intake .acos/project-profile.yaml conserva la historia inicial. Resoluciones aceptadas: framing/framing.yaml, framing/metrics.md y DECISIONS.md. Fuente canónica del avance: .acos/state.yaml.

## Estado vigente: COMPLETED

Las siete etapas y doce gates del laboratorio están aprobados. Handoff y cierre aceptados por David; evidencia en evidence/approvals/2026-10-07-handoff.md. No hay siguiente etapa dentro del proyecto.

## Cómo usar el proyecto cerrado

1. Leer handoff/closure.md para el balance y handoff/runbook.md para uso/reproducción. El runbook conserva la versión revisada antes del cierre; la aprobación posterior y el estado vigente constan en approvals y state.
2. Consultar decision/recommendation.md y validation/model_validation.md para resultados y límites; conservar datos, policy, modelo y outputs originales.
3. Ejecutar acos status y acos validate --gate handoff para comprobar cierre/integridad. V1 mantiene handoff como etapa final y puede mostrar ese gate o preguntas en acos next aun después de COMPLETED; no indica trabajo pendiente. Usar status/state para determinar cierre.
4. Revisar propuestas separadas en docs/acos/validation/2026-10-07-post-pilot-next-steps.md del checkout del OS; handoff/closure.md contiene un resumen portable.
5. Nuevos datos o mejoras requieren otro protocolo/contexto; no reabrir silenciosamente el piloto ni reutilizar el holdout observado como test intacto. La aprobación del laboratorio no cambia madurez Foundry.

## Reproducción de desarrollo

Desde la carpeta del piloto, con Python 3.11+ y un destino nuevo:

```bash
python analysis/baseline.py --output /ruta/a/destino-vacio
```

Comparar cinco JSON contra analysis/outputs/baseline-development/. Tests: python -m pytest -q analysis/test_baseline.py (requiere pytest). No sobrescribir outputs ni datasets archivados. Usar exclusivamente data/raw v2.

## Capabilities y continuidad

Snapshots understand-dataset, design-validation y detect-leakage 0.1.0 experimental, en .agents/skills y .claude/skills. CAPABILITIES.md registra cobertura y límites. Comprobar disponibilidad nativa antes de invocar; esta auditoría de pipeline fue aplicación manual de pautas, no una ejecución comparativa de skill.

Al cerrar sesión actualizar STATE, MANUAL y TASKS. Registrar feedback con tarea, versión y evidencia; anonimizar antes de trasladar al Foundry. No promover automáticamente ni modificar snapshots. El test sintético no demuestra generalización, efecto causal o readiness de producción.

## Evidencia de evaluación final

analysis/evaluate_holdout.py es el runner sin entrenamiento. Los outputs preservados están en analysis/outputs/holdout-final; metadata identifica los hashes del modelo y policy. No sobrescribir ni ejecutar cambios de parámetros sobre el test observado. La auditoría recalculó resultados desde los outputs, sin elegir otro modelo. 105 tests de producto y piloto pasan. No se generó un nuevo conjunto de reserva ni se simularon campañas.
