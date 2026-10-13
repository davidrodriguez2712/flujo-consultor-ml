# Cierre del piloto — Churn / retención

Fecha: 2026-10-07. Status canónico: COMPLETED. Reviewer: David Rodríguez.

## Alcance completado

Discovery → framing → diagnosis → execution → validation → delivery → handoff. Siete etapas y doce gates aprobados con evidencia. Inputs sintéticos, baseline reproducible, evaluación temporal, decision memo, contrato de entrega y runbook local. [Aprobación final](../evidence/approvals/2026-10-07-handoff.md).

## Resultado y evidencia

- Holdout julio–diciembre 2025: Precision@50 media 10,67%, Recall@50 11,02%, Lift@50 2,52; 32 positivos entre 300 selecciones cliente-mes.
- Nueve folds de desarrollo; modelo fijo al 1 de julio, seis meses de test sin refit ni tuning.
- Cuatro CSV y cinco JSON de desarrollo reproducidos idénticos; hashes originales conservados. El test no se repitió al preparar handoff.
- Suite combinada ejecutada: 105 tests. Cierre y resultados de comprobación registrados en analysis/outputs/closure-checks.json.

La aprobación corresponde al laboratorio. No hay beneficio causal, ROI, generalización real o producción demostrados. El cierre de proyectos y la madurez de capacidades son ciclos distintos.

## Foundry

understand-dataset, design-validation y detect-leakage 0.1.0 permanecen experimental. Solo design-validation tuvo comparación exploratoria nativa; no demostró mejora consistente en un caso. Las otras pautas se aplicaron manualmente por el asistente. Review no independiente. [Feedback](capability_feedback.md).

## Siguientes iniciativas propuestas

1. Revisar el solapamiento de validate-delayed-outcome-targets con understand-dataset/design-validation. Primera prioridad por los errores temporales observados; considerar contrato/gate o extensión antes de nueva skill.
2. Contrastar evaluate-operational-selection: capacidad, empates, repetición, labels y límites causales. Este piloto aporta contexto sintético, no eficacia demostrada.
3. Contrastar synthesize-evidence-to-recommendation mediante playbook/template: preservar lineage, opciones, incertidumbre y límites en otras casuísticas.
4. Ejecutar Windows nativo y probar movilidad del workspace fuera del checkout original.
5. Pilotar con datos reales y review independiente cuando exista contexto y autorización.

Estas iniciativas están propuestas, no completadas ni promovidas. Revisar catálogo existente antes de crear fichas duplicadas. Detalle de priorización en el checkout del OS: docs/acos/validation/2026-10-07-post-pilot-next-steps.md.

## Conservación

El runbook y el inventario inicial conservan su estado histórico de preparación para revisión. handoff-manifest-02-closed.json registra el estado final autorizado sin sobrescribir esa evidencia. El inventario del delivery sigue intacto. No depender de rutas tmp para conservar el proyecto.

V1 todavía devuelve preguntas/gate de handoff en next/status cuando está COMPLETED. El cierre se determina por status/state y aprobación de todos los gates; esta observación se documenta para una mejora separada del producto.
