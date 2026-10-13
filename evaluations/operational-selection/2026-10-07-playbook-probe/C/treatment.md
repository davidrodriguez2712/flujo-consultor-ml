```json
{
  "selected_ids": ["H1", "U1"],
  "effective_k": 2,
  "metrics": {
    "precision": null,
    "recall": null,
    "lift": null
  },
  "decision": "ranking_only",
  "rationale": [
    "Población elegible: 4 casos (U1, H1, U2, H2). K efectivo = min(2, 4) = 2, sin relleno con excluidos.",
    "Orden por score descendente: U1 (0.99), H1 (0.80), U2 (0.70), H2 (0.10). No hay empates, así que la regla de id ascendente no se activa. Top-2 = {U1, H1}; se listan en orden alfabético por id: [H1, U1].",
    "Cobertura de labels: 2 de 4 casos elegibles (50%) tienen target observado (H1=1, H2=0). U1 y U2 tienen target null, que significa no observado y no negativo. No se imputa 0.",
    "Cobertura en la selección: 1 de 2 seleccionados tiene label (H1=1). U1 no tiene label, por lo que los positivos de la selección no se pueden contar.",
    "Precision@2 = positivos en la selección / 2. Es no identificable (null): el numerador está entre 1 y 2 según el label desconocido de U1. Solo se puede decir que lo observado es 1 positivo confirmado entre 2 seleccionados.",
    "Recall@2 = positivos en la selección / positivos elegibles. Es no identificable (null): faltan los labels de U1 y U2, y el denominador de positivos poblacionales está entre 1 y 3.",
    "Lift@2 = Precision@2 / prevalencia de la población elegible. Es null porque no son identificables ni el numerador ni la prevalencia. La prevalencia observada entre inspeccionados (1/2) no se extrapola a la población: los inspeccionados no son una muestra representativa y no hay diseño de muestreo ni propensiones para corregir el sesgo.",
    "Sesgo de selección: los targets existen solo en casos inspeccionados históricamente. El mecanismo de inspección es desconocido y probablemente depende del riesgo.",
    "Límite causal: la selección es una propuesta nueva y no hay inspecciones ejecutadas. El score es un ranking de riesgo, no uplift. No se estima efecto, incrementalidad ni ROI de inspeccionar. Por eso la decisión es ranking_only y no causal_not_identifiable.",
    "No se inventaron costes, labels, restricciones de cooldown ni autoridad. No se aprueba ningún gate."
  ],
  "open_questions": [
    "¿Cómo se eligieron históricamente los casos inspeccionados (H1, H2)? Se necesitan el mecanismo, el diseño de muestreo o las propensiones de inspección.",
    "¿Existen labels, o una regla de label con ventana y delay, para U1 y U2? ¿O se pueden obtener mediante una muestra de inspección aleatoria?",
    "¿Cuál es la capacidad operativa real y quién es el owner? K=2 viene del input, pero su origen no está confirmado.",
    "¿Hay restricciones de elegibilidad (cooldown, contactabilidad) no declaradas?",
    "¿Qué decisión o acción cambiaría el score y qué evidencia causal se requiere? Si se quiere medir incrementalidad, hace falta un diseño experimental con estimand definido.",
    "¿Cuál es la métrica de negocio aceptada (por ejemplo recuperación esperada) y quién revisa el resultado?"
  ],
  "gate_decision": "NEEDS_REVIEW"
}
```
