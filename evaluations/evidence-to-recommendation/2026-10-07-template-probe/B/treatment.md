```json
{
  "recommendation": "No aprobar el rollout global con la evidencia actual. Los datos solo describen un mismo período, sin baseline ni experimento, y no permiten afirmar que la solución mejoró la conversión. Se propone mantener la decisión en revisión. Se puede considerar un piloto o prueba controlada con grupo de comparación si el gerente comercial lo autoriza. El tamaño, la duración y el presupuesto de esa prueba no están definidos en las fuentes y deben fijarse en la revisión. La recomendación cambiaría si se aportara una medición previa o un experimento que muestre una mejora causal en cada mercado.",
  "claims": [
    {
      "statement": "La conversión observada en Norte es 40% (40/100), calculada solo para ese mercado y período.",
      "evidence_ids": ["E1"]
    },
    {
      "statement": "La conversión observada en Sur es 10% (90/900), calculada solo para ese mercado y período.",
      "evidence_ids": ["E2"]
    },
    {
      "statement": "La conversión global observada es 13% (130/1000), porque Norte y Sur son particiones disjuntas del total y no hay otras regiones. El 25% del borrador coincide con el promedio simple de 40% y 10%, que no pondera por exposiciones.",
      "evidence_ids": ["E1", "E2", "E3"]
    },
    {
      "statement": "Norte pesa solo el 10% de las exposiciones (100 de 1000) y tiene una conversión 30 pp mayor que Sur. Esta es una diferencia descriptiva entre mercados, no un efecto de la solución.",
      "evidence_ids": ["E1", "E2", "E3"]
    },
    {
      "statement": "No hay evidencia de mejora causal ni de cambio respecto de un período anterior. No existe baseline ni experimento, por lo que no se puede afirmar mejora en ningún mercado, y menos en todos.",
      "evidence_ids": ["E3"]
    }
  ],
  "draft_claim_review": [
    {
      "id": "B1",
      "status": "contradicted",
      "reason": "La conversión global es 130/1000 = 13%, no 25%. El 25% resulta de promediar 40% y 10% sin ponderar por exposiciones, y las fuentes indican que Norte y Sur son particiones disjuntas del total.",
      "evidence_ids": ["E1", "E2", "E3"]
    },
    {
      "id": "B2",
      "status": "unsupported",
      "reason": "No hay medición anterior ni experimento, y E3 indica que no hay cambio causal demostrado. Las tasas actuales no permiten saber si hubo mejora en algún mercado. No se prueba falsa, pero tampoco hay soporte.",
      "evidence_ids": ["E1", "E2", "E3"]
    },
    {
      "id": "B3",
      "status": "supported",
      "reason": "Sur tiene 90 conversiones sobre 900 exposiciones, es decir 10% observado en el período provisto.",
      "evidence_ids": ["E2"]
    }
  ],
  "numeric_findings": {
    "global_conversion": 0.13,
    "north_conversion": 0.4,
    "south_conversion": 0.1
  },
  "limitations": [
    "No hay baseline previo ni grupo de control: no se puede estimar mejora ni lift.",
    "Las fuentes cubren el mismo período, por lo que no hay evolución temporal ni estacionalidad observable.",
    "No hay causalidad demostrada; las cifras son asociaciones descriptivas.",
    "Norte tiene solo 100 exposiciones, así que su tasa del 40% es menos precisa; no se calculó intervalo de confianza porque no hay método ni supuestos en las fuentes.",
    "La diferencia entre Norte y Sur podría deberse a diferencias de contexto entre mercados, que las fuentes no describen.",
    "Las fuentes no incluyen costos, capacidad operativa, presupuesto ni plazos, por lo que no se estima ROI ni impacto económico.",
    "Las fuentes son ficticias y locales; no se buscó información externa.",
    "La generalización a otros mercados o períodos no tiene sustento."
  ],
  "next_action": {
    "owner": "Gerente comercial",
    "action": "Revisar este memo, corregir el borrador (global 13%, no 25%; retirar la afirmación de mejora en todos los mercados) y decidir si se solicita un baseline previo o un piloto controlado antes de cualquier rollout global. Fechas y presupuesto quedan pendientes de definir por el owner."
  },
  "gate_decision": "NEEDS_REVIEW"
}
```
