# Contexto

Preparar decision memo ejecutivo de laboratorio con fuentes ficticias provistas, sin buscar afuera.

# Objetivo

Corregir borrador y proponer acción proporcionada a evidencia.

# Tarea

Entregar solo JSON: recommendation (texto), claims (lista de statement y evidence_ids válidos), draft_claim_review (una fila por draft id con status supported/unsupported/contradicted, reason y evidence_ids), numeric_findings (campos requeridos en inputs; números o null cuando no identificable), limitations (lista), next_action {owner,action}, gate_decision NEEDS_REVIEW. Supported: evidencia respalda claim. Contradicted: evidencia lo refuta aritmética o lógicamente. Unsupported: falta evidencia suficiente para afirmarlo, aunque no se pruebe falso. Ratios en fracción 0–1; campos _pp en puntos porcentuales; _pct en porcentaje.

# Inputs

Inputs provistos íntegros. Usar E1/E2/E3 como referencias de fuentes locales ficticias.

# Restricciones

No inventar fuentes, facts, plazos, presupuestos o permisos. No entrenar, escribir, publicar, actuar o aprobar gates. La acción es propuesta para review.

# Criterio de finalización

Memo condicionado, claims trazables y claims del borrador clasificados; cálculos y límites reconciliados, acción con owner provisto.
