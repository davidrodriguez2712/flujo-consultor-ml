# Storyline propuesta — revisión de validation

Audiencia: equipo ficticio de retención y decisor de negocio. Reviewer: David Rodríguez. No es un entregable publicado ni aprobado para cliente.

1. Decisión: con 50 revisiones al mes, priorizar clientes activos con mayor riesgo de churn.
2. Evidencia: fixture sintético, diagnóstico y protocolo temporal aprobados; evaluación de modelo fijo en seis meses de holdout.
3. Resultado: Precision@50 media 10,67% versus 4,28% aleatorio esperado; Recall@50 11,02%; Lift@50 2,52. 32 positivos en 300 selecciones cliente-mes. Describir variación mensual, no solo media.
4. Advertencia de interpretación: Precision menor que desarrollo; no atribuir causa demostrada. No hay evidencia de beneficio de contactar ni generalización real.
5. Recomendación provisional: usar este caso para revisar el funcionamiento del OS; validar con fuentes reales y diseñar una prueba de intervención antes de justificar una campaña o inversión.
6. Próxima decisión: aceptar evaluación y límites para preparar decision memo y handoff del laboratorio. Ningún gate futuro se aprueba automáticamente.

Fuentes: validation/model_validation.md, modeling/model_brief.md y analysis/outputs/holdout-audit.json. Sin ROI, ahorro, margen recuperado o uplift inventados. Gate executive_delivery-review pendiente.
