# Delivery contract

## Decisión y alcance

Entregar benchmark histórico de priorización retail y recomendación historical_sales [OBS001]. Encargo/cliente/capacidad simulados [LIM002]. No publicar ni enviar a terceros; David revisa entrega local. Audiencias: owner comercial simulado y responsable técnico.

## Inputs con autoridad

- `reports/validation/holdout-results.json`: decisión/métricas finales.
- `reports/validation/development-selection.json`: elección antes del final.
- `reports/validation/evidence-manifest.json`: hashes de evaluación.
- `reports/validation/human-approval.json`: aprobación Validation y reviews.
- `data/source_manifest.json`: licencia/provenance.
- `evidence/claims.yaml`: trazabilidad de cifras, supuestos, propuestas y límites.

## Outputs

- `decision/recommendation.md`: decisión y condiciones.
- `delivery/decision_memo.md`: síntesis ejecutiva.
- `delivery/analytical_report.md`: método, resultados y límites.
- `delivery/prioritization_retrospective.csv`: lista ilustrativa histórica.
- `reports/delivery/verification.json` y `evidence-manifest.json`: comprobaciones.

## Criterios de aceptación

Cifras coinciden con fuentes y misma población/horizonte; claims tipados y referenciados; ranking consistente con baseline congelado; español con terminología técnica preservada. Target positivo y exclusiones explícitos. No atribuir uplift, ventas netas, margen o ROI; no convertir lista histórica en campaña real [LIM001][LIM002]. Recomendación futura limitada a validar contexto actual y prueba causal [PROP001]. No deck/dashboard fuera de alcance.

## Review y continuidad

Gate Delivery NEEDS_REVIEW hasta aprobación explícita de David con evidencia. Luego Handoff: reconstrucción aislada desde lock, comparación de artefactos, runbook y feedback; no promocionar capacidades automáticamente. El pase de Delivery no declara COMPLETED el engagement.
