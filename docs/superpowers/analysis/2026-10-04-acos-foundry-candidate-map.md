# Mapa de hipótesis ACOS a candidates del Foundry

**Estado:** 24 fichas documentadas; 18 decisiones de mantener como conocimiento y seis diferidas. Actualizado el 6 de octubre de 2026.  
**Fecha:** 4 de octubre de 2026

## Decisiones actuales

El Foundry ya registró decisiones sobre las 24 fichas. La [revisión de integración del 6 de octubre](2026-10-06-acos-foundry-integration.md) conserva el inventario operativo y sus límites. Tres experimentos se archivaron como conocimiento y las extensiones de validación volvieron a `0.1.0`; no se seleccionan variantes archivadas.

## Resultado de la revisión inicial

Se conservaron 24 fichas porque las hipótesis tienen triggers, outputs o preguntas de evaluación distintos. No se fusionaron por proximidad temática. La consolidación se refleja en el tratamiento recomendado: antes de experimentar, decidir si una ficha requiere skill independiente, extensión, playbook, template o gate. Una ficha no obliga a crear una skill.

El Foundry conserva los candidates canónicos. Este mapa solo enlaza las fichas; el registro H01–H24 conserva su origen exploratorio y los escenarios son hipotéticos. Ninguna simulación acredita recurrencia real, mejora baseline/treatment ni promoción.

## Candidates canónicos y tratamiento propuesto

| Hipótesis | Candidate en Foundry | Tratamiento inicial propuesto | Decisión actual en Foundry |
|---|---|---|---|
| H01 | [frame-business-decision](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-frame-business-decision.md) | Procedimiento candidato; comparar con brief/gate del OS antes de elegir skill. | mantener como conocimiento |
| H02 | [quantify-decision-impact](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-quantify-decision-impact.md) | Procedimiento candidato de impacto, condicionado a inputs de valor/coste. | mantener como conocimiento |
| H03 | [formulate-constrained-decision](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-formulate-constrained-decision.md) | Template de formulación primero; evaluar skill si mejora la identificación de objetivos/restricciones. | mantener como conocimiento |
| H04 | [design-intervention-evaluation](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-design-intervention-evaluation.md) | Procedimiento candidato de diseño de evaluación causal. | mantener como conocimiento |
| H05 | [evaluate-operational-selection](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-evaluate-operational-selection.md) | Procedimiento candidato o ampliación del gate de selección operativa. | mantener como conocimiento |
| H06 | [forecast-backtesting](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-forecast-backtesting.md) | Propuesta de extensión de design-validation; skill separada solo si necesita un workflow propio verificable. | mantener como conocimiento |
| H07 | [evaluate-grounded-assistant](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-evaluate-grounded-assistant.md) | Procedimiento candidato de evaluación del asistente con fuentes, más eval set/contratos. | mantener como conocimiento |
| H08 | [synthesize-evidence-to-recommendation](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-synthesize-evidence-to-recommendation.md) | Playbook/template de delivery primero; evaluar mejora antes de elegir skill. | mantener como conocimiento |
| H09 | [reconcile-business-metrics](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-reconcile-business-metrics.md) | Template/gate de definiciones y posible procedimiento de reconciliación. | mantener como conocimiento |
| H10 | [design-entity-resolution](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-design-entity-resolution.md) | Contrato/mapping y procedimiento especializado por contrastar. | pendiente (diferido) |
| H11 | [assess-decision-data-readiness](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-assess-decision-data-readiness.md) | Propuesta de extensión de understand-dataset más matriz requisito/fuente y gate. | mantener como conocimiento |
| H12 | [evaluate-document-extraction](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-evaluate-document-extraction.md) | Schema/eval set y procedimiento especializado por contrastar. | mantener como conocimiento |
| H13 | [evaluate-recommendation-policy](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-evaluate-recommendation-policy.md) | Procedimiento especializado de evaluación de políticas de recomendación. | pendiente (diferido) |
| H14 | [audit-inherited-solution](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-audit-inherited-solution.md) | Playbook de auditoría primero; coordinación de checks existentes. | mantener como conocimiento |
| H15 | [diagnose-event-log-process](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-diagnose-event-log-process.md) | Contrato de eventos y playbook antes de elegir skill. | pendiente (diferido) |
| H16 | [define-agent-action-boundaries](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-define-agent-action-boundaries.md) | Contratos/gates de autoridad primero; procedimiento de diseño/revisión por contrastar. | mantener como conocimiento |
| H17 | [design-operational-monitoring](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-design-operational-monitoring.md) | Playbook/runbook primero; skill solo si mejora su diseño de forma observable. | mantener como conocimiento |
| H18 | [design-human-review-policy](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-design-human-review-policy.md) | Contrato/gates de revisión humana primero. | mantener como conocimiento |
| H19 | [evaluate-probability-calibration](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-evaluate-probability-calibration.md) | Propuesta de extensión especializada de design-validation; no decidir aún skill independiente. | mantener como conocimiento |
| H20 | [validate-delayed-outcome-targets](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-validate-delayed-outcome-targets.md) | Contrato/gate temporal y propuesta de extensión de understand-dataset/design-validation. | mantener como conocimiento |
| H21 | [design-time-to-event-evaluation](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-design-time-to-event-evaluation.md) | Propuesta de extensión especializada de validación, sujeta a eventos observables y supuestos. | pendiente (diferido) |
| H22 | [estimate-customer-lifetime-value](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-estimate-customer-lifetime-value.md) | Contrato/template de valor y procedimiento especializado por contrastar. | pendiente (diferido) |
| H23 | [evaluate-uplift-targeting](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-evaluate-uplift-targeting.md) | Propuesta de extensión especializada de H04/H05; comparar antes de elegir skill separada. | mantener como conocimiento |
| H24 | [design-unlabeled-anomaly-review](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-design-unlabeled-anomaly-review.md) | Playbook/contrato de evaluación sin labels; contrastar necesidad de procedimiento especializado. | pendiente (diferido) |

