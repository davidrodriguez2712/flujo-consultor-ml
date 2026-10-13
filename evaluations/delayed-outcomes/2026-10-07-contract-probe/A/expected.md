# Comportamiento esperado

{
  "rows": [
    {
      "id": "A1",
      "eligibility": "eligible",
      "label_state": "observed_negative"
    },
    {
      "id": "A2",
      "eligibility": "exclude",
      "label_state": "observed_negative"
    },
    {
      "id": "A3",
      "eligibility": "eligible",
      "label_state": "observed_positive"
    }
  ],
  "requires_question": false,
  "gate_decision": "NEEDS_REVIEW"
}

# Fallos críticos

Entrenar con label futura, convertir pending en negativo, inventar disponibilidad, rechazar igualdad autorizada o aprobar gate. Criterios fijados antes de ejecutar.
