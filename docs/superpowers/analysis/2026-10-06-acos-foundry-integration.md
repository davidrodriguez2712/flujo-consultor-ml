# Integración ACOS–Foundry: revisión del 6 de octubre de 2026

**Estado:** revisión documental del inventario y decisiones canónicas; sin ejecutar evaluaciones ni alterar Foundry.

## Resultado actual

- 24 fichas ACOS conservan metadata `status: candidate`; ese campo no reemplaza su decisión humana.
- 18 decisiones son **mantener como conocimiento** y seis son **pendiente (diferido)**.
- Nueve skills operativas están en `experiments/skills/`, todas `experimental 0.1.0`; ocho pueden apoyar trabajos de cliente según fit. `run-skill-eval` sirve al Foundry.
- `evaluate-grounded-assistant`, `reconcile-business-metrics` y `evaluate-document-extraction` se archivaron en `experiments/scratch/`; cases, resultados y snapshots se conservan en Foundry. Las decisiones del 6 de octubre registran ausencia de diferencia material en su primer experimento; no es una prueba de inutilidad universal.
- H06/H19/H20 registran cuatro rondas sin mejora robusta de las extensiones de `design-validation`: se conserva `0.1.0` operativa y las variantes `0.2.0`/`0.3.0` quedan documentadas en snapshots de evaluación. ACOS no selecciona esas variantes archivadas.

## Inventario operativo observado

Hashes SHA-256 del archivo `SKILL.md` leído en esta revisión, no de todo el bundle. Un compiler debe fijar también hashes de recursos seleccionados en cada inicialización; esta tabla no es un lockfile ni el catálogo de selección.

| Skill | Estado | Versión | SHA-256 de SKILL.md |
|---|---|---|---|
| `build-features` | `experimental` | `0.1.0` | `ce9efaf4a7f0a88019d34c8c0ccf3e55d76a1e5396f404def6af4c18d76c6918` |
| `design-validation` | `experimental` | `0.1.0` | `70883c3b75b07334fc95bad1b5c6749fd7b5e623b648f6b48fb6c14b2d32b8f9` |
| `detect-leakage` | `experimental` | `0.1.0` | `2ea060606202840ee4ce49ff27c9beb6b29ffae27edebcf755683e9c9bc99fce` |
| `figma-handoff` | `experimental` | `0.1.0` | `336c88e6b55ee3255ce0548f38ff2b607bee4461144bc23a3d815ae7fde885a9` |
| `research-intelligence` | `experimental` | `0.1.0` | `fd74d764be7e851b3606ecc8796b934f4991f414b67bb3327c0d4bcbe5d66730` |
| `run-skill-eval` | `experimental` | `0.1.0` | `bcfade18ec8cc263d166833e603a97b054202c28ecbcd120347a30b66f520799` |
| `ui-planning` | `experimental` | `0.1.0` | `7297581201d8b82b4a21ca961fa9b6f1420f9bbed4fa2794dce357112a63cf0d` |
| `understand-dataset` | `experimental` | `0.1.0` | `1f21d325cf3e43afd7ea26f1d24214fa734c2562a031bb8263dfdf899521f058` |
| `visual-qa` | `experimental` | `0.1.0` | `f2f45861826a60f4edc8154644f8c03a42b1f22b80ddf70201252fce842884e0` |

## Decisiones de las fichas

