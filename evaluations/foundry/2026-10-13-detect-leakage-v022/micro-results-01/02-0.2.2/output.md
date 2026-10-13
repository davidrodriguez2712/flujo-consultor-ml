---
skill: detect-leakage
version: 0.2.2
fecha: 2026-10-13
modo: guia_textual
estado: no_determinable
inputs: context.md, dictionary.json, observations.csv
---

## Resumen

Con este expediente no puede confirmarse leakage de complaint_count, ni certificarse su validez temporal. Recomendación para hoy: no usarla para scoring hasta obtener evidencia de disponibilidad al scoring. Conclusión limitada al expediente suministrado; no se ejecutaron checks, entrenamiento ni verificaciones de producción.

## Hallazgos

- **Brecha (No determinable):** la ventana de conteo y la fecha de disponibilidad no están documentadas. Mecanismo potencial: el conteo podría incluir reclamos posteriores a 2025-06-01T00:00:00Z. Fuente: dictionary.json, context.md. Confianza baja en ambas direcciones. Severidad no estimable. Acción: uso provisional reservado (ver Recomendaciones).
- La exportación (2025-08-01) es posterior al scoring y no prueba disponibilidad ni el estado del conteo en esa fecha.

## Evidencia

- context.md: scoring 2025-06-01; exportación 2025-08-01; outcomes posteriores para evaluación retrospectiva.
- dictionary.json: feature_available_at y construction_code nulos.
- observations.csv (lectura, sin hashes): 3 filas; exported_at posterior a prediction_at; complaint_count 3, 0, 2.

## Preguntas abiertas

- ¿Cuál es la ventana exacta y el corte temporal del conteo?
- ¿Existe código de construcción y versión histórica vigente al scoring?
- ¿Qué split y preprocessing se usaron?

## Recomendaciones

- **Condición de confirmación:** demostrar uso de reclamos posteriores al scoring, o disponibilidad posterior tratada como disponible.
- **Condición de posible validez:** ventana previa al scoring y disponibilidad efectiva al scoring, con linaje verificable.
- **Acción provisional:** no usar complaint_count para scoring hoy; reservar su uso a decisión del owner hasta recibir esta evidencia.