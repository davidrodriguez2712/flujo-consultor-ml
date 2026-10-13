---
skill: detect-leakage
version: 0.2.1
fecha: 2026-10-13
modo: guia_textual
estado: No determinable; no recomendar uso de complaint_count para scoring hoy
inputs:
  - context.md
  - dictionary.json
  - observations.csv
---

## Resumen
No puedo concluir que complaint_count sea válido para scoring. Tampoco puedo concluir que haya leakage demostrado. La brecha es de proceso: falta ventana de conteo y fecha de disponibilidad. La exportación del 2025-08-01 solo fecha el archivo, no el valor al scoring del 2025-06-01.

## Hallazgos
- **Componente:** complaint_count.
- **Conclusión:** No determinable.
- **Mecanismo demostrado o brecha:** Brecha. No hay ventana, disponibilidad, versión histórica ni código de construcción.
- **Fuente:** context.md; dictionary.json (feature_available_at y construction_code en null).
- **Confianza:** Baja en validez y en riesgo.
- **Severidad potencial:** Alta, porque el conteo podría incluir reclamos posteriores al scoring.
- **Acción:** Reserva de uso bajo autoridad del owner hasta acreditar disponibilidad.

## Evidencia
- Lectura del expediente: outcomes existen en la exportación para evaluación retrospectiva.
- Lectura de observations.csv: 3 filas, con complaint_count 3, 0, 2 y target 1, 0, 0. No es muestra suficiente para performance ni para conclusiones de generalización.
- No se ejecutaron checks deterministas ni pipelines.

## Preguntas abiertas
- ¿Qué ventana cubre complaint_count (p. ej., reclamos previos a 2025-06-01)?
- ¿Cuándo estuvo disponible en producción el valor usado al scoring?
- ¿Existe versión histórica o snapshot con corte verificable?
- ¿Cuál es el código de construcción y el orden de split/preprocessing?

## Recomendaciones
- No usar complaint_count para scoring hoy; mantenerlo solo como candidato en revisión.
- Solicitar al owner ventana, fecha de disponibilidad y código de construcción.
- Verificar con snapshot del 2025-06-01 o log de producción que el valor no incluye eventos posteriores.
- Reevaluar si la evidencia confirma ventana previa y disponibilidad al scoring.