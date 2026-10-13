---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-13
modo: guia_textual
estado: borrador_no_recomendable_para_scoring
inputs: context.md, dictionary.json, observations.csv
---

## Resumen

No recomendar hoy usar complaint_count para scoring. El expediente no acredita cuándo existía el conteo ni qué ventana cubre. La exportación es posterior al scoring, así que no sirve como prueba de disponibilidad. Solo se verificó por lectura que las filas tienen prediction_at anterior a exported_at.

## Hallazgos

- **Disponibilidad no determinable (Riesgo, severidad alta):** sin feature_available_at ni código, no se sabe si el conteo estaba disponible al 2025-06-01.
- **Posible contaminación temporal (Riesgo, severidad alta):** la ventana del conteo es desconocida; podría incluir reclamos posteriores al scoring.
- **Sin confirmación de mecanismo (No determinable):** la muestra de tres filas no muestra igualdad feature-target; esto no descarta leakage.

## Evidencia

- Lectura: prediction_at 2025-06-01 y exported_at 2025-08-01 en las tres filas.
- Lectura: dictionary.json tiene feature_available_at y construction_code en null.
- Lectura: context.md indica que no se conoce si el conteo refleja estado al scoring o al exportar.
- No ejecutado: conteos, joins, duplicados ni comprobaciones de ventana (sin acceso a datos completos).

## Preguntas abiertas

- ¿Cuál es la fecha de disponibilidad de complaint_count en producción?
- ¿Qué ventana temporal cubre el conteo y con qué cutoff se calculó?
- ¿Existe una versión histórica del conteo como estaba al 2025-06-01?
- ¿Cuál es el código de construcción?

## Recomendaciones

- No usar complaint_count para scoring hasta cerrar las preguntas abiertas.
- Obtener código, ventana y fecha de disponibilidad, y reconstruir el conteo con corte al prediction_at si la fuente lo permite.
- Revisar después el resultado con comprobaciones deterministas y revisión humana del proceso.
- Evidencia que cambiaría la conclusión: fuente documentada de disponibilidad anterior al scoring, ventana con cutoff verificable y código que muestre el cálculo.