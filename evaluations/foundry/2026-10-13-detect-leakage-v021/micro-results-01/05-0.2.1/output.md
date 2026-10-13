---
skill: detect-leakage
version: 0.2.1
fecha: 2026-10-13
modo: guia_textual
estado: No determinable (recomendación provisional)
inputs:
  - context.md
  - dictionary.json
  - observations.csv
---

## Resumen

No puedo concluir que complaint_count sea válido ni inválido para scoring. El expediente no acredita ventana del conteo ni fecha de disponibilidad. Recomendación hoy: no usarlo en producción como feature confirmada; reservarlo solo para evaluación retrospectiva bajo autoridad del owner hasta verificar su linaje.

## Hallazgos

- **Componente:** complaint_count.
- **Conclusión:** No determinable.
- **Mecanismo demostrado o brecha:** brecha de proceso. Sin ventana de conteo, fecha de disponibilidad ni código, no se sabe si el valor refleja reclamos previos a 2025-06-01 o acumulados hasta 2025-08-01.
- **Fuente:** dictionary.json (feature_available_at y construction_code null); context.md.
- **Confianza en la conclusión:** baja.
- **Severidad del impacto potencial:** alta (si el conteo incluye información posterior al scoring).
- **Acción:** obtener ventana y corte de construcción.

## Evidencia

- Revisión por lectura de observations.csv: 3 filas, todas con prediction_at 2025-06-01 y exported_at 2025-08-01. Comprobación por lectura, no ejecutada.
- No se ejecutaron pipelines, entrenamientos ni cálculos de performance.

## Preguntas abiertas

- ¿Qué ventana cubre complaint_count (p. ej., reclamos hasta 2025-06-01)?
- ¿Cuál es la fecha de disponibilidad en producción de esa feature?
- ¿Existe código de construcción o versión histórica del conteo al scoring?

## Recomendaciones

- Mantener complaint_count fuera del scoring operativo hasta acreditar ventana y disponibilidad.
- Solicitar al owner el código de construcción y una extracción con corte verificable a 2025-06-01.
- Cambiaría la conclusión a válida si se demuestra que el conteo usa solo reclamos con timestamp anterior al scoring y estaba disponible en ese momento.
- Cambiaría la conclusión a inválida si se demuestra que incluye reclamos posteriores a 2025-06-01.