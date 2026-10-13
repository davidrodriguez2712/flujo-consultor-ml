```markdown
---
skill: detect-leakage
version: 0.1.0
fecha: 2026-10-11
estado: auditoría parcial; sin hallazgos confirmados de leakage
condicion: rehearsal
decision_id: RET-01
inputs: expediente incrustado
---

## Resumen
Expediente insuficiente para concluir leakage. Se conoce `usage_previous_30d` con ventana previa y disponibilidad 2025-10-31T23:00Z, anterior al scoring 2025-11-01T08:00Z. Ese patrón es compatible con información legítima, pero no está verificado.

## Hallazgos
- **Medio, Riesgo:** no hay código, split ni fit que confirmen que la ventana de `usage_previous_30d` excluye observaciones posteriores al scoring.
- **Informativo:** no se detecta target leakage ni post-event leakage con la información disponible.

## Evidencia
- Timestamp de disponibilidad (2025-10-31T23:00Z) anterior al scoring (2025-11-01T08:00Z).
- Ventana declarada como previa; sin definición de límites ni consulta.
- Sin split, fit, código, joins ni agregaciones inspeccionables.

## Preguntas abiertas
- ¿Cómo se calcula exactamente `usage_previous_30d` y en qué instante se congela su valor para cada suministro?

## Recomendaciones
- Obtener la consulta o código que genera `usage_previous_30d` y verificar que sólo usa datos previos a 2025-10-31T23:00Z.
- Auditar split y preprocesado (imputación, escalado, encoding) con el código real antes de confiar en métricas.
- Mantener la decisión RET-01 como rehearsal hasta cerrar la verificación.

## Límites
Auditoría basada solo en el expediente incrustado; no implica seguridad universal, no verifica datos reales ni valida semántica de negocio.
```