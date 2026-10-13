# Manual del engagement retail — cerrado

## Status

COMPLETED. David aprobó todas las etapas y gates, incluido Handoff. Ver .acos/state.yaml y reports/handoff/human-approval.json.

## Resultado

Conservar baseline historical_sales. Final histórico: Top100 de2.768 elegibles, GBP993.347,93 y41,25% de ventas válidas elegibles. Datos UCI reales; encargo/cliente/capacidad simulados. No estima efecto de contacto, ventas netas, margen, CLV completo o ROI.

## Consultar

- delivery/decision_memo.md y analytical_report.md: decisión/método/límites.
- evidence/claims.yaml:43claims tipados y verificados.
- handoff/runbook.md: reproducción en copia nueva desde lock/Excel.
- reports/handoff/reproduction.json: PASS, mismas selecciones/métricas,56tests en original/copia.
- handoff/capability_feedback.md: uso experimental y gaps, sin promoción Foundry.
- handoff/handoff-manifest.json:263archivos históricos congelados; approvals finales/estado fuera de freeze.

## Después del cierre

Conservar referencias y marcador original; no repetir holdout para modificar estrategia. Reproducir mismo cálculo solo en copia aislada con reproduce_retail.py y outputs nuevos. Para negocio/datos/estrategia nuevos iniciar contexto/versión y evaluación nueva. Cierre local no autoriza publicar, enviar, contactar clientes o modificar Foundry.

APIUS$0. Reproducción analítica comprobada macOSarm64/Python3.13.2; Windows/Linux no ejecutados para este análisis. Review final nativo del ejecutor, no independiente.
