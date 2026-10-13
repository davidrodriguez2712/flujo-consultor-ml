```json
{
  "selected_ids": ["B", "C"],
  "effective_k": 2,
  "metrics": {
    "precision": 0.5,
    "recall": 1.0,
    "lift": 1.0
  },
  "decision": "ranking_only",
  "rationale": [
    "Ventana de cooldown: [2025-01-02, 2025-02-01). A (último contacto 2025-01-20) y D (2025-01-31) caen dentro y quedan excluidos. B (2024-12-15) cae antes de la ventana y C (sin contacto previo) no tiene contacto, así que ambos son elegibles.",
    "Población elegible tras cooldown: {B, C}, n=2. Ordenados por score descendente e id ascendente: B (0.80), C (0.70).",
    "Capacidad K=3, pero solo hay 2 elegibles. Como no se permite rellenar con excluidos, effective_k = min(3, 2) = 2 y quedan 1 cupo sin usar.",
    "Denominadores explícitos: Precision@2 = positivos seleccionados / seleccionados = 1 (C) / 2 = 0.5. Recall = positivos seleccionados / positivos elegibles = 1 / 1 = 1.0. Tasa base elegible = 1/2 = 0.5. Lift = 0.5 / 0.5 = 1.0.",
    "Las métricas se calculan solo sobre la población elegible (B, C), no sobre los cuatro originales, según el contexto. Con n=2 la selección coincide con toda la población elegible, por lo que recall=1.0 y lift=1.0 son triviales y no informan sobre la calidad del ranking. Además, B (score más alto entre los elegibles) tiene target 0 y C tiene target 1, es decir, el ranking entre los elegibles está invertido respecto al target.",
    "Los targets son asociaciones descriptivas con labels completas. No identifican el efecto causal del contacto: no hay grupo de comparación, asignación aleatoria ni datos de tratamiento. Por eso la decisión es ranking_only y no se estiman efectos de acciones no ejecutadas.",
    "Con n=2 no se puede calcular una incertidumbre significativa (intervalos); cualquier lectura de desempeño es anecdótica."
  ],
  "open_questions": [
    "¿Se desea usar el cupo sobrante (1 de 3) de otra forma? El contexto prohíbe rellenar con excluidos, por lo que se deja sin usar salvo que el owner indique lo contrario.",
    "¿La ventana del cooldown es semiabierta como indica la notación [2025-01-02, 2025-02-01)? Se asumió así; un contacto el 2025-02-01 no afecta a ningún cliente en este conjunto.",
    "¿Cuál es la definición del target (outcome, ventana de observación, horizonte) y la fecha de predicción? No están en los inputs, por lo que el target se toma tal cual viene.",
    "¿Existe una validación con más datos (n mayor) y un baseline para evaluar el ranking? Con 2 elegibles no es posible.",
    "¿Quién es el owner/autoridad que revisa y aprueba el gate? No se asume autoridad."
  ],
  "gate_decision": "NEEDS_REVIEW"
}
```
