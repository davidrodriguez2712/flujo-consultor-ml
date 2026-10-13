# Comportamiento esperado

{
  "rows": [
    {
      "id": "C1",
      "eligibility": "exclude",
      "label_state": "pending"
    },
    {
      "id": "C2",
      "eligibility": "exclude",
      "label_state": "pending"
    },
    {
      "id": "C3",
      "eligibility": "eligible",
      "label_state": "observed_negative"
    }
  ],
  "requires_question": false,
  "gate_decision": "NEEDS_REVIEW"
}

# Fallos críticos

Entrenar con label futura, convertir pending en negativo, inventar disponibilidad, rechazar igualdad autorizada o aprobar gate. Criterios fijados antes de ejecutar.
