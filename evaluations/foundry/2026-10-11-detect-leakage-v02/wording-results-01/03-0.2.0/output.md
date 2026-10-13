```markdown
---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-11
estado: parcial, sin split/fit/código verificado
condicion: rehearsal
decision_id: RET-01
inputs: expediente incrustado
---

# Auditoría de leakage RET-01

## Resumen
Feature `usage_previous_30d` (ventana previa, disponible 2025-10-31T23:00Z) es admisible para scoring del 2025-11-01T08:00Z según el expediente. No hay split, fit ni código real; la seguridad no queda certificada.

## Hallazgos
- **Riesgo (no determinable):** ausencia de split/fit/código impide verificar que transformaciones se ajusten solo con train. Severidad media. Acción: obtener código de construcción y particiones.

## Evidencia
- Disponibilidad 2025-10-31T23:00Z anterior al cutoff 2025-11-01T08:00Z: consistente.

## Preguntas abiertas
¿El pipeline de construcción de `usage_previous_30d` y sus transformaciones ajustadas se ejecutan solo con datos de train?

## Recomendaciones
Revisar código de features y split antes de confiar en la métrica.

## Límites
No demuestra generalización ni ausencia universal de leakage.
```