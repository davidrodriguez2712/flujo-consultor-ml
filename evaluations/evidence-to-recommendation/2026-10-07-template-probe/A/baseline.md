{
  "recommendation": "No autorizar un despliegue a escala ni comprometer cifras de recuperación o ROI. La evidencia solo muestra que el ranking concentra más positivos que el azar entre los 50 seleccionados (Precision@50 descriptiva 20% frente a 10% esperado al azar). No hay contactos, tratamiento/control, costes, margen ni efecto incremental, por lo que no se puede estimar beneficio recuperado ni ROI. Se propone, para revisión, un piloto acotado con grupo de control aleatorio, costes y margen definidos de antemano, y criterios de continuar/cambiar fijados antes de contactar. Los USD 120000 son MRR expuesto, no beneficio recuperable.",
  "claims": [
    {
      "statement": "La Precision@50 descriptiva observada es 20% (10 positivos de 50 seleccionados), frente a 10% esperado con selección aleatoria; es un resultado predictivo descriptivo sobre la población evaluada observada, no un efecto de campaña.",
      "evidence_ids": ["E1"]
    },
    {
      "statement": "Los USD 120000 son MRR expuesto de los seleccionados y no representan beneficio recuperado.",
      "evidence_ids": ["E2"]
    },
    {
      "statement": "No existe evidencia de coste, margen, efecto incremental ni intervención observada, por lo que el impacto incremental y el ROI no son identificables con las fuentes provistas.",
      "evidence_ids": ["E2"]
    },
    {
      "statement": "El lift descriptivo de 2x sobre el azar (20% vs 10%) no equivale a retorno incremental; no hay tratamiento/control ni contactos realizados.",
      "evidence_ids": ["E1", "E2"]
    }
  ],
  "draft_claim_review": [
    {
      "id": "A1",
      "status": "contradicted",
      "reason": "Presenta como recuperación futura lo que E2 define como MRR expuesto, que explícitamente no representa beneficio recuperado. Además no hay intervención ni efecto incremental observados, así que USD 120000 no puede ser el resultado de la campaña. Como mínimo es no sustentado; se marca contradicted porque E2 niega directamente la equivalencia.",
      "evidence_ids": ["E2"]
    },
    {
      "id": "A2",
      "status": "unsupported",
      "reason": "El ROI requiere beneficio incremental y coste; ninguno está en la evidencia (E2 indica que no hay coste, margen ni efecto incremental). El 300% no tiene base y tampoco se puede refutar aritméticamente, por lo que queda sin soporte.",
      "evidence_ids": ["E2"]
    },
    {
      "id": "A3",
      "status": "supported",
      "reason": "10 positivos / 50 seleccionados = 0.20 = 20%, coincide con E1. Es descriptiva sobre la población evaluada observada.",
      "evidence_ids": ["E1"]
    }
  ],
  "numeric_findings": {
    "precision": 0.2,
    "incremental_impact_usd": null,
    "roi_pct": null
  },
  "limitations": [
    "Precision@50 es descriptiva sobre 50 seleccionados de la población evaluada observada; no se informa intervalo de incertidumbre ni generalización a otras poblaciones o periodos.",
    "El comparador aleatorio de 10% es un valor esperado dado en E1; no se verificó su derivación a partir de los datos.",
    "No hay contactos realizados ni diseño tratamiento/control, por lo que no se puede identificar efecto causal ni impacto incremental.",
    "USD 120000 es MRR expuesto, no beneficio recuperado ni ahorro; no se debe usar como retorno.",
    "No hay datos de coste de contacto, implementación, margen ni capacidad operativa, por lo que el ROI no es calculable.",
    "No se dispone de escenarios base/alto/bajo ni de plazos o presupuesto; no se inventan en este memo.",
    "Solo se usaron las fuentes ficticias E1 y E2 provistas; no se buscó información externa. E3 se mencionó como referencia posible en el encargo pero no figura en la evidencia entregada.",
    "La clasificación, audiencia y canal de distribución del memo no están confirmados."
  ],
  "next_action": {
    "owner": "Responsable de retención",
    "action": "Revisar este memo y decidir si se diseña un piloto acotado con grupo de control aleatorio, definiendo previamente coste de contacto, margen, outcome de retención y criterio de continuar/cambiar, antes de cualquier despliegue. Es una propuesta sujeta a revisión humana; no se ha aprobado ni ejecutado nada."
  },
  "gate_decision": "NEEDS_REVIEW"
}
