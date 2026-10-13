---
fecha: 2026-10-11
caso: L01
skill: none
skill_version: null
inputs:
  - path: case.md
    sha256: 89f1c1a622a64a73dafb5b641d871d372e72a1076533a23378ec2446f11e1e14
    bytes: 1728
  - path: inputs/context.md
    sha256: 3e3db7db6249d33479a7e01fdcaee3f8f8fec3f898f7c863e2d252398e613552
    bytes: 776
  - path: inputs/observations.csv
    sha256: 29e4badcbbcbf9e242bde9f2d31b80d1f55091a52d094b658e6992a457ad0f19
    bytes: 417
    filas: 4
  - path: inputs/pipeline.py
    sha256: fb122bed11f58973887818405e1b992b1589a72f8faf0ea13daf98ddb2f3da63
    bytes: 204
estado: completado (auditoría de expediente; sin validación de dominio)
condicion: hallazgos críticos de leakage en el conjunto de features declarado; no se aprueba ningún gate
---

# Reporte de auditoría de leakage — L01

## Resumen

El conjunto de features declarado (`history_kwh_90d`, `recovered_kwh`) contiene una feature con leakage post-evento confirmado por timestamps: `recovered_kwh` no estaba disponible en el momento de scoring (2025-06-01T00:00:00Z). Su disponibilidad en el expediente es entre 2025-06-09 y 2025-06-12, es decir, posterior al scoring y a la inspección. `history_kwh_90d` cumple el criterio temporal declarado. No se evaluó performance, split ni fit de transformaciones, porque no están en el expediente.

## Hallazgos

**H1 — Post-event leakage por `recovered_kwh` (crítico, confianza: Confirmado)**
- Componente: `inputs/pipeline.py` (línea 2, `FEATURE_COLUMNS`) y columna `recovered_kwh` de `inputs/observations.csv`.
- Mecanismo: el valor se determina al procesar la inspección; el contexto indica que no existe para el sistema hasta `recovered_available_at`, y que un cero posterior tampoco era dato conocido al scoring.
- Evidencia: en las 4 filas, `recovered_available_at` (2025-06-09T12:00Z, 06-10, 06-11, 06-12) es posterior a `prediction_at` (2025-06-01T00:00Z). La columna está incluida en `build_features` (pipeline.py líneas 3-4), sin filtro temporal.
- Acción propuesta: excluir `recovered_kwh` del conjunto de features de scoring. Si se necesita como auxiliar de evaluación, documentarlo como outcome, no como feature. No eliminar automáticamente; decisión del equipo.

**H2 — Riesgo de proxy del target en `recovered_kwh` (alto, confianza: Probable)**
- Mecanismo: `recovered_kwh` se mide en la inspección que define `fraud_confirmed`, por lo que puede codificar directamente el outcome.
- Evidencia descriptiva (4 filas, no es una métrica): `recovered_kwh > 0` coincide con `fraud_confirmed = 1` en S01 y S03; `recovered_kwh = 0` coincide con `fraud_confirmed = 0` en S02 y S04. Con 4 filas no se puede concluir sobre la fuerza de la relación.
- Acción propuesta: mantener H1 como bloqueante; no usar esta coincidencia para estimar performance.

**H3 — Temporalidad de `history_kwh_90d` (informativo, confianza: Confirmado en el expediente)**
- Evidencia: `history_available_at` = 2025-05-31T23:00:00Z en las 4 filas, anterior a `prediction_at` (2025-06-01T00:00:00Z). Coincide con la descripción de `inputs/context.md`.
- Límite: esto verifica solo los timestamps declarados; no verifica cómo se calculó la ventana de 90 días ni su origen, porque el expediente no incluye esa lógica.
- Acción propuesta: ninguna por ahora; confirmar la lógica de construcción fuera de este expediente.

## Evidencia

- `case.md`: contrato de la tarea; auditar features sin calcular performance ni entrenar.
- `inputs/context.md`: unidad de scoring, ventana del target (14 días), disponibilidad de `history_kwh_90d` y `recovered_kwh`.
- `inputs/observations.csv`: 4 filas sintéticas, columnas y timestamps citados arriba.
- `inputs/pipeline.py`: fragmento con selección de columnas; no contiene split, fit ni cálculo de métricas.
- Verificación determinista: la utilidad `check_inputs.py` devolvió hashes, bytes y conteo de 4 filas coincidentes con la tabla del frontmatter. Los conteos y hashes son los de esa salida; no se recalcularon manualmente.

## Preguntas abiertas

1. ¿Cómo se construye `history_kwh_90d` (fuente, ventana y corte exacto)? No está en el expediente.
2. ¿El sistema productivo realmente usará `recovered_kwh` en scoring o solo está en este fragmento?
3. ¿Hay split, fit de imputadores/escaladores o target encoding fuera de `pipeline.py` que pudieran añadir otro leakage? No determinable con este expediente.
4. ¿Un experto del dominio confirma que `recovered_kwh` no tiene una versión disponible antes de la inspección?

## Recomendaciones

1. Retirar `recovered_kwh` de `FEATURE_COLUMNS` antes de cualquier entrenamiento o evaluación de scoring.
2. Añadir un filtro temporal explícito (`recovered_available_at <= prediction_at`) en la construcción de features, y un test que falle si se incumple.
3. Revisar el pipeline completo (split, fit, joins) con los artefactos reales; esta auditoría no los cubre.
4. Pedir validación de un experto del dominio sobre la semántica de las columnas.

## Límites de la inspección

- Datos sintéticos de 4 filas; no son representativos y no permiten conclusiones estadísticas.
- Se leyó el código del fragmento; no se ejecutó `pipeline.py`, no se entrenó ningún modelo y no se calcularon métricas.
- No se invocó la skill `acos-eval:detect-leakage`; por eso el frontmatter declara `skill: none`. La auditoría se hizo a partir de los inputs autorizados.
- No hay fuente de referencia del reviewer en el expediente; no se usó.
- Esta auditoría no aprueba gates ni decisiones de negocio.
