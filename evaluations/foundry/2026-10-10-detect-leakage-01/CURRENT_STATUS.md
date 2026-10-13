# Estado actual — detect-leakage

2026-10-11: evaluación inicial ejecutada y revisada por el autor. Los documentos originales de preparación mantienen su estado histórico; este índice refleja el avance posterior.

- Cinco rondas preservadas; round05 tiene smoke+3pares completos, nativeSkill3/3treatments.
- 229 pruebas locales pasadas. API Anthropic estimada totalUS$0.07056525 de techoUS$0.10; 61solicitudes reales en cinco rondas, todasconusage conocido. No más API requerida para este cierre.
- Contenido baseline2/3, treatment3/3conobservaciones; conjunto de contenido/trazabilidad baseline2/3, treatment0/3. Falta condición en frontmatter de tres treatments; sin señal favorable bajo regla congelada. No generalizar desde casos guiados/sintéticos y una repetición.
- Recomendación mantener experimental supervisada, corregir contrato/entidades/disponibilidad y evaluar casos nuevos. Foundry/madurez canónicos sin cambios automáticos.
- Reporte: docs/acos/validation/2026-10-11-foundry-detect-leakage-evaluation-report.md.
- Propuestas: reviewer-followup-05/RECOMMENDATIONS.md.
- Actualización 2026-10-12: revisión distinta del autor completada en `independent-review-01/REVIEW.md`. Detecta fallos de fundamentación adicionales: contenido baseline2/3, treatment1/3; cumplimiento conjunto baseline1/3, treatment0/3 según su adjudicación. Se conserva el autorreview anterior sin sustituir sus juicios. Reviewer agente, no humano ni ciego; adjudicación humana pendiente si se decide madurez.
- Se ejecutó un estudio separado de 0.2.0 en `../2026-10-11-detect-leakage-v02/`. Canonical actualizado a 0.2.0 experimental supervisada; evidencia de 0.1.0 intacta. No se promueve madurez ni se reparan resultados históricos.