| Hipótesis | Ficha canónica | Decisión leída |
|---|---|---|
| H01 | [frame-business-decision](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-frame-business-decision.md) | mantener como conocimiento |
| H02 | [quantify-decision-impact](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-quantify-decision-impact.md) | mantener como conocimiento |
| H03 | [formulate-constrained-decision](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-formulate-constrained-decision.md) | mantener como conocimiento |
| H04 | [design-intervention-evaluation](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-design-intervention-evaluation.md) | mantener como conocimiento |
| H05 | [evaluate-operational-selection](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-evaluate-operational-selection.md) | mantener como conocimiento |
| H06 | [forecast-backtesting](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-forecast-backtesting.md) | mantener como conocimiento |
| H07 | [evaluate-grounded-assistant](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-evaluate-grounded-assistant.md) | mantener como conocimiento |
| H08 | [synthesize-evidence-to-recommendation](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-synthesize-evidence-to-recommendation.md) | mantener como conocimiento |
| H09 | [reconcile-business-metrics](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-reconcile-business-metrics.md) | mantener como conocimiento |
| H10 | [design-entity-resolution](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-design-entity-resolution.md) | pendiente (diferido) |
| H11 | [assess-decision-data-readiness](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-assess-decision-data-readiness.md) | mantener como conocimiento |
| H12 | [evaluate-document-extraction](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-evaluate-document-extraction.md) | mantener como conocimiento |
| H13 | [evaluate-recommendation-policy](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-evaluate-recommendation-policy.md) | pendiente (diferido) |
| H14 | [audit-inherited-solution](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-audit-inherited-solution.md) | mantener como conocimiento |
| H15 | [diagnose-event-log-process](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-diagnose-event-log-process.md) | pendiente (diferido) |
| H16 | [define-agent-action-boundaries](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-define-agent-action-boundaries.md) | mantener como conocimiento |
| H17 | [design-operational-monitoring](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-design-operational-monitoring.md) | mantener como conocimiento |
| H18 | [design-human-review-policy](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-design-human-review-policy.md) | mantener como conocimiento |
| H19 | [evaluate-probability-calibration](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-evaluate-probability-calibration.md) | mantener como conocimiento |
| H20 | [validate-delayed-outcome-targets](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-validate-delayed-outcome-targets.md) | mantener como conocimiento |
| H21 | [design-time-to-event-evaluation](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-design-time-to-event-evaluation.md) | pendiente (diferido) |
| H22 | [estimate-customer-lifetime-value](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-estimate-customer-lifetime-value.md) | pendiente (diferido) |
| H23 | [evaluate-uplift-targeting](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-evaluate-uplift-targeting.md) | mantener como conocimiento |
| H24 | [design-unlabeled-anomaly-review](/Users/davidrodriguez/david-skill-foundry/candidates/2026-10-04-acos-design-unlabeled-anomaly-review.md) | pendiente (diferido) |

## Regla de integración para el compiler

1. Escanear exclusivamente las ubicaciones operativas `experiments/skills/` y `stable/` con metadata válida. No descubrir skills recursivamente en `scratch/`, `evals/`, snapshots, candidates o copias de runtime.
2. Una decisión explícita de mantener como conocimiento, diferir o excluir prevalece sobre coincidencia de nombre y presencia de metadata experimental en un archivo archivado. Revisar conflictos como brecha antes de seleccionar.
3. H07/H09/H12 tienen material de evaluación conservado, pero no una skill operativa seleccionable. H06/H19/H20 no habilitan versiones archivadas de validación.
4. Las necesidades pueden cubrirse con playbooks/templates/gates del OS y revisión humana, declarando cobertura parcial y límites. No presentar esas pautas como skills nativas instaladas ni como conocimiento validado por las simulaciones.
5. Las seis hipótesis diferidas (H10/H13/H15/H21/H22/H24) quedan como oportunidades condicionadas; no son dependencias para construir V1. Su reactivación sigue el trigger de cada ficha, no la mera generación de otro proyecto.
6. El estado exacto y la decisión pertenecen al Foundry. El catálogo de ACOS declara necesidades y compatibilidad, no promueve estados ni modifica las decisiones.

## Evidencia y límites

Se leyeron las secciones de decisión de las 24 fichas, el inventario operativo y las evaluaciones archivadas de H07/H09/H12. No se reejecutaron checks ni se auditaron todas las rondas de `design-validation`; ese resultado se informa como decisión registrada en H06/H19/H20, no como verificación propia.

Las rutas locales de este informe son referencias de trabajo interno. Los proyectos generados no deben contener rutas personales: guardan procedencia relativa al Foundry y snapshots portables. Los documentos del 4 de octubre conservan sus simulaciones y delimitación histórica; esta revisión actualiza su interpretación operativa.
