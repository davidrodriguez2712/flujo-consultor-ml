---
skill: detect-leakage
version: 0.2.2
fecha: 2026-10-13
modo: guia_textual
estado: no_determinable
inputs:
  - context.md
  - dictionary.json
  - observations.csv
---

## Resumen
Estado: No determinable. No se confirma leakage de complaint_count ni su validez temporal. Recomendación para hoy: no usar complaint_count en scoring; reserva provisional bajo autoridad del owner.

## Hallazgos
- Brecha de disponibilidad: no hay fecha de disponibilidad ni ventana de conteo. No se sabe si el valor refleja el estado al scoring (2025-06-01) o al exportar (2025-08-01). Confianza en esta brecha: alta. Severidad: no estimable. Condiciones y acción en Recomendaciones.
- La exportación posterior no prueba disponibilidad ni mecanismo. No se declara la feature inválida ni segura.

## Evidencia
- context.md: scoring 2025-06-01; exportación 2025-08-01 con outcomes posteriores; sin código de construcción ni versión histórica.
- dictionary.json: feature_available_at y construction_code en null.
- observations.csv: 3 filas, revisadas por lectura. Son insuficientes para estimar señal o impacto. No se ejecutaron checks deterministas.

## Preguntas abiertas
- ¿Desde cuándo y con qué ventana se calcula complaint_count en producción?
- ¿Existe un snapshot de complaint_count con corte 2025-06-01?
- ¿Cuál es el código de construcción y el linaje del campo?

## Recomendaciones
- Condición de confirmación: demostrar uso de información posterior, o disponibilidad efectiva posterior tratada como disponible al scoring.
- Condición de posible validez: ventana previa y disponibilidad efectiva al scoring, con linaje verificable.
- Acción provisional: no usar para scoring hoy; mantener reserva hasta obtener evidencia y decisión del owner.