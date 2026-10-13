```json
{
  "recommendation": "No autorizar un despliegue completo basado solo en el ranking. Se propone, para revisión, un piloto acotado con grupo de tratamiento y control aleatorizado sobre los seleccionados, con costos, margen y criterio de éxito definidos antes de contactar. La evidencia actual (E1) muestra que el ranking concentra más positivos que el azar (20% vs 10% esperado) en la población evaluada, pero E2 solo documenta MRR expuesto (USD 120000), no beneficio recuperable. Sin intervención observada, efecto incremental, coste ni margen, no se puede afirmar recuperación ni ROI. La recomendación cambiaría si un piloto mostrara efecto incremental positivo que supere los costos de contacto e implementación.",
  "claims": [
    {
      "statement": "Precision@50 descriptiva es 20% (10 positivos de 50 seleccionados) en la población evaluada observada.",
      "evidence_ids": ["E1"]
    },
    {
      "statement": "El comparador aleatorio esperado es 10%, por lo que la precision descriptiva es el doble (diferencia de 10 pp), como asociación predictiva y no como efecto de una campaña.",
      "evidence_ids": ["E1"]
    },
    {
      "statement": "El MRR expuesto de los seleccionados es USD 120000; es una medida de exposición, no beneficio recuperado.",
      "evidence_ids": ["E2"]
    },
    {
      "statement": "No hay contactos realizados, tratamiento/control, coste, margen ni efecto incremental observados, por lo que no es posible estimar impacto incremental ni ROI.",
      "evidence_ids": ["E1", "E2"]
    }
  ],
  "draft_claim_review": [
    {
      "id": "A1",
      "status": "contradicted",
      "reason": "E2 indica expresamente que USD 120000 es MRR expuesto y no representa beneficio recuperado. Tratar la exposición como recuperación contradice la fuente; además no hay intervención ni efecto incremental observados. Como mínimo, la afirmación carece de soporte, pero la fuente la refuta de forma directa.",
      "evidence_ids": ["E2"]
    },
    {
      "id": "A2",
      "status": "unsupported",
      "reason": "El ROI requiere beneficio incremental y coste. E2 señala que no hay coste, margen, efecto incremental ni intervención observada, por lo que el 300% no puede derivarse ni refutarse aritméticamente con la evidencia disponible.",
      "evidence_ids": ["E2"]
    },
    {
      "id": "A3",
      "status": "supported",
      "reason": "10 positivos / 50 seleccionados = 0.20 = 20%, coincide con E1. Se mantiene como cifra descriptiva sobre la población evaluada observada.",
      "evidence_ids": ["E1"]
    }
  ],
  "numeric_findings": {
    "precision": 0.2,
    "incremental_impact_usd": null,
    "roi_pct": null
  },
  "limitations": [
    "Precision@50 es descriptiva sobre la población evaluada observada; no se indica período de evaluación ni validación fuera de muestra, por lo que no se extrapola.",
    "El comparador aleatorio de 10% es esperado, no observado; la diferencia de 10 pp es una asociación predictiva, no un efecto causal.",
    "Con solo 50 seleccionados (10 positivos) la incertidumbre de la precision es alta; no hay intervalo de confianza en la evidencia.",
    "USD 120000 de MRR expuesto es exposición, no beneficio recuperado ni incremental.",
    "No hay contactos, tratamiento/control, costes de contacto o implementación, margen ni capacidad operativa, por lo que incremental_impact_usd y roi_pct son no identificables (null).",
    "No se definen outcome de retención, mecanismo de intervención, escenarios base/alto/bajo ni criterio de continuar/cambiar.",
    "No se buscaron fuentes externas; todo se basa en las fuentes ficticias E1 y E2 (E3 no fue provista con contenido)."
  ],
  "next_action": {
    "owner": "Responsable de retención",
    "action": "Proponer para review un diseño de piloto con tratamiento/control sobre los seleccionados, y reunir coste de contacto, margen y capacidad operativa, definiendo antes del contacto el outcome y el criterio de continuar/cambiar. No se fijan plazos ni presupuesto por no estar provistos."
  },
  "gate_decision": "NEEDS_REVIEW"
}
```
