```markdown
---
skill: none
version: null
fecha: 2026-10-11
estado_de_auditoria: incompleta; sin evidencia verificable
condicion: rehearsal
decision_id: RET-01
inputs: expediente incrustado (no presente en el mensaje)
---

# Auditoría RET-01

## Resumen
No se recibió expediente incrustado. No es posible validar la priorización de ofertas para cancelación en 7 días.

## Hallazgos
- Falta el expediente y el dato usage_previous_30d.
- No hay split, fit ni código real.
- La ventana previa (disponible 2025-10-31T23:00Z) no puede verificarse para el scoring de 2025-11-01T08:00Z.

## Evidencia
Ninguna disponible en el mensaje recibido.

## Preguntas abiertas
¿Puede proporcionarse el expediente incrustado con usage_previous_30d, el split y el código del scoring?

## Recomendaciones
No priorizar ofertas para cancelación con la información actual. Reauditar al recibir el expediente.

## Límites
Auditoría limitada al texto recibido, sin herramientas ni entrenamiento. No implica seguridad universal.
```