# Contexto

Auditar elegibilidad temporal de filas históricas para entrenamiento supervisado.

# Objetivo

Resolver los inputs sin entrenar ni aprobar gates.

# Tarea

Aplicar las pautas provistas a las filas. Entregar solo JSON con rows (id, eligibility: eligible/exclude/indeterminate, label_state: observed_negative/observed_positive/pending/unknown, reason con evidencia temporal), open_questions (lista) y gate_decision (NEEDS_REVIEW).

# Inputs

inputs.json provisto íntegro. Features históricas disponibles antes de cada prediction_timestamp; no hay duplicados ni otro requisito operacional.

# Restricciones

No entrenar, escribir archivos, aprobar gates, inventar fechas o outcomes. La tarea es auditar; no diseñar otro sistema.

# Criterio de finalización

Una decisión por fila, motivo verificable y preguntas ante información ausente.
