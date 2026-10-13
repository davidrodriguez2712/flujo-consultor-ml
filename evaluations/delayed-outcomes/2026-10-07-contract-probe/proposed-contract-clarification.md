# Aclaración propuesta para futuros contratos temporales

Estado: propuesta posterior a la prueba; no tratamiento ejecutado ni skill instalada.

Distinguir tres campos por fila:

1. outcome_state_at_extraction: observed_negative, observed_positive, pending o unknown; describe lo disponible en la extracción y la semántica de certificación provista.
2. label_availability_at_training: available, unavailable o indeterminate; se compara disponibilidad conocida contra training_timestamp. No usar observed de la extracción como sustituto.
3. train_eligibility: eligible, exclude o indeterminate, derivada del contrato de tarea y de los campos anteriores.

Declarar training_timestamp explícito, punto de vista de cada estado, igualdad <= cuando corresponda y si se admiten positivos antes de cerrar ventana. Si no se conoce certificación o disponibilidad, conservar esa incertidumbre. Una etiqueta observada en extracción posterior puede ser unavailable o indeterminate al entrenar.

Esta propuesta aborda una ambigüedad del autor observada en la ronda, no demuestra una mejora. Para probarla se necesitan cases/expected nuevos fijados antes, sin sobrescribir A–D ni reutilizar sus resultados como evidencia independiente.
