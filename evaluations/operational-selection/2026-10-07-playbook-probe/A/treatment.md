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
    "Población: 4 casos activos y elegibles (A, B, C, D). No se declaran exclusiones, cooldown ni restricciones de contactabilidad, así que no se inventó ninguna.",
    "K efectivo = min(capacidad 2, elegibles 4) = 2. No hubo exclusiones que rellenar.",
    "Orden: score descendente, con empate por id ascendente fijado antes de ver labels. A, B y C empatan en 0.9 y D tiene 0.1. El orden resultante es A, B, C, D, y el top-2 es A, B.",
    "Labels completas y binarias en los 4 casos: A=1, B=0, C=1, D=0. Positivos elegibles observados = 2, prevalencia = 2/4 = 0.5.",
    "Precision@2 = positivos seleccionados / seleccionados = 1/2 = 0.5 (A=1, B=0).",
    "Recall@2 = positivos seleccionados / positivos elegibles = 1/2 = 0.5.",
    "Lift@2 = Precision@2 / prevalencia de la misma población elegible = 0.5/0.5 = 1.0. Coincide con el comparador aleatorio bajo la misma capacidad y población, cuya precisión esperada es 0.5, así que el top-2 no supera al azar.",
    "Las métricas son identificables porque las labels están completas en toda la población elegible. No se extrapola a otras poblaciones.",
    "Fragilidad: el score no discrimina entre A, B y C (los tres tienen 0.9). La selección depende solo de la regla de desempate por id, no del score. Con otro desempate, Precision@2 sería 1.0 (A, C) o 0.5 (B, C). Con n=4 y 2 positivos no hay incertidumbre estimable de forma útil.",
    "Límite de inferencia: son métricas descriptivas de ranking. Un score o propensión no es uplift, y no se estima efecto incremental, ROI ni impacto de acciones no ejecutadas. Para eso haría falta un diseño experimental o causal con estimand, asignación y comparador definidos.",
    "No se entrenó ningún modelo, no se ejecutaron acciones ni se escribieron archivos. No tengo autoridad para aprobar gates, por lo que gate_decision queda en NEEDS_REVIEW."
  ],
  "open_questions": [
    "¿Cuál es la acción operativa que consumirá la selección y cuál es el outcome (target) que mide la label? El input no lo define.",
    "¿El score tiene un empate triple en 0.9 por diseño o por baja resolución? Si es por resolución, ¿hay un criterio secundario de priorización aprobado por el owner?",
    "¿Existen restricciones de elegibilidad, cooldown o contactabilidad no declaradas que cambiarían la población o el K efectivo?",
    "¿Quién es el owner y quién aprueba el gate?",
    "¿Se necesita medir incrementalidad? De ser así, habría que definir un diseño experimental o causal, con tamaño de muestra suficiente."
  ],
  "gate_decision": "NEEDS_REVIEW"
}
```
