```json
{
  "selected_ids": ["A", "B"],
  "effective_k": 2,
  "metrics": {
    "precision": 0.5,
    "recall": 0.5,
    "lift": 1.0
  },
  "decision": "ranking_only",
  "rationale": [
    "Población: 4 casos activos y elegibles (A, B, C, D), con labels binarias completas. Capacidad K=2, por lo que effective_k=2 (K ≤ N, sin recorte).",
    "Orden: score descendente y empate por id ascendente, regla fijada antes de las labels. A, B y C empatan en 0.9 y D tiene 0.1. Orden resultante: A, B, C, D. Top-2 = {A, B}.",
    "Precision@2 = TP/K = 1/2 = 0.5 (A=1 es positivo y B=0 es negativo).",
    "Recall@2 = TP/positivos totales = 1/2 = 0.5 (positivos en la población: A y C, es decir 2 de 4).",
    "Tasa base = 2/4 = 0.5. Lift@2 = 0.5 / 0.5 = 1.0.",
    "Comparador aleatorio con la misma capacidad y población: precisión esperada = 0.5 y recall esperado = K/N = 0.5. El ranking no supera al azar (lift 1.0).",
    "La selección depende por completo del desempate por id. C tiene el mismo score y target=1, y con otro desempate el resultado sería distinto (por ejemplo {A, C} daría precision 1.0). El score no discrimina entre A, B y C.",
    "Las métricas son descriptivas sobre los 4 casos con labels observadas. No hay intervención ejecutada ni grupo de comparación asignado, así que no se identifica ningún efecto causal de inspeccionar. La propensión o el score alto no implican que la acción cause mejora.",
    "Con N=4 y 2 positivos no es razonable reportar intervalos ni generalizar. Cualquier cambio de un solo caso mueve las métricas de forma material.",
    "No se entrenó, no se actuó externamente, no se escribieron archivos y no se aprobó ningún gate."
  ],
  "open_questions": [
    "¿Qué decisión y qué acción operativa usará el score (inspección u otra) y quién es el owner?",
    "¿Qué representa el score y por qué hay tres casos empatados en 0.9? ¿Existe un criterio de desempate con sentido operativo distinto al id?",
    "¿Cómo se define el target (regla de label), con qué prediction timestamp, ventana de observación y horizonte?",
    "¿Las labels estaban disponibles en el momento de decisión? Si se usaron para evaluar, ¿hay label delay?",
    "¿Se necesita medir incrementalidad? De ser así, hace falta un diseño experimental o causal con estimand, asignación y comparador definidos.",
    "¿Se dispone de una población mayor para evaluar con incertidumbre, baseline y desempeño por período o segmento?"
  ],
  "gate_decision": "NEEDS_REVIEW"
}
```
