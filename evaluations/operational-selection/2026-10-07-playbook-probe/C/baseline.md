```json
{
  "selected_ids": ["U1", "H1"],
  "effective_k": 2,
  "metrics": {
    "precision": null,
    "recall": null,
    "lift": null
  },
  "decision": "ranking_only",
  "rationale": [
    "Selección: orden por score descendente (empate por id ascendente, sin empates aquí): U1=0.99, H1=0.80, U2=0.70, H2=0.10. Con K=2 y 4 casos elegibles, effective_k=2 (K ≤ N, no hay recorte).",
    "Denominadores: población elegible N=4; selección completa n=2 (U1, H1); casos con label observado = 2 (H1=1, H2=0); casos sin label = 2 (U1, U2). Solo H1 está en la selección con label; U1 no tiene label.",
    "Precision@2 en la selección completa = (positivos en {U1,H1}) / 2. H1 aporta 1 positivo, pero el label de U1 es null (no inspeccionado, no es negativo). El numerador es indeterminado, así que precision=null.",
    "Recall@2 en toda la población = positivos en la selección / positivos totales. Ni el numerador ni el denominador son identificables porque U1 y U2 no tienen label. Los únicos positivos conocidos son H1 (1) y el único negativo conocido es H2. recall=null.",
    "Lift@2 = Precision@2 / tasa base poblacional. Ambos términos dependen de labels ausentes (U1, U2), y no hay diseño de muestreo ni propensiones para reponderar. lift=null.",
    "Sesgo/cobertura: los labels existen solo para casos inspeccionados históricamente (H1, H2), con cobertura 2/4 = 50% de la población y 1/2 = 50% de la selección. El mecanismo de inspección es desconocido y probablemente depende del score o de otros factores, por lo que no se puede asumir que los labelados representen a los no labelados (sesgo de selección, MNAR potencial). Imputar null como 0 sesgaría las métricas.",
    "Solo como cotas lógicas (no estimaciones; dependen de los labels desconocidos de U1 y U2 y de que esos labels estén definidos): precision@2 ∈ [0.5, 1.0]; recall@2 ∈ [0.5, 1.0]; tasa base ∈ [0.25, 0.75]; lift ∈ [1.0, 2.0]. Combinaciones (U1,U2): (0,0) → P=0.5, base=0.25, lift=2; (0,1) → P=0.5, base=0.5, lift=1; (1,0) → P=1, base=0.5, lift=2; (1,1) → P=1, base=0.75, lift=1.33.",
    "Descriptivo sobre el subconjunto labelado de la selección (H1: 1/1) no equivale a Precision@2 de la selección completa y no se reporta como tal.",
    "Decisión ranking_only: la salida es una priorización de 2 casos para una acción existente. La selección es una propuesta nueva, no hay inspecciones ejecutadas, ni grupo de comparación, asignación aleatoria o contrafactual. No se identifica ni se estima ningún efecto causal de inspeccionar, y un score alto no implica que la acción cause mejora.",
    "No se entrenó ningún modelo, no se ejecutó ninguna acción, no se escribieron archivos y no se inventaron labels, costes ni autoridad. Esta salida no aprueba ningún gate."
  ],
  "open_questions": [
    "¿Cómo se decidió históricamente qué casos se inspeccionaron (H1, H2)? ¿Dependió del score u otras variables? Sin esto no se puede corregir el sesgo de selección.",
    "¿Existe, o puede obtenerse, el label verdadero de U1 y U2 (por ejemplo, mediante inspección posterior o una muestra aleatoria de verificación)?",
    "¿Cuál es la definición formal del target (regla de label, ventana de observación, horizonte, label delay) y cuál era el timestamp de predicción del score?",
    "¿Quién es el owner de la decisión y cuál es la capacidad operativa real? ¿Es K=2 una restricción real o un parámetro de ejemplo?",
    "¿Se desea medir incrementalidad de la inspección? En ese caso haría falta definir estimand, comparador y asignación (idealmente aleatoria) antes de ejecutar.",
    "¿Qué baseline (regla actual o aleatorio) y qué estrategia de validación se usarían para comparar la selección? Con N=4 no hay base para incertidumbre estadística."
  ],
  "gate_decision": "NEEDS_REVIEW"
}
```
