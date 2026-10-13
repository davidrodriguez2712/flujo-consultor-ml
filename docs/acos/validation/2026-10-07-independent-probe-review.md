# Segunda revisión de las evaluaciones exploratorias

Fecha: 2026-10-07. Status: revisión por agentes completada; revisión humana externa pendiente.

## Alcance e independencia

Tres revisores separados recibieron contextos nuevos, sin heredar la conversación del autor, y auditaron una ronda cada uno en modo de solo lectura. Revisores: `/root/review_temporal_probe`, `/root/review_selection_probe` y `/root/review_delivery_probe`. El coordinador contrastó los hallazgos con los artefactos antes de consolidarlos. La separación reduce el sesgo del autor, pero los agentes no son revisores humanos externos ni ofrecen independencia institucional. El coordinador sigue siendo el autor original; su síntesis no sustituye los juicios separados.

No se ejecutaron nuevas llamadas de baseline/treatment. No se cambiaron inputs, expected, suplementos, outputs o checks originales. No es una evaluación canónica del Foundry ni una decisión de madurez. Las recomendaciones siguen sujetas a autoridad humana.

## Resultado ejecutivo

| Ronda | Resultado recalculado | Hallazgo principal | Propuesta |
|---|---|---|---|
| Disponibilidad temporal | Elegibilidad 9/9 por condición; mismatches literales de estado 3/2 | Instante de `label_state` ambiguo; D baseline inventa un intervalo | Mantener conocimiento; definir instantes antes de otra prueba |
| Selección operacional | Baseline 4/4; treatment 3/4 en orden y decision, 4/4 en otros checks | Orden incorrecto en C; campo D ambiguo; inputs anticipan respuestas | Mantener conocimiento; precisar contrato sin recalificar esta ronda |
| Evidencia a recomendación | Números 12/12 y statuses literales 10/12 por condición | C1 confunde certeza y efecto; lineage incompleto en ambas ramas | Mantener conocimiento; precisar claims y referencias por premisa |

No se observó beneficio diferencial suficiente para justificar una skill nueva o promover una capacidad. Esto no demuestra equivalencia entre condiciones ni que los suplementos sean inútiles en otros proyectos.

## Hallazgos del revisor temporal

### Media — decisión correcta con motivo no respaldado

[D baseline](../../../evaluations/delayed-outcomes/2026-10-07-contract-probe/D/baseline.md) afirma que la disponibilidad «queda entre 2025-06-30 […] y 2025-07-15». No hay regla de certificación ni delay que permita fijar ese intervalo. `indeterminate` es correcto, pero el motivo no es enteramente correcto. La review original ya advertía este problema; el resumen lo omitía. Se corrigió esa afirmación en el informe de la ronda, no en el output.

### Media — estado sin instante de referencia

A2/B2 admiten interpretar `pending` al cutoff y `observed_negative` en extracción posterior. D añade desconocimiento de disponibilidad. Los 3/2 mismatches son una comparación literal reproducible, no una medición fiable de superioridad. No se cambia expected. Para una prueba futura, separar estado en extracción y disponibilidad para entrenamiento.

### Baja — cutoff y training_timestamp

B formula la regla con `training_timestamp` pero entrega `cutoff`. Ambas respuestas condicionan la equivalencia. Los resultados son correctos bajo la interpretación prevista; proporcionar ambos conceptos inequívocamente en otro caso.

## Hallazgos del revisor de selección

### Media — tareas guiadas

[C inputs](../../../evaluations/operational-selection/2026-10-07-playbook-probe/C/inputs.json) explicita «null no significa negativo»; D entrega la falta de identificación causal. No se encontró expected documental en los prompts, pero varios comportamientos esperados ya están prescritos por los inputs. La comparación prueba ejecución de esas tareas; no aísla el aporte del playbook ni demuestra cobertura en tareas abiertas.

### Baja — representación frente a causalidad

[C treatment](../../../evaluations/operational-selection/2026-10-07-playbook-probe/C/treatment.md) devuelve H1,U1 pese a scores U1=0,99 y H1=0,80: fallo real de orden, con miembros y K correctos. D devuelve `ranking_only` y niega la identificación causal en texto. El esquema permite dos conceptos coexistentes sin definir precedencia. El mismatch de D permanece como discrepancia literal, no como afirmación causal falsa.

### Baja — representatividad y población

