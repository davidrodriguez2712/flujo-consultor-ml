---
skill: detect-leakage
version: 0.2.1
fecha: 2026-10-13
modo: guia_textual
estado: borrador_no_determinable
inputs:
- context.md
- dictionary.json
- observations.csv
---

## Resumen

No puedo concluir que `complaint_count` sea leakage confirmado ni que sea válido para scoring. La recomendación de hoy es no usarlo para scoring y mantenerlo en reserva provisional hasta obtener evidencia de disponibilidad.

## Hallazgos

- **Componente:** feature `complaint_count`. **Conclusión:** No determinable. **Brecha:** no hay ventana de conteo, fecha de disponibilidad ni código de construcción. **Confianza:** baja. **Severidad potencial:** alta, porque la exportación es posterior al scoring. **Acción:** reserva provisional.

## Evidencia

- Lectura del expediente: scoring 2025-06-01, exportación 2025-08-01, target a 30 días.
- Lectura de `dictionary.json`: `feature_available_at` y `construction_code` son `null`.
- Lectura de `observations.csv` (3 filas): no hay igualdad feature-target; esto no descarta leakage.

## Preguntas abiertas

- ¿El conteo corresponde a reclamos hasta 2025-06-01?
- ¿Cuál es la ventana exacta del conteo?
- ¿Cuándo estuvo disponible en producción?

## Recomendaciones

- No usar `complaint_count` para scoring hoy.
- Solicitar snapshot histórico al corte 2025-06-01T00:00:00Z con fuente verificable.
- Solicitar código de construcción y ventana.
- Solicitar fecha de disponibilidad efectiva.

La conclusión cambiaría con evidencia de ventana previa al scoring, disponibilidad efectiva anterior al scoring y linaje del código.