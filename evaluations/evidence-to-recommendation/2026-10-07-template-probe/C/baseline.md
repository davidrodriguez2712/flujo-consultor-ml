```json
{
  "recommendation": "No escalar la intervención por ahora. La evidencia no demuestra aumento de conversión (estimación +1 pp, IC95% [-1, 3] pp, que incluye el cero) y el aumento de quejas observado (+6 pp: 8% vs 2%) supera el guardrail autorizado de 2 pp. No hay permiso para cambiar el guardrail ni datos de margen/costes para estimar ROI. Se propone que el PM de crecimiento revise la evidencia y, si desea continuar, mantenga la intervención sin escalar hasta contar con una estimación de conversión concluyente y quejas dentro del guardrail, o hasta que el responsable con autoridad decida explícitamente sobre el guardrail. La decisión final y cualquier gate quedan para revisión humana.",
  "claims": [
    {
      "statement": "La estimación puntual de aumento de conversión es de 1 pp, pero el IC95% [-1, 3] pp incluye el cero y valores negativos; no hay evidencia concluyente de un aumento positivo.",
      "evidence_ids": ["E1"]
    },
    {
      "statement": "La tasa de quejas es 8% en treatment y 2% en control (mismo período y definición), es decir, un aumento de 6 pp.",
      "evidence_ids": ["E2"]
    },
    {
      "statement": "El aumento de quejas de 6 pp excede el guardrail autorizado de 2 pp, por lo que el guardrail no se cumple.",
      "evidence_ids": ["E2"]
    },
    {
      "statement": "No se puede calcular ROI porque no hay margen ni costes, y no existe permiso para modificar el guardrail.",
      "evidence_ids": ["E3"]
    }
  ],
  "draft_claim_review": [
    {
      "id": "C1",
      "status": "contradicted",
      "reason": "El IC95% [-1, 3] pp incluye el cero y valores negativos, y E1 indica explícitamente que no hay evidencia concluyente de aumento positivo; por tanto 'está demostrado' es incompatible con la evidencia.",
      "evidence_ids": ["E1"]
    },
    {
      "id": "C2",
      "status": "contradicted",
      "reason": "8% - 2% = 6 pp, no 1 pp. El 1 pp corresponde a la estimación de conversión, no a las quejas.",
      "evidence_ids": ["E2"]
    },
    {
      "id": "C3",
      "status": "contradicted",
      "reason": "El aumento de quejas (6 pp) supera el máximo autorizado de 2 pp, y E3 indica que no hay permiso para cambiar el guardrail.",
      "evidence_ids": ["E2", "E3"]
    }
  ],
  "numeric_findings": {
    "estimated_conversion_delta_pp": 1,
    "complaint_delta_pp": 6,
    "roi_pct": null
  },
  "limitations": [
    "El IC95% de conversión [-1, 3] pp incluye el cero; no se recalculó el intervalo, según lo indicado.",
    "No hay margen ni costes, por lo que el ROI no es identificable (null).",
    "No se proveen tamaños de muestra ni intervalo de confianza para la diferencia de quejas; solo se usan las tasas puntuales de E2.",
    "No hay permiso para cambiar el guardrail de quejas (máx. 2 pp).",
    "Evidencia limitada a un ensayo A/B ficticio de septiembre 2025; no se extrapola a otros períodos o poblaciones.",
    "No se buscaron fuentes externas; solo E1, E2 y E3."
  ],
  "next_action": {
    "owner": "PM de crecimiento",
    "action": "Revisar este memo y decidir si se mantiene sin escalar la intervención; si se desea continuar, solicitar evidencia de conversión más concluyente, datos de margen y costes para el ROI, y un plan para reducir quejas por debajo de 2 pp. Cualquier cambio de guardrail debe ser decidido por quien tenga autoridad para ello. Propuesta sujeta a revisión humana."
  },
  "gate_decision": "NEEDS_REVIEW"
}
```
