# Decisiones

## Inicialización

Composición confirmada; snapshots experimentales aceptados como provisionales. No se aprobaron gates de negocio ni se ampliaron permisos.

Registrar cambios de alcance/etapa, reviewer, evidencia y fecha antes de avanzar.

## 2026-10-07 — Inicio del piloto sintético

El usuario seleccionó churn/retención y autorizó generar datos. Se compiló el workspace con ambas rutas de runtime y snapshots experimental. Industria de suscripciones, capacidad 50/mes y KPI son supuestos propuestos para revisión; no aprobación humana de negocio.

## 2026-10-07 — Corrección del generador

La versión v0 tenía 535 casos de actividad incompatible con antigüedad, 1173 historias previas al alta y 193 tickets previos al alta. Se corrigieron ventanas y se conservaron los CSV v0 en data/interim/generator-draft-v0. V1 supera checks de coherencia temporal y alta; hashes y checks actualizados. Solo v1 en data/raw es input vigente.

## 2026-10-07 — Primera comparación de design-validation

Baseline y treatment ejecutados con el mismo modelo, prompt e inputs y contextos independientes. Expected fijado antes de ejecutar y no expuesto. Treatment cargó design-validation 0.1.0; baseline no cargó skills. Review local no independiente: no hay evidencia suficiente de mejora consistente; errores temporales en ambos outputs y conteo de train inconsistente en baseline. No se modificó Foundry ni se promovió la capacidad. Ver evaluation/design-validation/review.md.

## 2026-10-07 — Discovery aprobado por David

Respuesta humana «si» a la aceptación de K=50, definición de churn, Precision@50/Recall@50 y reviewer. Evidencia en evidence/approvals/2026-10-07-discovery.md. Gate discovery validado como PASS antes de registrar completed_stages y avanzar a framing. No se aprobó framing ni el diseño temporal nuevo.

El project-profile se conserva como snapshot de intake; sus preguntas iniciales se resuelven mediante state, framing y esta decisión, sin alterar hashes ni composición. El rol de owner operativo es ficticio; David es el reviewer del piloto.

## 2026-10-07 — Framing/protocolo aprobados

David respondió «si apruebo» al contrato y protocolo temporal presentados. Framing validado PASS antes de avanzar a diagnosis; evidencia en evidence/approvals/2026-10-07-framing.md. No se aprobaron gates posteriores.

## 2026-10-07 — Generador v2 tras auditoría

Checks diagnósticos reprodujeron un cancellation_at posterior al corte (12:00 frente a 00:00 del 2026-01-15). Se corrigió la comparación de fecha a estrictamente anterior al día del corte, acorde a horas fijas de la simulación. V1 conservado en data/interim/generator-v1-before-diagnosis. Solo cambió ese campo de una label pendiente; demás CSV y labels observadas idénticos. V2 supera 26 checks; reproducibilidad verificada. Los inputs v1 de la comparación de skills quedan preservados, sin modificar outputs ni expected.

## 2026-10-07 — Diagnosis aprobado y transición a execution

David respondió «arpboado» a la solicitud de aprobar diagnosis/data-quality para avanzar al baseline. Aprobación registrada en evidence/approvals/2026-10-07-diagnosis.md; ambos gates PASS antes de cambiar estado. Estado canónico avanzado a execution; no se aprobaron gates posteriores.

Baseline por grupos: cuatro predictors históricos, imputación del train, suavizado 20 y umbral de caída 50% fijados antes de métricas. No se usaron coeficientes del generador ni tuning. Nueve folds de desarrollo; modelo final fijo al 1 de julio de 2025, sin puntuar test. Results y policy trazables en analysis/outputs/baseline-development. Auditoría y reproducción en baseline-audit.json; review no independiente. Pautas de detect-leakage 0.1.0 aplicadas manualmente: útiles para ordenar revisión, sin evidencia comparativa ni promoción Foundry.

## 2026-10-07 — Execution aprobado y evaluación final

David respondió «aprobado» a la revisión del baseline y autorización de evaluar el modelo congelado. Evidencia en evidence/approvals/2026-10-07-execution.md; execution validado PASS antes de avanzar a validation. Se evaluó una vez julio–diciembre: modelo y policy intactos, sin refit ni tuning. Metadata, scores y resultados preservados en analysis/outputs/holdout-final. Enero excluido. Precision@50 media 10,67%, Recall@50 11,02%, Lift@50 2,52; no causa demostrada para el cambio frente a desarrollo. 105 tests pasan; checks en holdout-audit.json. Revisión no independiente.

El test deja de ser reserva intacta. Cambios guiados por estos resultados necesitarán otro protocolo y datos reservados. Gates de validation y módulos pendientes; no se aprobaron delivery, handoff ni promociones Foundry.

## 2026-10-07 — Validation aprobado; delivery preparado

David respondió «aprobado» a la solicitud de revisar validation y cuatro gates de módulos para preparar delivery. Evidencia en evidence/approvals/2026-10-07-validation.md. Los cinco gates se validaron PASS antes de avanzar. No se alteraron informes aprobados ni artefactos de entrenamiento/evaluación.

Memo en decision/recommendation.md y contrato en delivery/delivery_contract.md: entrega local de laboratorio, baseline sintético y recomendación de piloto real separado. Inventario de hashes en delivery/delivery-manifest.json. Gate delivery pendiente; no se aprobaron handoff, producción, campañas ni promociones del Foundry.

## 2026-10-07 — Delivery aprobado y preparación de handoff

David respondió «aprobado y sigamos» al memo/contrato y autorización de preparar handoff. Evidencia en evidence/approvals/2026-10-07-delivery.md. Delivery validado PASS antes de avanzar. Runbook y feedback local preparados; no se modifica el paquete aprobado de delivery. El inventario de handoff registra artefactos adicionales y estado al preparar revisión. Handoff aún no aprobado; sin cierre, producción, publicación ni promociones Foundry.

## 2026-10-07 — Aprobación final y cierre

David respondió «aprobaod seguimos» a la revisión del runbook/feedback y autorización de cerrar el piloto. Handoff validado PASS antes de registrar COMPLETED y las siete etapas completas. Evidencia en evidence/approvals/2026-10-07-handoff.md. Mantener handoff como current_stage final según contrato V1. Se conserva inventario preparado para revisión; nueva revisión de inventario documenta cierre y cambios autorizados en state/vistas.

Seguimiento: propuestas locales vinculadas a candidates existentes de labels demoradas, selección operacional y síntesis de evidencia. No se modifica Foundry ni se declara promoción. Limitación observada de UX V1: status/next siguen mostrando gate/preguntas de handoff después de cierre; documentar para futura mejora, sin cambiar el producto dentro del cierre del piloto.
