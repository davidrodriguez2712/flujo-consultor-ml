```json
{
  "selected_ids": ["A", "B"],
  "effective_k": 2,
  "metrics": {
    "precision": 0.5,
    "recall": 0.5,
    "lift": 0.75
  },
  "decision": "causal_not_identifiable",
  "rationale": [
    "Ranking de riesgo: score descendente, id ascendente como desempate. Orden: A (0.9), B (0.8), C (0.2). No hay empates, así que el desempate no interviene.",
    "K=2 y hay 3 clientes elegibles, por lo que effective_k = min(K, 3) = 2. Seleccionados: A y B.",
    "Precision@2 = clientes con churn=1 en el top-2 / 2 = 1/2 = 0.5 (A=1, B=0).",
    "Recall@2 = churners en el top-2 / churners totales = 1/2 = 0.5 (churners totales: A y C).",
    "Lift@2 = Precision@2 / tasa base = 0.5 / (2/3) = 0.75. La tasa base de churn es 2/3 ≈ 0.667 sobre los 3 clientes elegibles. Lift < 1: en esta muestra el top-2 no supera al azar.",
    "Las métricas son descriptivas sobre 3 filas (n muy pequeño, sin intervalos de confianza fiables). Los labels de churn están completos, por eso se pueden calcular, pero describen asociación del score con el churn observado bajo la política actual.",
    "El score es de probabilidad de churn, no de uplift. Un score de churn alto no implica que contactar a ese cliente cause retención (el playbook distingue propensión de efecto causal).",
    "No hay grupo tratamiento/control, ni asignación, ni costes, ni margen, ni efecto incremental. Por tanto no se puede identificar cuántos clientes se 'salvan' ni el ROI de contactos. Las métricas causales (clientes salvados, ROI) son null/no estimadas, y no se afirma que este ranking maximice ninguna de ellas.",
    "Este resultado no demuestra una campaña óptima: solo es un ranking de riesgo para la capacidad K=2. Tampoco hay baseline comparable ni validación temporal/holdout."
  ],
  "open_questions": [
    "¿Qué acción concreta se aplicaría a los contactados y quién es el owner de la decisión?",
    "¿Existe o puede diseñarse un experimento aleatorizado (tratamiento/control) para medir el efecto incremental del contacto y estimar uplift?",
    "¿Cuáles son el coste por contacto, el margen/valor por cliente retenido y la definición de ROI a usar?",
    "¿Cuál es la definición del label de churn, la ventana de observación, el horizonte de predicción y el momento de scoring?",
    "¿K=2 es una capacidad operativa real o un parámetro ilustrativo?",
    "¿Se dispone de más clientes y de un baseline (regla actual) para comparar con un tamaño de muestra suficiente?"
  ],
  "gate_decision": "NEEDS_REVIEW"
}
```
