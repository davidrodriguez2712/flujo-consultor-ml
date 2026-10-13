# Contexto

Auditoría de selección operativa en datos ficticios.

# Objetivo

Resolver selección y límites con los inputs; sin ejecutar acciones.

# Tarea

Entregar solo JSON con selected_ids (ordenados), effective_k, metrics {precision, recall, lift} (número o null según identificabilidad en la población requerida), decision (ranking_only o causal_not_identifiable), rationale (lista con evidencia/cálculos), open_questions y gate_decision NEEDS_REVIEW. Usar restricciones de inputs. Las métricas son descriptivas; no estimar efectos de acciones no ejecutadas.

# Inputs

inputs.json provisto completo.

# Restricciones

No entrenar, actuar externamente, escribir archivos ni aprobar gates. No inventar labels, costes o autoridad.

# Criterio de finalización

Selección verificable, denominadores explícitos, límites de inferencia y preguntas cuando falte evidencia.
