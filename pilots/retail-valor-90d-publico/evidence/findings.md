# Diagnosis — revisión humana pendiente

Framing aprobado por David; fuentes, snapshots y contratos históricos intactos.

## Hallazgos

- 788.187 líneas válidas, 5.852 clientes, 41 países; GBP 17.124.926,23 en el alcance definido.
- Top-1 concentra 3,39%; Top-10 16,09%; Top-100 37,56% de ventas válidas históricas. 4.234 clientes tienen más de una factura observada.
- 19.165 líneas de cancelación tras reconciliación; importe firmado GBP -1.465.303,66, auditado aparte. No derivar ventas netas sin vinculación fiable.
- Sensibilidad de una fila por patrón: 11.610 líneas menos y -0,329% de ventas; mismos 5.852 clientes. No cambiar la regla aprobada ni afirmar robustez de cada ranking.
- Anónimos y códigos no estándar conservan las exclusiones/cobertura documentadas en Framing; no convertirlos en clientes artificiales.

## Evaluación propuesta

| Uso | Cutoff | Clientes elegibles | Snapshots train maduros |
|---|---|---:|---:|
| Development | 2010-09-01 | 2.822 | 1 |
| Development | 2010-12-01 | 3.465 | 4 |
| Development | 2011-03-01 | 3.338 | 7 |
| Development | 2011-06-01 | 2.658 | 10 |
| Holdout final | 2011-09-01 | 2.768 | 13 |

Comparar dos modelos fijos contra ventas históricas90. Modelo admisible si mejora agregado y pierde en como máximo dos de cuatro períodos. Preferir simple salvo mejora del complejo en todos los períodos frente al simple. Holdout una vez: empate/pérdida conserva baseline sin elegir otro modelo usando ese resultado.

## Condiciones y límites

Disponibilidad inmediata es supuesto, no hecho: +7 días de latencia hipotética hace inviable el primer fit. Datos históricos públicos y encargo/capacidad simulados; no valida una campaña real ni uplift/ROI. Cohortes usan primera compra observada, no adquisición. Diciembre2011 es incompleto. Los outcomes del holdout no se inspeccionaron; distribución descriptiva de la fuente completa sí.

## Revisión solicitada

Aprobar Diagnosis y data-quality, calendario y aceptación en validation/evaluation_contract.yaml antes de crear dataset temporal, features o labels. Gate NEEDS_REVIEW, no PASS automático. Gasto API US$0.

Evidencia: reports/diagnosis/diagnostic-summary.json; monthly-summary.csv; observed-cohorts.csv; cutoff-proposal.json; reports/framing/coverage-preview.json.
