---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-12
inputs:
  - path: case.md
    sha256: 89f1c1a622a64a73dafb5b641d871d372e72a1076533a23378ec2446f11e1e14
  - path: inputs/context.md
    sha256: 3e3db7db6249d33479a7e01fdcaee3f8f8fec3f898f7c863e2d252398e613552
  - path: inputs/observations.csv
    sha256: 29e4badcbbcbf9e242bde9f2d31b80d1f55091a52d094b658e6992a457ad0f19
  - path: inputs/pipeline.py
    sha256: fb122bed11f58973887818405e1b992b1589a72f8faf0ea13daf98ddb2f3da63
estado: auditoría completada; hallazgos de leakage reportados; no es aprobación de gate
condicion: treatment
---

## Resumen

La feature `recovered_kwh` introduce información posterior al scoring: no existía para el sistema hasta `recovered_available_at` (2025-06-09 a 2025-06-12), mientras la predicción ocurre el 2025-06-01. Está declarada en `FEATURE_COLUMNS`. Se recomienda retirarla del scoring. `history_kwh_90d` no muestra mecanismo de leakage con el expediente disponible.

## Hallazgos

**H1. `recovered_kwh` como feature posterior al scoring**
- Componente: `inputs/pipeline.py` (FEATURE_COLUMNS, build_features).
- Mecanismo: valor determinado al procesar la inspección; disponible desde `recovered_available_at`, posterior a `prediction_at`.
- Fuente: context.md; observations.csv (columnas `recovered_kwh`, `recovered_available_at`, `prediction_at`).
- Confianza: alta.
- Severidad: alta.
- Acción: retirar `recovered_kwh` de las features de scoring; no usarlo como predictor.

**H2. Indicio de señal perfecta en la muestra**
- Componente: `recovered_kwh` frente a `fraud_confirmed`.
- Mecanismo: en las 4 filas, `recovered_kwh > 0` coincide con `fraud_confirmed = 1`. Es un indicio con n=4, no una medición.
- Fuente: observations.csv, filas S01–S04.
- Confianza: baja; no confirma mecanismo por sí solo.
- Severidad: media (refuerza H1).
- Acción: no usar esta coincidencia como evidencia de desempeño; revisar con muestra real.

**H3. `history_kwh_90d` sin mecanismo de leakage observado**
- Componente: `history_kwh_90d`.
- Evidencia: `history_available_at` = 2025-05-31T23:00:00Z, anterior a `prediction_at` = 2025-06-01T00:00:00Z; context.md indica uso de días anteriores al scoring.
- Confianza: media. La ventana de cálculo no está en el expediente.
- Severidad: no determinada como riesgo.
- Acción: verificar en la fuente la ventana y el corte de la agregación.

## Evidencia

- Hashes, columnas y conteos: utility `check_inputs.py` ejecutada una vez (4 entradas; CSV con 4 filas y 7 columnas).
- Timestamps comparados manualmente contra el cutoff de scoring (lectura de valores, no un check automatizado de pipeline).
- Código leído: `pipeline.py` (fragmento de 4 líneas). No se ejecutó pipeline, no se entrenó, no se calcularon métricas.

## Preguntas abiertas

- ¿Cómo se calcula `history_kwh_90d` en la fuente, y cuál es su corte real en producción?
- ¿Existe en producción un proceso que reconstruya `recovered_kwh` con disponibilidad histórica verificable?
- No se especifica el momento de entrenamiento, split ni fit de transformaciones; no se concluye sobre esas partes.
- Falta owner que acepte la definición de features para scoring.

## Recomendaciones

1. Retirar `recovered_kwh` de `FEATURE_COLUMNS` para scoring; conservarlo solo como outcome o dato de evaluación retrospectiva.
2. Verificar en la fuente la ventana y disponibilidad de `history_kwh_90d`.
3. Revisión humana del proceso de construcción antes de cualquier uso productivo.
4. Esta auditoría no aprueba gates ni certifica ausencia de leakage.
