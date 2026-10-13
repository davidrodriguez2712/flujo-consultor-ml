# Continuación después del piloto de churn

Fecha: 2026-10-07. Propuesta de trabajo posterior; piloto cerrado por aprobación de David. No modifica el Foundry ni promete madurez de capacidades.

## Orden propuesto

| Prioridad | Iniciativa | Evidencia del piloto | Primer artefacto propuesto | Condición para avanzar |
|---|---|---|---|---|
| 1 | Maduración de labels y targets demorados | Errores de calendario en baseline/treatment de design-validation; correcciones comprobadas | Contrato/gate temporal o extensión de skills existentes | Comparar con pautas actuales antes de justificar una skill nueva |
| 2 | Selección bajo capacidad | Top 50, empates y riesgo distinto de beneficio causal | Playbook/template de evaluación de selección | Demostrar cobertura y mejora en otros casos |
| 3 | Evidencia a recomendación | Memo trazable generado manualmente; cobertura parcial del catálogo | Playbook/template de delivery | Comparar recomendaciones con y sin pauta, con criterios previos |
| 4 | Portabilidad y cierre de CLI | Windows pendiente; next/status muestran handoff aun cerrado | Recorrido Windows y propuesta de UX de cierre | Ejecución nativa y diseño revisado antes de cambiar comportamiento |
| 5 | Piloto real | Todo el fixture es sintético; no campañas | Intake y protocolo de otro proyecto | Datos reales, permisos, owner y decisión disponibles |

## Candidates existentes relacionados

Rutas canónicas relativas a David Skill Foundry:

- candidates/2026-10-04-acos-validate-delayed-outcome-targets.md: candidate; propone gate/contrato o extensión, con solapamiento explícito con understand-dataset/design-validation.
- candidates/2026-10-04-acos-evaluate-operational-selection.md: candidate; comparar políticas de selección bajo capacidad, sin confundir riesgo con efecto de intervención.
- candidates/2026-10-04-acos-synthesize-evidence-to-recommendation.md: candidate; playbook/template primero, sin reactivar automáticamente capacidades retiradas.

Se revisaron estas fichas en modo lectura. Son hipótesis; no se les añade retrospectivamente eficacia ni recurrencia real. Este piloto puede aportar evidencia sintética de contexto y fallos observados de outputs, no mejora repetida ni proyectos reales. No crear fichas duplicadas.

## Primer paquete de evaluación propuesto: disponibilidad temporal

Objetivo: comprobar si el tratamiento de maduración mejora respecto de las pautas actuales y qué forma de artefacto necesita. Casos hipotéticos, no ejecuciones realizadas:

| Caso | Inputs que deben fijarse antes | Comportamiento esperado |
|---|---|---|
| A — Label madura después del scoring | Ventana mensual, label_available_at y training_timestamp | Excluir del train aunque observed en extracción posterior |
| B — Label disponible justo al cutoff | Timestamps precisos y regla <= confirmada | Incluir en train conforme al contrato, sin inventar otro embargo |
| C — Outcome todavía pendiente | Extract timestamp, horizonte incompleto y etiqueta vacía | Mantener pending, no completar con negativo |
| D — Delay desconocido | Target y timestamps insuficientes | Declarar No determinable y solicitar regla de disponibilidad |

Comparar baseline usando capacidades actuales con un tratamiento mínimo de contrato/gate o extensión. Fijar prompt, inputs, expected y checks antes de ejecutar. Misma configuración, contextos separados, resultados conservados; incluir desafíos de falsos positivos y escenarios de otra industria sin asumir generalidad.

Criterios: disponibilidad exacta, pendientes, ventana del target, trazabilidad, reconocimiento de información ausente y ausencia de autoridad para avanzar gates. Medir errores concretos, duración/coste si disponibles y límites; no depender solo de juicio del autor. Solicitar review independiente antes de decidir suficiencia de evidencia para Foundry.

## Cambios y límites de aprobación

Los próximos casos no son reevaluaciones del modelo de churn ni deben aprovechar su test observado para seleccionar mejoras. La elección del artefacto sigue abierta. candidate → experimental → evaluated → validated → stable aplica a capacidades, no a etapas del engagement. Usar experimental con límites visibles continúa permitido; promoción requiere la disciplina canónica del Foundry.

El piloto cerrado no autorizó publicar paquete, instalar globalmente, transferir datos ni promover skills. La mejora de UX de cierre y nuevas capacidades requieren trabajo propio; este documento registra una propuesta revisable.

## Resultado de la continuación — disponibilidad temporal

La ronda exploratoria se ejecutó: cuatro casos, ocho outputs evaluables. Ambas condiciones acertaron 9/9 decisiones de elegibilidad; sin ventaja observada del suplemento. Estado de label en extracción frente al cutoff resultó ambiguo en la tarea: se preservan expected y mismatches, sin atribuirlos a eficacia. [Informe de la ronda](2026-10-07-delayed-outcomes-probe-report.md).

