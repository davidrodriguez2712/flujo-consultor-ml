---
fecha: 2026-10-11
caso: L01 (detect-leakage, baseline)
skill: none/null
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
    rows: 4
  - path: inputs/pipeline.py
    sha256: fb122bed11f58973887818405e1b992b1589a72f8faf0ea13daf98ddb2f3da63
    bytes: 204
estado: borrador para revisión humana
condicion: auditoría estática de features; sin ejecución de pipeline, sin métricas
---

# Resumen

Se identificó **una fuga crítica**: `recovered_kwh` figura como feature en `pipeline.py` pero se conoce solo después del scoring (desde 2025-06-09 a 2025-06-12, frente a un scoring el 2025-06-01). `history_kwh_90d` no presenta fuga por timestamp. El expediente no permite evaluar split, fit ni métricas.

# Hallazgos

**H1 — Fuga de información futura en `recovered_kwh`**
- Componente: `inputs/pipeline.py` (línea 2, `FEATURE_COLUMNS`; línea 4, `build_features`).
- Mecanismo: el valor se determina al procesar la inspección y solo existe desde `recovered_available_at`, posterior a `prediction_at`. Un cero posterior tampoco era dato conocido al scoring (`inputs/context.md`).
- Fuente: `inputs/observations.csv` filas S01–S04 (`prediction_at`=2025-06-01T00:00:00Z; `recovered_available_at` = 06-09, 06-10, 06-11, 06-12); `inputs/context.md`.
- Confianza: alta (la disponibilidad posterior está declarada y es verificable en las filas).
- Severidad: crítica.
- Acción propuesta: excluir `recovered_kwh` del conjunto de features de scoring; re-auditar cualquier variante que lo use indirectamente (p. ej., agregados o flags derivados de inspección). Confirmar con el owner del dato la definición de disponibilidad.

**H2 — `history_kwh_90d` sin fuga por timestamp**
- Componente: `inputs/pipeline.py` (línea 2).
- Mecanismo: `history_available_at` = 2025-05-31T23:00:00Z, anterior al scoring (2025-06-01T00:00:00Z) en las 4 filas.
- Fuente: `inputs/observations.csv`; `inputs/context.md`.
- Confianza: media-alta. Verificado por timestamp; no se pudo verificar que la ventana de 90 días se calcule solo con datos previos (la lógica de construcción no está en el expediente).
- Severidad: baja (sin hallazgo confirmado).
- Acción propuesta: solicitar la query/código que genera la columna y confirmar que la ventana termina antes del scoring.

# Evidencia

- Verificación determinista (`.runtime/check_inputs.py`, ejecutada una vez): hashes, bytes y conteo de columnas/filas listados en el frontmatter. CSV con 7 columnas y 4 filas; `case.md` y `inputs/` íntegros respecto a esa ejecución.
- Lectura manual: `context.md`, `pipeline.py`, `observations.csv`, `workflow.md`, `case.md`.
- Observación descriptiva (n=4, sintético, no es métrica): las filas con `recovered_kwh` > 0 son las de `fraud_confirmed` = 1. Esto refuerza la sospecha de fuga, pero no se calcula ni se interpreta como performance.

# Preguntas abiertas

1. ¿Cómo se construye `history_kwh_90d` (ventana exacta y fuente)?
2. ¿Existen otras features derivadas de inspección fuera de las dos declaradas? El contexto afirma que no; no se verificó más allá del fragmento.
3. ¿Quién es el owner que acepta la definición de disponibilidad de `recovered_kwh`?

# Recomendaciones

- Bloquear `recovered_kwh` como feature de scoring (decisión humana requerida para cualquier excepción).
- Mantener `history_kwh_90d` condicionada a la verificación de la query pendiente.
- No usar ningún resultado de evaluación de este expediente como evidencia de rendimiento.

# Límites de inspección

- Solo se leyeron los archivos autorizados. No se ejecutó `pipeline.py`, no se entrenó nada, no hubo red ni instalación.
- Dataset sintético de 4 filas: no representa población ni permite inferencia estadística.
- Ausentes en el expediente: split, fit de transformaciones, métricas y construcción de labels. No se concluye sobre esas partes.
- Skill `acos-eval:detect-leakage` no disponible en este entorno; auditoría realizada sin skill (baseline).
- No se comprobó si ya existía un reporte previo en la ruta de salida; se escribió el reporte en esa ruta.