C treatment afirma que los inspeccionados «no son una muestra representativa», aunque se desconoce el mecanismo. Lo sustentado es que no puede asumirse representatividad. D dice «K=2 clientes elegibles» con tres filas elegibles: separar capacidad y tamaño de población en futuras versiones del caso. Las métricas recalculadas A/B/D son respectivamente (0,5;0,5;1), (0,5;1;1) y (0,5;0,5;0,75); C conserva null. Las cotas adicionales de C baseline son aritméticamente correctas.

## Hallazgos del revisor de delivery

### Media — certeza distinta de signo del efecto

[C inputs](../../../evaluations/evidence-to-recommendation/2026-10-07-template-probe/C/inputs.json) plantea «Está demostrado que la intervención aumenta conversión», mientras E1 niega evidencia concluyente. Ambos outputs usan `contradicted`, defendible para la afirmación de certeza; expected exige `unsupported`, pensando en el efecto desconocido. El revisor considera defectuoso ese criterio para C1. A1 es distinto: exposición no refuta lógicamente recuperación futura. No se corrige expected retrospectivamente ni se reemplaza 10/12 por otra cifra; se registra el problema del criterio.

### Media — referencias incompletas en ambas condiciones

El umbral de quejas de 2 pp está solo en `context`. C baseline cita E2; [C treatment](../../../evaluations/evidence-to-recommendation/2026-10-07-template-probe/C/treatment.md) cita E2/E3. Ninguna referencia incluye el umbral. El cálculo de 6 pp y la recomendación de no escalar tienen respaldo en el conjunto de inputs, pero la trazabilidad por IDs es incompleta en ambas ramas. Validar que un ID exista no verifica todas las premisas.

### Media — condiciones futuras y sesgo

B baseline y treatment admiten reconsiderar con medición previa o experimento; una medición previa aislada no identifica causalidad. D sugiere sesgo al alza sin demostrar dirección y baseline declara no representatividad como hecho. Las recomendaciones actuales rechazan escalamiento/extrapolación, pero sus fundamentos y condiciones futuras necesitan esos matices. No son fallos numéricos ni evidencia de ventaja de una rama.

### Baja — lectura y formato

A treatment pregunta por un período ya proporcionado. Solo una de ocho respuestas de delivery cumple JSON puro; todas las de temporal/selección incluyen fences. El parseo tolerante permitió evaluación, pero no constituye conformidad literal de formato. Los checks ya preservaban esta distinción.

## Integridad y límites de procedencia

Los revisores comprobaron 24 hashes de inputs congelados por ronda, y 57/52/52 del manifest temporal/selección/delivery. El coordinador verificó nuevamente los 161 hashes de manifests y los 24 pares raw/Markdown, con 24 sesiones distintas exitosas. Costes y tiempos reportados coinciden con metadata. [Registro de comprobaciones](2026-10-07-independent-probe-review-checks.json).

Los hashes demuestran consistencia actual, no prueban por sí mismos que los criterios existían antes de ejecutar. No se conservaron runner/checker, comandos exactos, versión CLI ni registro de configuración efectiva suficiente para reproducir toda la ejecución. La declaración de congelación previa y los flags de ejecución están parcialmente corroborados, pero no acreditados íntegramente por el paquete. No se encontró evidencia contradictoria ni expected documental incrustado.

Una ejecución por condición/caso, un modelo y fuentes sintéticas cortas no prueban generalidad, significancia, eficacia causal ni mejora repetida. Los tiempos de pared de metadata y `duration_ms` del proveedor son magnitudes distintas; no inferir ahorro por estas diferencias.

## Acciones realizadas y pendientes

Realizado: segunda revisión separada; comprobaciones de integridad; corrección de resúmenes y documentación explícita de límites. La evidencia original, piloto cerrado y Foundry se mantienen sin modificaciones.

Propuestas para otra ronda, todavía no ejecutadas: fijar estados temporales, separar tipo de output de identificación causal, asignar IDs a contratos/guardrails y verificar soporte por premisa. Añadir decisiones positivas justificadas y casos menos guiados, conservar runner/configuración y medir formato estricto antes de congelar criterios nuevos. No reutilizar expected corregidos silenciosamente ni presentar esos cambios como resultados de esta ronda.

Pendientes del proyecto: revisión humana externa, Windows nativo y piloto real con contexto y datos disponibles. El Foundry conserva su estado canónico; estos informes no autorizan creación, traslado o promoción automática de capacidades.

## Seguimiento documental

Después de aprobar su diseño se documentaron los [cuatro contratos propuestos](../evaluation-contracts/README.md). Son una respuesta a los hallazgos, con ejemplos y criterios para otra ronda. No se ejecutaron ni se incorporaron al compiler; no modifican los criterios o resultados de las rondas revisadas.