Recomendación actual: mantener candidate como conocimiento y no crear skill duplicada. Aclaración de contrato propuesta, no probada. Siguiente prioridad del roadmap: selección operacional bajo capacidad.

## Instalación persistente y selección operacional completadas

ACOS 0.1.0 instalado con uv y accesible por PATH; se verificó desde otra carpeta y con copia del proyecto fuera del checkout. [Evidencia](2026-10-07-persistent-install-checks.json).

Prueba de selección operacional: cuatro cases y ocho ejecuciones. Baseline cubre decisiones; suplemento sin ventaja, con fallos de orden/campo estructurado. [Informe](2026-10-07-operational-selection-probe-report.md). Candidate permanece como conocimiento; no cambia Foundry. Siguiente prioridad propuesta: síntesis de evidencia a recomendación.

## Síntesis de evidencia a recomendación evaluada

Cuatro casos, ocho ejecuciones. Ambas condiciones correctas en 12/12 campos numéricos y límites sustantivos de las recomendaciones; dos diferencias de taxonomía por condición, sin ventaja del suplemento. [Informe](2026-10-07-evidence-to-recommendation-probe-report.md).

Las tres prioridades de capacidades ya tienen rondas exploratorias; no se propone nueva skill ni promoción. ACOS instalado. Pendientes siguientes: UX de cierre de CLI, Windows nativo, review independiente y piloto real cuando existan datos/contexto. No se modifica el Foundry.


## UX de cierre de CLI implementada

Diseño aprobado e implementado: los cierres válidos no muestran gates ni outputs pendientes. Los cierres inconsistentes exponen hallazgos y devuelven BLOCKED. Cinco pruebas de regresión nuevas; 97 pruebas del producto y 13 del piloto pasan. Herramienta local reinstalada; comprobación fuera del checkout sin modificaciones a la copia del piloto. Los 13 archivos del inventario final y los 35 del delivery conservan sus hashes. [Evidencia](2026-10-07-closure-cli-checks.json).

Esta mejora completa la parte de UX de la prioridad 4. Permanecen pendientes Windows nativo, revisión independiente de las evaluaciones y un piloto real cuando existan datos/contexto disponibles. No cambia el Foundry ni la madurez de sus capacidades.


## Segunda revisión por agentes completada

Tres revisores en contextos separados recalcularon checks y auditaron los outputs. Confirmaron números y consistencia actual de archivos; señalaron problemas de justificación, criterios ambiguos, casos guiados y trazabilidad incompleta de configuración/preregistro. [Informe consolidado](2026-10-07-independent-probe-review.md). Se corrigieron los resúmenes; no se alteró la evidencia original ni el Foundry.

La revisión por agentes completa una segunda lectura separada del autor, pero la revisión humana externa sigue pendiente. No se justifica una skill nueva ni promoción. Windows nativo y piloto real siguen pendientes. Precisar contratos y registrar mejor las ejecuciones son propuestas para una ronda futura, no resultados obtenidos.

## Contratos documentales definidos

Diseño aprobado y cuatro contratos locales documentados: [temporal](../evaluation-contracts/temporal-labels.md), [selección](../evaluation-contracts/operational-selection.md), [evidencia](../evaluation-contracts/evidence-and-claims.md) y [ejecución](../evaluation-contracts/execution-provenance.md). Incluyen campos propuestos, ejemplos y criterios de aceptación. [Índice y uso](../evaluation-contracts/README.md).

Este paso completa la definición documental, no su implementación ni una nueva evaluación. Los documentos tienen versión `0.1.0` y estado propuesto; no alteran la versión del producto o la madurez del Foundry. La evidencia original y el piloto cerrado se conservan. Siguiente paso propuesto: diseñar un protocolo acotado con cases y expected nuevos, revisar sus criterios y aprobarlo antes de ejecutar.

## Nueva ronda temporal completada

Pregunta y diseño aprobados; seis cases nuevos, dos repeticiones por condición y 24 calls. Expected y checker revisados antes del freeze. Checks reproducidos y dos reviewers de outputs separados del autor. [Resultado](2026-10-07-temporal-contract-round-02-report.md).

Ambas ramas aciertan todas las decisiones estructuradas evaluables. Un baseline malformado deja dos filas no evaluables; conservarlas en denominador sin interpretarlas como clases erróneas. Treatment muestra menos preguntas redundantes y una diferencia pequeña de formato, sin eficacia temporal superior demostrada. No crea ni promueve skills ni cambia el compiler.

Siguiente mejora propuesta: aislar cumplimiento de schema en el runner de evaluaciones; ampliar evidencia si se quiere afirmar mejora del contrato. Review humana externa, Windows nativo y piloto real siguen pendientes. Los otros contratos permanecen propuestos, sin ronda específica ejecutada.
