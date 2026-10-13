# Contratos para futuras evaluaciones

Versión documental: `0.1.0`. Fecha: 2026-10-07. Estado: **propuesto, local, sin evaluación de eficacia**. Diseño y creación autorizados por el usuario.

Estos contratos precisan tareas y criterios de futuras rondas exploratorias. Responden a los problemas de la [segunda revisión](../validation/2026-10-07-independent-probe-review.md). Son documentos del proyecto ACOS: no son skills, agents, schemas ejecutables ni gates instalados en el compiler. Su versión no cambia la versión del producto ni el estado de ninguna capacidad del Foundry.

## Catálogo

| Contrato | Cuándo utilizarlo | Qué debe quedar explícito |
|---|---|---|
| [Temporal](temporal-labels.md) | Labels demoradas o datos temporales | Instantes, certificación, disponibilidad y elegibilidad |
| [Selección](operational-selection.md) | Ranking y capacidad limitada | Población, restricciones, orden, métricas e identificación causal |
| [Evidencia](evidence-and-claims.md) | Memo o recomendación sustentada | Proposición exacta, premisas, referencias y condiciones de cambio |
| [Ejecución](execution-provenance.md) | Cualquier comparación baseline/treatment | Criterios previos, payload, configuración, outputs y checks reproducibles |

Los ejemplos son ilustrativos; no constituyen una ronda ejecutada, resultados de mejora ni expected ya aprobados para un experimento. Los campos constituyen una propuesta de contrato documental, no una interfaz pública implementada. Los criterios de aceptación describen verificaciones que deberán implementarse o realizarse en otra ronda.

## Cómo preparar una ronda

1. Formular la hipótesis y la decisión que la evidencia permitiría tomar. Seleccionar únicamente los contratos pertinentes, más el de ejecución.
2. Preparar cases, inputs y expected nuevos. Usar los ejemplos como referencia de estructura; no como prueba de generalidad.
3. Fijar el contrato de tarea y formato común a ambas condiciones. Precisar qué contenido adicional recibe treatment. Si se prueba el propio contrato como suplemento, documentar esa diferencia y evaluar con criterios comunes externos.
4. Revisar el expected antes de ejecutar: estado temporal, población, unidades, proposición y criterios de fallo deben ser inequívocos. Resolver contradicciones del case; no adelantar sus respuestas particulares en los inputs.
5. Aprobar el protocolo concreto y conservar el preregistro. Ejecutar con payloads separados y sin acceso a expected.
6. Aplicar checks y revisión semántica por separado; registrar resultados estrictos y diagnósticos tolerantes sin mezclarlos.
7. Solicitar revisión separada del autor y presentar la recomendación a la persona responsable.

Las rondas originales permanecen cerradas. Una corrección del criterio produce una nueva versión del case y del expected, con motivo y vínculo a la anterior. No recalificar la ronda anterior silenciosamente ni reutilizar su resultado como evidencia de la nueva versión.

## Cobertura pendiente

La ronda 03 incluyó decisiones positivas justificadas, información insuficiente, fuentes contradictorias y expedientes menos guiados. Su resultado figura abajo. Sigue pendiente ampliar evidencia con procesos y datos reales; una sola respuesta correcta no demuestra mejora repetida.

La necesidad observada determinará si basta conocimiento, contrato, template, playbook, skill o agent. Cualquier incorporación al compiler o traslado al Foundry requiere su trabajo y revisión correspondientes. Cada protocolo nuevo requiere su diseño y autorización propios; la existencia de estos documentos no autoriza otra ejecución.

## Primera ronda con el contrato temporal

La [ronda 02](../validation/2026-10-07-temporal-contract-round-02-report.md) se diseñó, aprobó y ejecutó después de crear estos documentos: seis cases nuevos y 24 calls. No mostró una ventaja en decisiones temporales evaluables; sí señales exploratorias de entrega estructurada y lectura. El contrato conserva estado propuesto. No extrapolar este resultado a los otros tres contratos ni presentarlo como eficacia general demostrada.

## Runner ejecutable para futuras rondas

El [runner temporal 0.2.0](structured-runner.md) y su schema común 0.1.0 ya existen como utilidad del checkout. Dos calls nativos de un case reutilizado comprobaron transporte, validación y separación del contenido; ver [informe técnico](../validation/2026-10-07-structured-runner-v02-report.md). Esto no convierte los contratos documentales en capacidades instaladas ni demuestra ventaja de treatment.

## Ronda 03 con runner común

La [ronda 03](../validation/2026-10-08-temporal-contract-round-03-report.md) ejecutó 24 calls aprobados sobre seis escenarios nuevos. Ambas condiciones acertaron 108/108 campos y 36/36 decisiones: no se demostró ventaja temporal. La revisión del autor halló dos outputs baseline con preguntas problemáticas frente a cero en treatment; señal secundaria exploratoria, sin promociones ni nuevas capacidades. Revisión humana de las conclusiones pendiente.

## Selección operacional, extensión y ronda 02

La [propuesta local 0.2.0](operational-selection-0.2.0.md) añade selección pequeña indivisible con costes variables al alcance Top-K del contrato 0.1.0. El [runner específico](selection-runner.md) separa estructura y contenido. La [ronda 02](../validation/2026-10-08-operational-selection-round-02-report.md) completó 24 llamadas: ambas condiciones coinciden en los campos comprobados de sus 12 outputs. Review del autor y agente separado hallan afirmaciones adicionales discutibles en ambas ramas. Sin mejora decisional demostrada ni nuevas skills/promociones; revisión humana de conclusiones pendiente.
