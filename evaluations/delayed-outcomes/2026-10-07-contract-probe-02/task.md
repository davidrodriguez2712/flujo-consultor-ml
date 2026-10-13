# Tarea común de auditoría temporal

Contexto ficticio. Clasifica cada fila para un entrenamiento histórico con los inputs provistos. No entrenes, actúes o apruebes gates. Devuelve únicamente un objeto JSON con rows, open_questions y gate_decision (NEEDS_REVIEW). rows debe ser un array de objetos, uno por fila con id string único; open_questions debe ser un array de strings no vacíos (o []). Cada fila contiene exactamente los campos siguientes: id, outcome_state_at_extraction (observed_positive/observed_negative/pending/unknown), label_availability_at_training (available/unavailable/indeterminate), train_eligibility (eligible/exclude/indeterminate), reason (justificación breve que permita verificar reglas y timestamps). No agregues campos.

El estado del outcome se refiere a la extracción; la disponibilidad, al entrenamiento; la elegibilidad, al uso de la fila en ese entrenamiento. Usa las reglas de negocio provistas. Si un dato no permite decidir, identifica lo que falta. Las preguntas abiertas pueden ser una lista vacía. No inventes reglas o fechas. El dato target_reported es el valor registrado en el sistema, no una declaración de certificación. La tarea no pide descubrir el esquema de respuesta sino razonar sobre sus inputs.

Precisiones comunes: comparar instantes tras normalizar sus offsets, con precisión de segundos. Sumar N días significa N × 24 horas.
