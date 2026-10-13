# Handoff — revisión humana pendiente

## Resultado transferible

Baseline historical_sales. Final histórico: Top100 de2.768 elegibles, GBP993.347,93 y41,25% de ventas válidas elegibles. Dos modelos fijos no elegibles en development; sin reselección después del final. Datos reales UCI, engagement/cliente/capacidad simulados. No causalidad, ventas netas, CLV completo o ROI.

## Reproducción

Entorno nuevo Python3.13.2/macOSarm64, instalado desde lock:17paquetes coinciden. Excel original reconstruye normalizado y snapshots, respetando persistencia/lectura CSV. PASS con rtol1e-8/atol1e-6, keys/filas/métodos/selección exactamente iguales.

| Comparación | Filas |
|---|---:|
| Normalización desde Excel | 1.067.371 |
| Snapshots train/development | 39.677 |
| Snapshot final reservado | 2.768 |
| Predicciones development | 49.132 |
| Predicciones finales | 2.768 |
| Ranking seleccionado | 100 |

Métricas de development/final coinciden, decisión baseline exacta. Marcador original del holdout y resultados originales intactos. Una reproducción fallida del harness se conserva junto con causa/fix/test; no ampliar tolerancias ni cambiar modelos para hacerla pasar. Reproducción es mismo cálculo en copia, no segundo período de evaluación ni nueva evidencia de generalización.

## Pruebas y review

56tests pasan en original y entorno reconstruido. Revisión final nativa del mismo ejecutor (no reviewer independiente), con foco del plan/spec y límites de reutilización registrados. No FindingsCritical/Important abiertos en scope del benchmark aprobado. Helper de ranking no debe usarse con strings numéricos fuera del schema normalizado. No presentar esta comprobación local como análisis ejecutado en Windows/Linux.

## Archivos principales

- handoff/runbook.md
- handoff/business_handoff.md
- handoff/technical_handoff.md
- handoff/capability_feedback.md
- handoff/next_steps.md
- reports/handoff/reproduction.json
- reports/handoff/final-review.md
- handoff/handoff-manifest.json

Feedback mantiene las skills experimental0.1.0 y candidates existentes como conocimiento; no escrituras ni promociones Foundry. Gasto APIUS$0; tiempo/infraestructura no cuantificados.

## Aprobación solicitada

David debe revisar reproducción, documentación, límites y feedback para aprobar Handoff. Solo entonces registrar PASS, completar todas las etapas y estado COMPLETED. Delivery aprobado; Handoff es último gate pendiente, no cierre automático.