## Solapamientos resueltos en el diseño de las fichas

- H01/H02/H08 conservan decisión, valoración y recomendación como outputs distintos. H02/H05/H08 registran los antecedentes de impacto, ranking y narrativa EQUANS sin modificar su evidencia ni reactivar skills retiradas.
- H06/H19/H21 se consideran primero extensiones especializadas de `design-validation`; H11 de `understand-dataset`; H20 un contrato/gate o extensión de ambas. No se experimentarán skills paralelas sin comparar esas alternativas.
- H04/H23 conservan dos preguntas: identificación/diseño de la intervención y evaluación de targeting causal. H23 puede ser una extensión, no necesariamente otra skill.
- H05/H13 conservan selección operativa y recomendación con exposición/cold start. Compartir ordenamiento no equivale a compartir el contrato de evaluación.
- H07/H12/H16 conservan respuestas, campos estructurados y autoridad de acciones como límites distintos. No se propone un agent nuevo.
- H14/H15/H17/H18/H24 proponen primero playbooks, contratos o gates; H24 agrega evaluación y aprendizaje sin labels a revisión/monitoreo. H09/H10/H22 también comienzan por contratos/templates antes de decidir el procedimiento especializado.

Estas decisiones delimitan las fichas; no aprueban su candidate gate ni demuestran que el tipo propuesto sea suficiente.

## Siguiente paso

Aplicar las decisiones actuales en la selección de capacidades del compiler. No reabrir automáticamente las 18 fichas conservadas como conocimiento; para las seis diferidas esperar la condición de cada ficha. Continuar con el plan del compiler usando artefactos del OS y las nueve skills operativas según fit. La revisión de un nuevo fallo o fuente en Foundry es un flujo separado.

## Procedencia

- [Registro exploratorio H01–H24](2026-10-04-acos-candidate-hypotheses.md).
- [24 simulaciones de negocio](2026-10-04-acos-business-simulations.md).
- [Template canónico del Foundry](/Users/davidrodriguez/david-skill-foundry/templates/candidate.md).
- [Reglas y candidate gate del Foundry](/Users/davidrodriguez/david-skill-foundry/AGENTS.md).
