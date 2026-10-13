```markdown
---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-11
estado_auditoria: parcial; sin split/fit/código real
condicion: rehearsal
decision_id: RET-01
inputs: expediente incrustado
---

# Auditoría de leakage — RET-01

## Resumen
Feature `usage_previous_30d` con ventana previa y disponibilidad 2025-10-31T23:00Z, anterior al scoring 2025-11-01T08:00Z. Temporalidad plausible, no verificada en proceso. Sin split, fit ni código.

## Hallazgos
- Riesgo (medio): disponibilidad real del feature no verificada en el pipeline. Acción: confirmar fuente y corte.

## Evidencia
- Expediente: ventana previa, disponible 2025-10-31T23:00Z, scoring 2025-11-01T08:00Z.

## Preguntas abiertas
- ¿El pipeline de producción calcula `usage_previous_30d` solo con datos disponibles antes de 2025-11-01T08:00Z?

## Recomendaciones
- Verificar corte temporal en código de construcción.
- Auditar split y fit de preprocesamiento cuando existan.

## Límites
No demuestra ausencia de leakage ni generalización. Sin código, split ni fit, no se verificó ningún control.
```