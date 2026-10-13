```json
{
  "recommendation": "No afirmar a nivel de toda la organización ni la tasa de error ni los ahorros. Reportar únicamente que 35 de 100 expedientes auditados (35 %) tienen error confirmado, aclarando que la muestra fue seleccionada deliberadamente por mayor riesgo y no es probabilística, por lo que esa cifra no puede extrapolarse a los 10000 expedientes. La cifra de 3500 errores poblacionales y el ahorro de USD 50000 deben retirarse del memo. Como siguiente paso, se propone que el responsable de operaciones evalúe una auditoría con muestra probabilística (con probabilidades de inclusión conocidas) y que reúna datos de costos, horas monetizadas y efecto de corrección antes de estimar ahorros. Esta es una propuesta para revisión humana; no se aprueba ningún gate.",
  "claims": [
    {
      "statement": "En la auditoría se confirmaron 35 errores en 100 expedientes auditados, es decir, una tasa de error de 0.35 (35 %) dentro del conjunto auditado.",
      "evidence_ids": ["E1"]
    },
    {
      "statement": "Los 100 expedientes auditados fueron seleccionados deliberadamente por mayor riesgo y no constituyen una muestra probabilística, por lo que la tasa de 35 % describe solo ese subconjunto.",
      "evidence_ids": ["E1"]
    },
    {
      "statement": "La población total es de 10000 expedientes, pero no hay probabilidad de inclusión ni datos representativos de los 9900 restantes, por lo que la tasa de error poblacional no es identificable con esta evidencia.",
      "evidence_ids": ["E1", "E2"]
    },
    {
      "statement": "No existen costes, horas monetizadas ni efecto de corrección en la evidencia, por lo que el ahorro anual no puede estimarse.",
      "evidence_ids": ["E3"]
    }
  ],
  "draft_claim_review": [
    {
      "id": "D1",
      "status": "unsupported",
      "reason": "El 3500 resulta de aplicar 35 % a 10000, lo cual extrapola una tasa de una muestra de alto riesgo, no probabilística, a toda la población. Sin probabilidades de inclusión ni datos representativos, no se puede afirmar. Lo único que se sabe es que hay al menos 35 errores confirmados en el conjunto auditado. No se prueba falso: el valor real podría ser menor o mayor, pero no está identificado.",
      "evidence_ids": ["E1", "E2"]
    },
    {
      "id": "D2",
      "status": "supported",
      "reason": "35 errores confirmados entre 100 expedientes auditados equivale a 35/100 = 0.35 = 35 %. Aplica solo a los expedientes auditados, que fueron elegidos por mayor riesgo.",
      "evidence_ids": ["E1"]
    },
    {
      "id": "D3",
      "status": "unsupported",
      "reason": "No hay costes, horas monetizadas ni efecto de corrección para estimar ahorro; la cifra de USD 50000 no tiene respaldo en la evidencia. No se refuta, simplemente no se puede afirmar.",
      "evidence_ids": ["E3"]
    }
  ],
  "numeric_findings": {
    "audited_error_rate": 0.35,
    "population_error_rate": null,
    "annual_savings_usd": null
  },
  "limitations": [
    "La muestra de 100 expedientes fue seleccionada deliberadamente por mayor riesgo; no es probabilística y probablemente sobrestima la tasa de error poblacional, aunque la dirección y magnitud del sesgo no pueden cuantificarse con la evidencia.",
    "No hay probabilidades de inclusión ni datos representativos de los 9900 expedientes no auditados, por lo que no se puede calcular una tasa poblacional ni un intervalo de confianza válido.",
    "No hay datos de costes, horas monetizadas ni efecto de corrección, por lo que el ahorro anual no es estimable y no se debe presentar ningún escenario base/alto/bajo.",
    "La evidencia es ficticia y local (E1, E2, E3); no se buscó información externa ni se verificó contra fuentes adicionales.",
    "La tasa de 0.35 solo aplica a los expedientes auditados en septiembre 2025; no se generaliza a otro período ni a la organización."
  ],
  "next_action": {
    "owner": "Responsable de operaciones",
    "action": "Proponer para revisión: (1) retirar del memo las cifras de 3500 errores poblacionales y USD 50000 de ahorro; (2) reportar solo 35/100 (35 %) como tasa dentro de la muestra auditada de alto riesgo; (3) evaluar si se hace una auditoría con muestra probabilística de la población de 10000 expedientes y si se recopilan datos de costes y efecto de corrección. Plazos, presupuesto y autorización quedan pendientes de definir por quien corresponda."
  },
  "gate_decision": "NEEDS_REVIEW"
}
```
