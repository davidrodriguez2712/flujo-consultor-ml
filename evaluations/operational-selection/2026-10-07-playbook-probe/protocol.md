# Preregistro — selección bajo capacidad

Prueba exploratoria documental autorizada como continuación: baseline playbook actual experiments-and-models; treatment mismo playbook más pauta v0.1. Candidate canónico evaluate-operational-selection permanece como conocimiento; no se reabre ni se crea skill. Objetivo: detectar si las pautas actuales fallan en capacidad/empates/labels e identificar si basta una pauta.

Cuatro cases, dos contextos nuevos por case, claude-sonnet-5-5 effort medium, safe-mode, sin herramientas/MCP, sin persistencia. Expected fuera de prompts y criterios fijados antes. Orden alternado A/C baseline primero, B/D treatment primero. Un run por condición; no repetir por mala calidad. Fallos de infraestructura se conservan aparte.

Checks separados: selección exacta, K efectivo, números con tolerancia 1e-8 o null, decisión causal, NEEDS_REVIEW. Review semántica de rationale y preguntas por el autor, no independiente. Formato fences se reporta por separado. No score compuesto, promoción o eficacia general por esta prueba. No se usan outputs del holdout de churn ni datos reales.
