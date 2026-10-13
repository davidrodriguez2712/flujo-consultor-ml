# Feedback local de capabilities — piloto de churn

Fecha: 2026-10-07. Estado: observaciones para revisión; no evaluación canónica ni promoción Foundry. Las tres skills seleccionadas conservan versión 0.1.0 y madurez experimental.

| Capability | Uso observado | Resultado y evidencia | Límite | Próxima acción propuesta |
|---|---|---|---|---|
| understand-dataset | Aplicación manual de pautas por el asistente | Report estructural, contrato, cardinalidad y disponibilidad; reports/dataset y diagnosis-checks.json | El autor también revisó; sin comparación de skill frente a baseline | Repetir en otro caso, con criterios y reviewer independiente |
| design-validation | Comparación exploratoria con invocación nativa en treatment | Ambos outputs cubren riesgos; treatment más cuidadoso en algunos puntos, ambos con errores de calendario; evaluation/design-validation/review.md | Un caso, sin mejora consistente demostrada; revisión no independiente | Evaluar otros casos y el límite de maduración de labels; conservar originales |
| detect-leakage | Aplicación manual de pautas por el asistente | Reports previos y auditoría de pipeline, checks por fold y exclusión de outcomes | No ejecución comparativa nativa ni garantía de ausencia de leakage semántico real | Añadir review independiente y escenarios que desafíen falsos positivos |

## Brechas observadas

CAPABILITIES.md registra cobertura parcial mediante pautas para framing, síntesis de evidencia, diseño de features, selección operacional y síntesis ejecutiva. El asistente produjo el baseline, memo y runbook; esto no demuestra que exista una skill operativa para esas tareas.

Hipótesis reutilizables a contrastar con los candidates existentes antes de proponer otro artefacto:

1. Contratos temporales con maduración de labels explícita pueden evitar errores de interpretación observados en la comparación.
2. Revisión de priorización bajo capacidad debe distinguir riesgo, valor y respuesta causal, y documentar empates/selecciones repetidas.
3. Síntesis ejecutiva puede necesitar una pauta que preserve lineage, medias mensuales, límites y ausencia de ROI demostrado.
4. La continuidad requiere conservar estado canónico, approvals y snapshots al portar un proyecto; no depende solo del nombre del runtime.

Son hipótesis locales basadas en este caso; no se crean candidates nuevos ni se asume su tipo. La necesidad y revisión del catálogo determinarán si corresponde skill, agent, playbook, template u otra capacidad acordada.

## Disciplina Foundry

Problema o fuente → candidate → experimental → evaluated → validated → stable. El proyecto puede usar experimental con límites visibles según la política aceptada; su aprobación humana no cambia la madurez de la capacidad. Revisar y anonimizar evidencia antes de trasladarla al Foundry. No se modificó el Foundry ni los snapshots del proyecto.
