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
Recomendación: no usar complaint_count para scoring hoy. Es una acción provisional, reservada a la autoridad del owner. Estado: No determinable. No hay mecanismo demostrado de leakage ni evidencia de validez temporal.

## Hallazgos
- complaint_count: brecha de disponibilidad. Sin ventana, fecha de corte ni código, no puede saberse si reflejaba el estado al scoring (2025-06-01). La exportación (2025-08-01) es posterior y no prueba disponibilidad. Fuente: context.md, dictionary.json. Confianza en la brecha: alta. Severidad: no estimable. Acción: ver Recomendaciones.

## Evidencia
- Lectura de context.md, dictionary.json y observations.csv (3 filas). No se ejecutaron cálculos ni checks deterministas.
- prediction_at 2025-06-01 y exported_at 2025-08-01 en todas las filas.
- feature_available_at y construction_code son null.

## Preguntas abiertas
- ¿Ventana y fecha de corte del conteo de reclamos?
- ¿Disponibilidad efectiva en producción al 2025-06-01?
- ¿Código de construcción y linaje?
- ¿Versión histórica del conteo al scoring?

## Recomendaciones
- Confirmación (no cumplida): demostrar información posterior usada como feature, o disponibilidad posterior usada como disponible al scoring.
- Posible validez temporal (no cumplida): ventana previa y disponibilidad efectiva al scoring, con linaje. La exportación no la satisface.
- Acción provisional: suspender el uso para scoring hasta obtener evidencia; decisión del owner.
- No certifica otras familias de leakage.