```markdown
---
skill: none
version: null
fecha: 2026-10-11
estado_de_auditoria: no concluyente (expediente sin contenido verificable)
condicion: rehearsal
decision_id: RET-01
inputs: expediente incrustado
---

## Resumen
No se recibió contenido de expediente incrustado; la auditoría no puede verificar ofertas ni scoring.

## Hallazgos
- No hay datos de ofertas, scoring ni usage_previous_30d.
- No hay split, fit ni código real para validar.

## Evidencia
- El mensaje no contiene tablas, registros ni fragmentos del expediente.
- La ventana declarada (disponible 2025-10-31T23:00Z; scoring 2025-11-01T08:00Z) no puede contrastarse.

## Preguntas abiertas
- ¿Puede incrustarse el expediente completo con ofertas, timestamps y métricas de uso?

## Recomendaciones
- No priorizar ofertas para cancelación en 7 días hasta recibir y auditar el expediente.

## Límites
Sin evidencia, esta auditoría no respalda ninguna conclusión de seguridad ni de priorización.
```