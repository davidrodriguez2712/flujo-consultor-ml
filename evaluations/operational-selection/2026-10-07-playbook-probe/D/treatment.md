```json
{
  "selected_ids": ["A", "B"],
  "effective_k": 2,
  "metrics": {
    "precision": 0.5,
    "recall": 0.5,
    "lift": 0.75
  },
  "decision": "ranking_only",
  "rationale": [
    "Población: 3 filas (A, B, C). El contexto indica K=2 clientes elegibles; no se declaran restricciones de cooldown/contactabilidad ni exclusiones, así que se usan las 3 filas como población evaluada. Supuesto a confirmar (ver open_questions).",
    "K efectivo = min(capacidad=2, elegibles=3) = 2, sin rellenar con excluidos.",
    "Ranking de riesgo: score descendente, id ascendente para empates (no hay empates): A (0.9), B (0.8), C (0.2). Top-2 = [A, B].",
    "Positivos seleccionados: A=1, B=0, por lo tanto 1 de 2 seleccionados.",
    "Precision@2 = 1/2 = 0.5 (denominador: 2 seleccionados).",
    "Positivos elegibles observados: A=1, C=1, es decir 2 (labels completas según el contexto). Recall@2 = 1/2 = 0.5.",
    "Prevalencia de la población elegible = 2/3 ≈ 0.6667. Lift@2 = 0.5 / 0.6667 = 0.75 (por debajo de 1: en esta muestra de 3 filas, el top-2 no supera al azar).",
    "Las métricas son descriptivas sobre 3 filas con labels completas; con n tan pequeño no hay incertidumbre estimable de forma útil y no deben generalizarse.",
    "El score es probabilidad de churn bajo política actual, no uplift. No hay tratamiento/control, costes, margen ni efecto incremental. Por eso no se puede afirmar que este ranking maximice clientes salvados ni ROI de contactos; la decisión causal no es identificable y no se demuestra una campaña óptima.",
    "Unidades: la tabla no distingue cliente-mes de clientes únicos; se asume una fila por cliente único, sin verificar.",
    "No se aprueba ningún gate; gate_decision queda en NEEDS_REVIEW."
  ],
  "open_questions": [
    "¿Se confirma que A, B y C son los 3 clientes elegibles y que no hay reglas de cooldown/contactabilidad que excluyan a alguno?",
    "¿Cada fila es un cliente único o un cliente-mes?",
    "¿Cuál es la definición, ventana y horizonte del label de churn y el momento de predicción del score?",
    "¿Existe o puede diseñarse un experimento (tratamiento/control) para medir el efecto incremental del contacto?",
    "¿Cuáles son los costes de contacto, margen por cliente retenido y el owner que define la métrica de negocio (clientes salvados vs ROI)?",
    "¿Hay una muestra mayor y representativa para evaluar el ranking con incertidumbre?"
  ],
  "gate_decision": "NEEDS_REVIEW"
}
```
