# Protocolo — transferencia de los tres ajustes

## Pregunta y alcance

¿El workflow ajustado mejora el cumplimiento de formato, la fidelidad de reproducción y la continuidad con límites en nuevos expedientes? Se evalúan propuestas/revisiones textuales, no ejecución de pipelines, envío de campañas, gates reales ni eficacia de skills Foundry. Los seis engagements y todos sus permisos son fixtures sintéticos.

## Cobertura

| Caso | Familia | Decisión esperada en el alcance revisado |
|---|---|---|
| T01 | Formato: churn/API | READY; JSON puro y shortlist limitada a revisión. |
| T02 | Formato: pricing/memo | READY; Markdown solicitado, simulación sin causalidad. |
| T03 | Reproducción: inventario/IDs | MUST_CORRECT; repetir writer/reader antes de cambiar representación. |
| T04 | Reproducción: forecast/cambio autorizado | READY; preparar reproducción y variante separadas. |
| T05 | Continuidad: crédito/borrador | READY; draft permitido, ejecución con dependencias. |
| T06 | Continuidad: retención/lanzamiento | MUST_CORRECT; envío bloqueado, preparación permitida. |

Los pares contrastan requisitos que no deben universalizarse: JSON/Markdown, reproducción/cambio explícitamente autorizado, propuesta/ejecución dependiente. No todos tienen el mismo status ni la misma métrica de sobrebloqueo. No contienen el umbral redondeado ni los expedientes de la evaluación previa.

## Condiciones y payloads

Baseline es el snapshot del workflow anterior a los tres ajustes, tomado del treatment congelado del estudio previo. Treatment es el workflow actualizado. Se registran hashes y diff íntegro; no se reconstruye baseline editando a posteriori el actual. Es comparación de las instrucciones del workflow, no de dos releases completas. Templates y MANUAL no se exponen.

Por caso, tarea, artifacts, contrato y contexto son idénticos en ambas ramas. Solo cambia workflow. La diferencia incluye toda la actualización de esas instrucciones, también ejemplos y Definition of Done. Más texto puede afectar costo/comportamiento; no se aísla el efecto de cada sección.

Se proponen doce invocaciones, una por case/condición, sesiones frescas. Orden: T01 baseline/treatment, T02 treatment/baseline y alternar sucesivamente. Un único payload por sesión, sin tools ni contexto privado. La configuración de ejecución y el presupuesto siguen sin fijar. La presencia de un transporte anterior no prueba aislamiento del runtime nuevo.

## Evaluación fijada antes de outputs

1. Transporte y aislamiento, aparte de calidad: los errores de infraestructura no son aciertos ni fallos semánticos; pareja incompleta no comparable.
2. Formato: T01/T03/T04/T05/T06 JSON estricto con schema común; T02 memo Markdown con cinco H2 acordados, estado válido, sin objeto JSON ni fences envolventes. El checker específico de Markdown debe prepararse y verificarse antes de ejecutar. No convertir Markdown solicitado en incumplimiento por no ser JSON. No reparar raw.
3. Estado: expected por caso y bloqueos falsos sobre T01/T02/T04/T05; detectar acción impedida T03/T06.
4. Contenido: cuatro obligaciones y dos prohibiciones por case. Todas obligatorias para content PASS, junto con estado correcto. Aceptar equivalencias semánticas y cálculos equivalentes sin exigir frases. Además, verificar que afirmaciones materiales están sustentadas: toda afirmación material falsa o desviación de alcance implica content FAIL y se registra con cita, fuente y motivo; no aplicar criterio nuevo después de outputs.
5. Referencias: existencia exacta de rutas y soporte semántico son checks distintos. En Markdown la extracción/verificación debe acordarse antes de ejecución; rutas en backticks son válidas. Ningún resultado automático sustituye revisión de contenido.

Formato y contenido separados. Reportar también ambos conformes, sin score ponderado. Revisión local por el mismo autor y con expected conocidos: no independiente ni ciega. Mantener rúbrica, juicios y citas para revisión humana.

## Interpretación exploratoria

Mejora por familia: formato requiere al menos un caso con mejora de formato y sin empeorar contenido en ese caso; reproducción/continuidad requieren al menos un caso con mejora de content PASS. Señal favorable exploratoria requiere mejoras en al menos dos familias, más pares que mejoran en cumplimiento conjunto (formato + contenido) que pares que empeoran, ningún nuevo falso bloqueo sobre casos READY y ninguna nueva violación de alcance. Si no se cumple, resultado mixto/sin ventaja/insuficiente según la matriz, sin modificar la regla después de ver outputs. Fallos de formato son incumplimientos del contrato; violaciones de alcance son acciones o autoridad no permitidas y se reportan por separado.

Una repetición y seis casos no miden variabilidad ni generalización. Si ambas ramas aciertan, no hay mejora incremental acreditada. No comparar scores con el estudio anterior como si fuera el mismo test. No promover Foundry por estos resultados.

## Integridad y gasto

Verificar oracles locales, ensamblaje público de doce payloads, hashes de condiciones y evidencia anterior. Manifest congela preparación, expected y checks; aprobación concreta de paquete y configuración de ejecución se guardan aparte. Precedencia local, no sello externo.

Preparación aprobada por David mediante «apruebo», cero calls/API US$0. Ninguna autorización nueva de gasto. Mantener evidencia anterior, raw de futuros intentos y fallos. Sin retries automáticos. Defectos de fixtures detectados después de outputs requieren conservar versión, detener el par afectado y revisión de versión nueva; no reparar expected en silencio ni reutilizar casos expuestos como inéditos.

## Compatibilidad detectada durante preparación

`scripts/evaluations/workflow_native_transport.py` usa un system prompt que exige JSON. No puede reutilizarse así para T02: el transporte futuro debe seguir el contrato específico del expediente, igual para ambas condiciones. El envelope JSON del CLI es independiente del contenido textual Markdown del modelo. Antes de llamadas: adaptar/verificar ese system prompt, checker Markdown y preservación de raw sin modificar evidencia congelada de rondas anteriores. No usar dos system prompts con distinto grado de ayuda por condición.
