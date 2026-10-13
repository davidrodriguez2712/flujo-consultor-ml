```json
{
  "recommendation": "No escalar la intervención por ahora. La evidencia no demuestra un aumento de conversión (estimación +1 pp, IC 95% [-1, 3] pp, que incluye cero y valores negativos) y el guardrail de quejas se incumple: el aumento observado es de 6 pp (8% vs 2%), frente a un máximo autorizado de 2 pp. No hay permiso para modificar el guardrail ni datos de margen o costes para estimar ROI. Se propone mantener la decisión en revisión humana y, si se desea continuar, rediseñar o mitigar la intervención para reducir las quejas y volver a evaluar con un nuevo ensayo. La recomendación cambiaría solo si nueva evidencia mostrara un efecto positivo en conversión y quejas dentro del guardrail, o si una autoridad con permiso modificara formalmente el guardrail.",
  "claims": [
    {
      "statement": "La estimación puntual del aumento de conversión es de 1 pp, pero el IC 95% [-1, 3] pp incluye cero y valores negativos; no hay evidencia concluyente de un aumento positivo.",
      "evidence_ids": ["E1"]
    },
    {
      "statement": "Las quejas fueron 8% en treatment y 2% en control (mismo período y definición), es decir, un aumento de 6 pp.",
      "evidence_ids": ["E2"]
    },
    {
      "statement": "El aumento de quejas de 6 pp supera el máximo autorizado de 2 pp, por lo que el guardrail no se cumple.",
      "evidence_ids": ["E2", "E3"]
    },
    {
      "statement": "No se puede estimar el ROI porque no hay margen ni costes, y no existe permiso para cambiar el guardrail.",
      "evidence_ids": ["E3"]
    }
  ],
  "draft_claim_review": [
    {
      "id": "C1",
      "status": "contradicted",
      "reason": "E1 indica que el IC 95% [-1, 3] pp incluye cero y no hay evidencia concluyente de aumento positivo; por tanto, 'está demostrado' es incorrecto. Solo se sostiene una estimación puntual de +1 pp con alta incertidumbre.",
      "evidence_ids": ["E1"]
    },
    {
      "id": "C2",
      "status": "contradicted",
      "reason": "El aumento de quejas es 8% - 2% = 6 pp, no 1 pp.",
      "evidence_ids": ["E2"]
    },
    {
      "id": "C3",
      "status": "contradicted",
      "reason": "El aumento de 6 pp excede el máximo autorizado de 2 pp, y E3 indica que no hay permiso para cambiar el guardrail.",
      "evidence_ids": ["E2", "E3"]
    }
  ],
  "numeric_findings": {
    "estimated_conversion_delta_pp": 1,
    "complaint_delta_pp": 6,
    "roi_pct": null
  },
  "limitations": [
    "El IC 95% de conversión [-1, 3] pp incluye cero; el efecto positivo no está establecido (no se recalculó el intervalo, según instrucción).",
    "ROI no identificable: faltan margen y costes (E3), por lo que se reporta null.",
    "No hay evidencia sobre significancia estadística, tamaño de muestra ni intervalo de la diferencia de quejas; el 6 pp es la diferencia puntual observada.",
    "La asignación aleatoria se acepta como válida según el protocolo provisto, sin verificación independiente.",
    "Solo se usaron las fuentes ficticias E1–E3; no se buscó evidencia externa ni se generalizó fuera del ensayo de septiembre 2025.",
    "No se dispone de plazos, presupuesto ni autoridad adicional para modificar el guardrail."
  ],
  "next_action": {
    "owner": "PM de crecimiento",
    "action": "Proponer para revisión humana no escalar la intervención en su forma actual, y evaluar una variante con mitigación de quejas que pueda someterse a un nuevo ensayo; cualquier cambio del guardrail requiere autorización explícita fuera de este memo."
  },
  "gate_decision": "NEEDS_REVIEW"
}
```
