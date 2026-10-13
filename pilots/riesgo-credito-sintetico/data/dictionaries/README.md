# Diccionario y contrato temporal del fixture

Versión del generator: 0.1.0. Datos 100% sintéticos. Fechas ISO de resolución diaria; comparación inclusiva `available_at <= cutoff`. Extract: 2026-01-15. Una fila por solicitud en cada tabla; join 1:1 por `application_id`. No unir únicamente por cliente porque tiene varias solicitudes.

| Tabla | Campos | Uso y disponibilidad |
|---|---|---|
| applications.csv | application_id, customer_id, scoring_at | Identificadores de solicitud/cliente; instante propuesto de scoring |
| applications.csv | monthly_income, debt_to_income, requested_amount, bureau_score | Inputs ficticios declarados disponibles al scoring; cantidades en unidades monetarias ficticias. bureau_score 300–850 es una escala arbitraria del laboratorio |
| history.csv | application_id, customer_id, snapshot_at, available_at, prior_late_count | Resumen de antecedentes ficticio, snapshot 10 días antes y disponible 2 días antes del scoring. No se deriva de un ledger de préstamos anterior |
| decisions.csv | application_id, decision_at, decision, funded_amount, disbursed_at | Decisión histórica simulada al día siguiente; desembolso ese día si approved. No disponibles al scoring |
| outcomes.csv | application_id, extract_at, disbursed_at, window_end, label_available_at, label_status, target_30dpd_90d | Contrato de target descrito debajo; contiene información posterior. Usar como label y metadatos de elegibilidad, no features |
| post_decision.csv | application_id, available_at, max_dpd_90d | Máxima mora del horizonte observado. Leakage deliberado: revela el target y solo está disponible después del horizonte |

## Target y maduración

`target_30dpd_90d=1` significa que se alcanzaron 30 días de mora dentro del horizonte de 90 días desde desembolso; 0 significa que no. `window_end=disbursed_at+90 días`. Por simplificación, tanto positivos como negativos completos se publican al día 97; no hay detección positiva anticipada. El generator simula ese indicador y una máxima mora consistente, no un calendario completo de cuotas/pagos.

- `observed`: crédito concedido, label disponible al extract; target 0/1.
- `pending`: crédito concedido, día 97 posterior al extract; target vacío. `label_available_at` es la fecha programada por el contrato, no evidencia de recepción futura.
- `not_observed_rejected`: no se desembolsó; target, ventana y disponibilidad vacíos. No es un negativo ni un outcome contrafactual.

Los campos de `post_decision` permanecen vacíos en pendientes y rechazadas. Para un cutoff histórico debe volver a comprobarse disponibilidad; un target observado al extract puede no haber estado disponible al entrenar.

## Supuestos y límites

24 meses, 300 solicitudes/mes, 1.800 identidades posibles y clientes recurrentes. Propensión latente por cliente no exportada. La concesión depende de bureau_score y debt_to_income con ruido; por eso el conjunto con labels está seleccionado. Los outcomes usan una regla probabilística ficticia con ligero cambio temporal. No existen tratamientos aleatorios, efecto de revisión, LGD observada ni ahorro identificable.

El conocimiento de la fórmula del generator sirve para auditar el fixture, no para introducir variables latentes, elegir el modelo usando holdout ni demostrar eficacia de las skills. La capacidad 100/mes limita propuestas de revisión, no garantiza que llenar 100 sea óptimo.
