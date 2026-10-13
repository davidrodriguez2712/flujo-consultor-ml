```markdown
---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-11
estado_auditoria: parcial; sin split/fit/código verificado
condicion: rehearsal
decision_id: RET-01
inputs: expediente incrustado
---

# Auditoría de leakage: RET-01

## Resumen
Feature `usage_previous_30d` disponible 2025-10-31T23:00Z; scoring 2025-11-01T08:00Z. Disponibilidad previa al scoring: válida en principio. Sin split, fit ni código: no certificable.

## Hallazgos
- Sin hallazgos confirmados.
- Riesgo: no verificado que la ventana no incluya datos posteriores a 2025-10-31T23:00Z (confianza baja, severidad media).

## Evidencia
- Timestamps declarados del expediente; no hay pipeline ni código.

## Preguntas abiertas
- ¿Cuál es la ventana exacta de `usage_previous_30d` y su proceso de cálculo, con corte verificado?

## Recomendaciones
- Verificar el corte de cálculo y que el train/fit use solo datos previos a cada fecha de predicción.
- No atribuir seguridad universal; la auditoría cubre solo el expediente.

## Límites
Sin ejecución ni acceso a código; no demuestra generalización ni ausencia de leakage.
```