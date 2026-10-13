---
skill: acos-eval:detect-leakage
version: 0.1.0 (según plantilla de la skill; no verificada en runtime)
fecha: 2026-10-11
proyecto: (sin especificar)
inputs:
  - case.md — sha256:db7f2572bc7e591a8d537735dade9cdbcc1da74a100ecb2dd245673b3540e951
  - inputs/context.md — sha256:ae79d0d67bdd4f71349d51644732c99ae1ce547ad618a6d663a30195042b1c7e
  - inputs/dictionary.json — sha256:72636cf89cf406c70e90c0c1325ddcb7c89229a915199153c35c9f167c414fe3
  - inputs/observations.csv — sha256:32ae7c42472e440093583da2798aba677eb2ceae58289e5d5dc77f3e46354532 (3 filas, 5 columnas)
estado: No determinable; sin evidencia confirmada de leakage, con riesgo temporal alto pendiente de datos de proceso
---

# Auditoría de leakage — feature `complaint_count` (L03, churn 30 días)

## Resumen

- **Evidencia de leakage:** no confirmada. Tampoco puede descartarse. La feature `complaint_count` no tiene fecha de disponibilidad, ventana de conteo ni código de construcción en el expediente.
- **Familias implicadas:** temporal (riesgo principal) y post-event (si el conteo refleja el estado a la exportación, 2025-08-01, y no al scoring, 2025-06-01). Target, split, preprocessing, joins y resampling: no evaluables (no hay código ni split).
- **Estrategia de validación:** con la información actual no es posible confirmar una validación fiable. Falta el momento de disponibilidad de la feature y la forma de particionar.

## Hallazgos

### Alto

**H1 — Temporal / post-event potencial sobre `complaint_count`**
- **Componente:** feature `complaint_count` (dictionary.json; observations.csv).
- **Mecanismo:** `prediction_at` = 2025-06-01T00:00:00Z, pero `exported_at` = 2025-08-01T00:00:00Z y el expediente indica que la exportación contiene outcomes posteriores al scoring. Si el conteo se construyó con reclamos hasta la fecha de exportación, incorporaría información posterior a la predicción (y posiblemente reclamos ligados a la propia cancelación). Si se construyó hasta 2025-06-01, no hay leakage temporal.
- **Evidencia:** context.md declara "No se conoce si el conteo refleja el estado al scoring o al exportar". dictionary.json: `feature_available_at: null`, `construction_code: null`, ventana "no documentada".
- **Confianza:** No determinable (mecanismo plausible, sin dato que lo confirme ni lo descarte).
- **Impacto potencial:** métricas de churn sobrestimadas y modelo que no generaliza a scoring real.
- **Prueba necesaria:** fecha de generación/disponibilidad de `complaint_count`; ventana exacta de conteo (p. ej. reclamos con timestamp < prediction_at); versión histórica del campo al 2025-06-01 o extracción con corte temporal.
- **Acción recomendada:** no eliminar la variable. Reconstruirla con reclamos estrictamente anteriores a `prediction_at` (ventana documentada) y verificar que coincide con el valor de producción en esa fecha.

### Riesgo

**R1 — Ausencia de código y de split**
- **Componente:** pipeline y validación (no presentes).
- **Familia:** cross-validation / train-test contamination / preprocessing (no evaluables).
- **Confianza:** Riesgo (no hay artefacto para verificar `fit` antes del split, joins ni solape de clientes).
- **Acción:** aportar el código de construcción y el esquema de validación (split temporal o por cliente) antes de confiar en métricas.

### Informativo

**I1 — Target con outcomes posteriores al scoring.** El target (`cancelled_next_30d`) se define en la ventana posterior a 2025-06-01 y es correcto por diseño. No constituye leakage por sí mismo; solo lo sería si alguna feature usase ese mismo periodo.

## Evidencia

Checks deterministas realizados:
- **Hashes y conteos** (utilidad `check_inputs.py`, ejecutada una vez): 3 filas en observations.csv, columnas `customer_id, prediction_at, exported_at, complaint_count, cancelled_next_30d`; hashes registrados en el frontmatter.
- **Relación feature-target:** en 3 filas, `complaint_count` = 3→target 1 (U01), 0→0 (U02), 2→0 (U03). No hay igualdad ni mapeo 1:1: **no se detecta target leakage directo**. Con 3 observaciones, cualquier AUC univariante no es estadísticamente significativo; no se calcula como evidencia.
- **Ventana temporal:** `prediction_at` idéntico en todas las filas (2025-06-01); `exported_at` idéntico (2025-08-01). Todas las filas comparten fechas; no hay información por fila para verificar la ventana de cada conteo.
- **Solape de entidades y de fechas entre particiones:** no evaluable (no hay split).
- **Orden de operaciones en código:** no evaluable (`construction_code: null`).
- **Cardinalidad de joins:** no evaluable (una sola tabla, sin joins documentados).

Límites de inspección: solo se leyeron los inputs autorizados; no se ejecutó pipeline ni se entrenó nada. El expediente contiene 3 filas sintéticas, insuficientes para cualquier conclusión estadística.

## Preguntas abiertas

1. ¿Cuándo se genera `complaint_count` (fecha real de disponibilidad en producción)?
2. ¿Qué ventana cuenta los reclamos (p. ej. últimos N días antes de `prediction_at`, o histórico completo)?
3. ¿El valor exportado corresponde al estado al 2025-06-01 o al 2025-08-01?
4. ¿Los reclamos pueden estar causados por el propio proceso de cancelación (p. ej. reclamo de cierre)? Requiere validación de un experto de negocio.
5. ¿Existe código de construcción y un esquema de split? ¿Quién es el owner para aceptar la definición?

## Recomendaciones

1. Obtener la fecha de disponibilidad y la ventana de `complaint_count` antes de usar la feature.
2. Si el conteo usa datos posteriores a 2025-06-01, reconstruirlo con reclamos anteriores a `prediction_at` (no eliminar la variable sin antes intentar la reconstrucción).
3. Aportar código de construcción y esquema de validación; verificar split temporal y ausencia de solape de clientes.
4. Repetir esta auditoría con el dataset completo; 3 filas no permiten medir efectos.
5. No tomar métricas del modelo como válidas hasta cerrar H1.
