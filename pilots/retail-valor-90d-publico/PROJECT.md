# Priorización comercial retail con datos públicos

Decisión: Proponer al inicio de cada mes hasta 100 clientes identificables para revisión comercial, ordenados por ventas positivas esperadas a 90 días.

Problema: Encargo simulado de priorización comercial con capacidad limitada; no existe un cliente contratante ni campaña observada.

Éxito: Ventas positivas futuras registradas en el Top-K, comparadas con baseline sobre la misma población y cutoff.

Owner: Responsable comercial simulado; David revisa los gates del piloto

Ver perfil confirmado en `.acos/project-profile.yaml`.

## Fuente y límites del engagement

Online Retail II: datos públicos reales, históricos y licenciados CC BY 4.0. El encargo y cliente son simulados. Ver provenance en data/source_manifest.json y Discovery en reports/discovery/review.md. No se mide impacto de campaña ni margen.
