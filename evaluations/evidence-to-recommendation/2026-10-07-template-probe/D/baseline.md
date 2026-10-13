```json
{
  "recommendation": "No afirmar a nivel organizacional ni la tasa de error ni los ahorros. Solo se puede reportar que 35 de 100 expedientes auditados (seleccionados deliberadamente por mayor riesgo) tienen error confirmado, es decir 35% en esa muestra no probabilística. Esa cifra no se puede extrapolar a los 10000 expedientes, ni sirve para estimar ahorros, porque no hay probabilidad de inclusión, datos representativos del resto ni costes o efecto de corrección. Se propone, para review, que el responsable de operaciones decida si conviene una auditoría con muestra probabilística y que se recopilen datos de costes y efecto de corrección antes de cualquier afirmación de ahorro. Ninguna cifra de ahorro ni de error poblacional debe comunicarse hasta entonces.",
  "claims": [
    {
      "statement": "En los 100 expedientes auditados, 35 tienen error confirmado, lo que equivale a una tasa de 0.35 (35%) dentro de esa muestra.",
      "evidence_ids": ["E1"]
    },
    {
      "statement": "Los 100 expedientes fueron seleccionados deliberadamente por mayor riesgo y no constituyen una muestra probabilística, por lo que la tasa observada no es representativa de la población.",
      "evidence_ids": ["E1", "E2"]
    },
    {
      "statement": "La población total es de 10000 expedientes, pero no hay probabilidad de inclusión ni datos representativos para los 9900 restantes, así que la tasa de error poblacional no es identificable con la evidencia disponible.",
      "evidence_ids": ["E1", "E2"]
    },
    {
      "statement": "No hay costes, horas monetizadas ni efecto de corrección, por lo que no se puede estimar ahorro anual.",
      "evidence_ids": ["E3"]
    }
  ],
  "draft_claim_review": [
    {
      "id": "D1",
      "status": "unsupported",
      "reason": "El 3500 resulta de aplicar 35% a 10000, lo que presupone que la muestra de alto riesgo es representativa. E1 indica selección deliberada por riesgo y E2 que no hay probabilidad de inclusión ni datos representativos. Por tanto la cifra no está respaldada. Tampoco se prueba falsa: solo se sabe que 35 errores están confirmados en la muestra, y el total poblacional es no identificable (probablemente sesgado al alza, pero sin datos para cuantificarlo).",
      "evidence_ids": ["E1", "E2"]
    },
    {
      "status": "supported",
      "id": "D2",
      "reason": "35 errores confirmados sobre 100 expedientes auditados dan 0.35, es decir 35%. Aplica solo a la muestra auditada, no a la población.",
      "evidence_ids": ["E1"]
    },
    {
      "id": "D3",
      "status": "unsupported",
      "reason": "E3 indica que no hay costes, horas monetizadas ni efecto de corrección. La cifra de USD 50000 no tiene base en la evidencia provista. No se puede probar falsa, solo carece de sustento.",
      "evidence_ids": ["E3"]
    }
  ],
  "numeric_findings": {
    "audited_error_rate": 0.35,
    "population_error_rate": null,
    "annual_savings_usd": null
  },
  "limitations": [
    "La muestra de 100 expedientes (1% de 10000) fue elegida por mayor riesgo, no al azar; la tasa de 0.35 describe solo esos expedientes.",
    "Sin probabilidades de inclusión ni datos representativos del resto, no se puede ponderar ni extrapolar a la población; por eso population_error_rate es null.",
    "No hay costes, horas monetizadas ni efecto de corrección; por eso annual_savings_usd es null y no se construyen escenarios base/alto/bajo.",
    "El período es septiembre 2025 según el contexto; no hay evidencia sobre otros períodos ni sobre la anualización.",
    "Este memo no incluye intervalos de confianza porque no hay diseño muestral que los justifique.",
    "La revisión humana y la aprobación del gate están pendientes; este documento es solo una propuesta."
  ],
  "next_action": {
    "owner": "Responsable de operaciones",
    "action": "Proponer para review: (1) comunicar solo la tasa de 35% como resultado de la muestra de alto riesgo, sin extrapolar; (2) evaluar una auditoría con muestra probabilística de la población de 10000 expedientes para estimar la tasa poblacional con incertidumbre; (3) reunir datos de costes, horas monetizadas y efecto esperado de corrección antes de evaluar cualquier ahorro. Plazos, presupuesto y tamaño de muestra quedan por definir por quien corresponda."
  },
  "gate_decision": "NEEDS_REVIEW"
}
```
