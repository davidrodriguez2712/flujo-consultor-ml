# Feedback de capacidades — aplicación manual

| Capacidad | Versión/estado | Tarea | Observación local |
|---|---|---|---|
| understand-dataset | 0.1.0 / experimental | Revisar tablas y grain | Estructuró keys, missing, fechas y fan-out con evidencia; el diccionario previo evitó inventar semántica |
| design-validation | 0.1.0 / experimental | Proponer validación según uso | Estructuró propósitos/cutoffs/poblaciones; se usó disponibilidad individual y no una regla automática de embargo |
| detect-leakage | 0.1.0 / experimental | Auditar fuentes y diseño previo | Permitió separar columnas posteriores confirmadas, riesgos de pipeline no construido y overlap de clientes permitido |

No hubo tratamiento/control, medición de mejora ni nueva ejecución nativa para estas tareas. Los reportes y checks son evidencia de aplicación, no eficacia incremental ni autoridad de promoción. No modifica Foundry.

Tensión textual a conservar como observación, no fallo medido: el checklist de detect-leakage dice que compartir entidades entre particiones implica contaminación, mientras sus reglas y design-validation exigen considerar el escenario. Aquí hay 289 clientes compartidos y recurrentes permitidos; el reporte interpreta overlap como diagnóstico, no prueba automática de leakage. Una futura evaluación puede verificar si esa redacción causa falsos positivos antes de proponer ajuste de la skill.

También se identificó un límite del flujo: Top-K mensual retrospectivo no representa revisión de solicitudes al llegar. Mantener como conocimiento local mientras no haya necesidad repetida y procedimiento verificable que justifiquen candidate. No crear fichas duplicadas automáticamente.
