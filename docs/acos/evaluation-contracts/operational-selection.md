# Contrato de selección operacional

Versión documental: `0.1.0`. Estado: propuesto, local, no ejecutado. [Alcance compartido](README.md).

## Propósito

Separar población, capacidad, ranking y causalidad. Un ranking de riesgo puede ser válido aunque no identifique el efecto de contactar a sus miembros.

## Inputs mínimos

- `business_decision`: decisión de negocio y si requiere efecto incremental.
- `population_id`, período y unidad: definir clientes, cliente-mes u otra entidad.
- `capacity_k`: máximo de unidades seleccionadas, separado del número de elegibles.
- Restricciones de elegibilidad con su fuente; ID único por unidad.
- Significado y disponibilidad del score; `sort_direction` y `tie_break_rule` fijados antes de outcomes.
- Definición de target, cobertura de labels y población sobre la que se piden métricas.
- Para una decisión causal: intervención, comparador, estimand y evidencia de identificación, o su ausencia explícita.

Este contrato describe top-K con capacidad por conteo y coste unitario homogéneo. Para presupuesto, costes variables, routing o combinaciones de restricciones, se necesita un problema de optimization específico; `min(K, elegibles)` no resuelve esos casos.

## Output propuesto

```yaml
output_type: risk_ranking
eligible_count: 3
capacity_k: 2
effective_k: 2
selected_ids: [A, B]
ordering:
  criterion: score_descending
  tie_break_rule: id_ascending
causal_identification:
  status: not_identifiable
  reason: Solo hay riesgo bajo la política actual; no hay evidencia de efecto incremental.
metrics:
  population_id: eligible-customer-months
  precision: 0.5
  recall: 0.5
  lift: 0.75
gate_decision: NEEDS_REVIEW
```

Ejemplo: tres elegibles A/B/C con scores 0,9/0,8/0,2 y targets 1/0/1. Negocio pregunta si contactar maximiza clientes salvados; no hay datos del efecto de contacto. La selección descriptiva y su falta de identificación causal se reportan separadamente.

`output_type` describe lo producido, por ejemplo `risk_ranking`; no decide si la pregunta de negocio está resuelta. `causal_identification.status`: `not_requested` si la tarea no pide causalidad; `identifiable` con diseño y supuestos sustentados; `not_identifiable` cuando los inputs no permiten identificar el efecto solicitado; `indeterminate` si no hay información para evaluar el diseño. No usar un campo que obligue a elegir entre ranking y falta de identificación causal.

## Reglas verificables

1. Aplicar elegibilidad antes de ordenar. No inventar cooldown ni rellenar capacidad con excluidos.
2. En este top-K simple, `effective_k=min(capacity_k, eligible_count)`; capacidad y conteo son enteros no negativos.
3. Ordenar seleccionados por el criterio completo. ID ascendente solo desempata; no reordenar alfabéticamente después de seleccionar.
4. Precision divide positivos seleccionados por seleccionados; recall, por positivos de la población requerida; lift, precision por prevalencia de esa misma población. Declarar conteos, población y período.
5. Evaluar identificación por métrica. Labels ausentes de no seleccionados pueden impedir recall/lift, aunque precision sea calculable si todos los seleccionados tienen label. No poner automáticamente null a todas ni completar ausentes con cero.
6. Un denominador cero produce `null` y motivo. Con selección vacía y positivos poblacionales conocidos, recall puede ser cero; precision sigue indefinida.
7. Separar cobertura observada y cotas lógicas de estimaciones identificadas. Muestreo de inspeccionados con mecanismo desconocido no prueba representatividad ni demuestra dirección del sesgo.
8. Riesgo y métricas descriptivas no identifican uplift, clientes salvados, ROI ni política óptima. La comparación causal requiere su propio diseño; una medición previa aislada no basta.

## Criterios de aceptación para otra ronda

- Verificar miembros y orden por separado, con empates y sin empates.
- Cubrir capacidad cero, menos elegibles que capacidad y etiquetas parcialmente observadas.
- Comprobar denominadores con conteos independientes y unidades consistentes.
- Incluir un ranking descriptivo suficiente para su tarea y una pregunta causal con evidencia válida, además de casos no identificables.
- Señalar población desconocida o inputs inconsistentes antes de afirmar una política ejecutable.
- Mantener la aprobación humana separada de producir un ranking.

Los ejemplos no autorizan contactar clientes ni constituyen un gate ejecutable. [Contrato de ejecución](execution-provenance.md).
