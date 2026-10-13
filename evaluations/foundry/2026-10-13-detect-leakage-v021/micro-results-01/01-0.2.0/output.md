---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-13
modo: guia_textual
estado: borrador_no_certificado
inputs: context.md, dictionary.json, observations.csv
---

## Resumen

No recomendar usar complaint_count para scoring hoy. El expediente no acredita que el conteo estuviera disponible al 2025-06-01T00:00:00Z. Riesgo de leakage temporal no determinable, con sospecha razonable por ventana y versión desconocidas.

## Hallazgos

- **Disponibilidad temporal:** no determinable. `feature_available_at` es null y no hay código de construcción. Severidad alta.
- **Ventana de conteo:** no documentada; podría incluir reclamos posteriores al scoring. Severidad alta.
- **Estado al exportar vs. al scoring:** el conteo podría reflejar 2025-08-01 y no 2025-06-01. Riesgo, severidad alta.
- **Metadata del expediente:** 3 filas revisadas por lectura; no se ejecutaron checks deterministas.

## Evidencia

- Lectura de `dictionary.json`: ventana y disponibilidad no documentadas; campos de disponibilidad y código en null.
- Lectura de `context.md`: exportación 2025-08-01 incluye outcomes posteriores; no hay versión histórica.
- Lectura de `observations.csv`: 3 filas, `complaint_count` 3, 0, 2. Sin prueba de disponibilidad.

## Preguntas abiertas

- ¿Cuál es la fecha de disponibilidad de complaint_count en producción?
- ¿Qué ventana temporal cuenta los reclamos?
- ¿Existe snapshot histórico del conteo al 2025-06-01?
- ¿Cuál es el código de construcción?

## Recomendaciones

- No usar complaint_count en scoring hasta confirmar disponibilidad y ventana.
- Solicitar código de construcción y snapshot con corte verificable al 2025-06-01.
- Si solo existe el conteo de exportación, tratarlo como no válido para scoring.
- Evidencia que cambiaría la conclusión: fecha de disponibilidad anterior o igual a 2025-06-01 y ventana cerrada antes de esa fecha, verificadas en código o registro de proceso.