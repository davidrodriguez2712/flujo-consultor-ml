```json
{
  "recommendation": "No aprobar el rollout global con la evidencia actual. La conversión observada es 13% global (130/1000), 40% en Norte y 10% en Sur. Estas cifras describen un solo período, sin baseline previo ni experimento, y no demuestran que la solución mejore la conversión en ningún mercado. Se propone una decisión condicionada: mantener el rollout en pausa y pedir al gerente comercial que decida si se obtiene un baseline previo o se diseña una prueba controlada por mercado antes de reconsiderar. El gate queda en NEEDS_REVIEW.",
  "claims": [
    {
      "statement": "Norte registró 40 conversiones sobre 100 exposiciones, es decir 40% de conversión observada.",
      "evidence_ids": ["E1"]
    },
    {
      "statement": "Sur registró 90 conversiones sobre 900 exposiciones, es decir 10% de conversión observada.",
      "evidence_ids": ["E2"]
    },
    {
      "statement": "Norte y Sur son particiones disjuntas del total sin otras regiones, así que el total es 130 conversiones sobre 1000 exposiciones, o 13% de conversión global.",
      "evidence_ids": ["E1", "E2", "E3"]
    },
    {
      "statement": "La diferencia entre Norte y Sur es de 30 puntos porcentuales. Es una comparación descriptiva entre mercados y no un efecto de la solución.",
      "evidence_ids": ["E1", "E2", "E3"]
    },
    {
      "statement": "No hay baseline previo ni experimento ni cambio causal demostrado, por lo que la evidencia no permite afirmar que la solución mejoró la conversión en ningún mercado ni justificar un rollout global por mejora.",
      "evidence_ids": ["E3"]
    }
  ],
  "draft_claim_review": [
    {
      "id": "B1",
      "status": "contradicted",
      "reason": "La conversión global es (40+90)/(100+900) = 130/1000 = 13%, no 25%. El 25% no coincide con el total ponderado. El promedio simple de Norte y Sur sería 25%, pero ignora que los denominadores son muy distintos.",
      "evidence_ids": ["E1", "E2", "E3"]
    },
    {
      "id": "B2",
      "status": "unsupported",
      "reason": "Sin medición anterior ni experimento no se puede afirmar una mejora, y E3 indica que no hay cambio causal demostrado. Las tasas observadas (40% y 10%) son niveles de un solo período, no cambios. La afirmación tampoco se prueba falsa, simplemente no hay evidencia suficiente.",
      "evidence_ids": ["E1", "E2", "E3"]
    },
    {
      "id": "B3",
      "status": "supported",
      "reason": "90/900 = 0.10, es decir 10% de conversión observada en Sur. Es una tasa descriptiva del período y no implica causalidad.",
      "evidence_ids": ["E2"]
    }
  ],
  "numeric_findings": {
    "global_conversion": 0.13,
    "north_conversion": 0.4,
    "south_conversion": 0.1
  },
  "limitations": [
    "Las fuentes describen el mismo período y no hay baseline previo, por lo que no se puede medir ningún cambio ni mejora.",
    "No hay experimento ni grupo de control, y E3 indica que no hay cambio causal demostrado.",
    "Las diferencias entre Norte y Sur (40% vs 10%) pueden deberse a composición de audiencia, canal u otros factores no observados; no se dispone de datos para explicarlas.",
    "Norte tiene solo 100 exposiciones, así que su tasa es más incierta. No se proporcionan intervalos de confianza ni pruebas de significancia y no se calcularon.",
    "La conversión global de 13% está dominada por Sur (90% de las exposiciones) y no representa un mercado típico.",
    "No hay otras regiones en los datos, por lo que no se puede extrapolar a un rollout global.",
    "No se proporcionaron costos, capacidad operativa, plazos ni presupuesto, y no se asumió ninguno.",
    "No se buscó información externa; el análisis se limita a E1, E2 y E3, que son fuentes ficticias."
  ],
  "next_action": {
    "owner": "Gerente comercial",
    "action": "Revisar este memo y decidir si se mantiene en pausa el rollout global. Propuesta para su revisión: solicitar un baseline previo por mercado o definir una prueba controlada con comparación, y reconsiderar la decisión solo con esa evidencia. Esta es una propuesta sujeta a revisión humana; no se aprueba ni ejecuta ninguna acción."
  },
  "gate_decision": "NEEDS_REVIEW"
}
```
