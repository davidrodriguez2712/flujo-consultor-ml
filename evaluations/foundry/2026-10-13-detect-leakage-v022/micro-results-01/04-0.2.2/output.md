---
skill: detect-leakage
version: 0.2.2
fecha: 2026-10-13
modo: guia_textual
estado: no_determinable
inputs: context.md, dictionary.json, observations.csv
---
## Resumen

No determinable. No recomendaría usar complaint_count para scoring hoy: no consta fecha de disponibilidad, ventana ni construcción. La exportación del 2025-08-01 es posterior al scoring y no prueba nada. No confirmo leakage ni validez temporal.

## Hallazgos

- Brecha de disponibilidad: complaint_count podría incluir reclamos posteriores al 2025-06-01 (feature_available_at nulo). Fuente: dictionary.json, context.md. Confianza en la brecha: alta. Severidad: no estimable. Acción: retener uso bajo autoridad del owner.

## Evidencia

- context.md: scoring 2025-06-01; exportación 2025-08-01 con outcomes posteriores.
- dictionary.json: ventana, disponibilidad y construcción sin documentar.
- observations.csv: 3 filas; lectura sin mecanismo demostrado.

## Preguntas abiertas

- ¿Cuál es la ventana exacta y el cutoff del conteo?
- ¿Cuándo estuvo disponible en producción?
- ¿Existe snapshot histórico al 2025-06-01?

## Recomendaciones

- Confirmación: demostrar información posterior usada, o disponibilidad posterior tratada como disponible. No cumplida.
- Validez temporal: ventana previa y disponibilidad efectiva al scoring con linaje. No cumplida; la exportación no la satisface.
- Acción provisional: no usar para scoring hasta obtener evidencia; decisión del owner.
- Cambiaría la conclusión: código de construcción, feature_available_at, snapshot verificable o logs de producción.