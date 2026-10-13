```markdown
---
skill: detect-leakage
version: 0.1.0
fecha: 2026-10-11
estado: auditoría parcial; sin evidencia de leakage confirmada; no concluyente
condicion: rehearsal
decision_id: RET-01
inputs: expediente incrustado
---

## Resumen
Expediente insuficiente para concluir. Feature `usage_previous_30d` con ventana previa y disponibilidad 2025-10-31T23:00Z, antes del scoring 2025-11-01T08:00Z. No hay evidencia de leakage temporal en la descripción; no hay split, fit ni código.

## Hallazgos
- **Informativo**: `usage_previous_30d` parece válida temporalmente. Confianza: Probable.
- **Riesgo (medio)**: sin código, no se verifica que la ventana se calcule solo con datos previos a la disponibilidad ni que no incluya el evento de cancelación.

## Evidencia
Ventana previa declarada; disponibilidad 2025-10-31T23:00Z < scoring 2025-11-01T08:00Z. Checks de split, solape de entidades, fit previo y cardinalidad de joins: no ejecutables.

## Preguntas abiertas
¿Cómo se calcula `usage_previous_30d` (fecha de corte exacta, tablas origen) y se verifica que excluye usos posteriores a 2025-10-31T23:00Z?

## Recomendaciones
Aportar código de generación de la feature y el esquema de validación antes de usar métricas para decidir. No eliminar la variable sin evidencia.

## Límites
Auditoría sin datos ni código; no garantiza ausencia de leakage ni sustituye validación de negocio.
```