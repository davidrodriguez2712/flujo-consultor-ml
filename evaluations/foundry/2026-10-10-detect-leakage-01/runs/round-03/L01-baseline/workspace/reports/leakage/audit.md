---
fecha: 2026-10-11
case: L01
estado: completado_con_limites
condicion: auditoria_estatica_de_features; sin ejecucion de pipeline ni metricas
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
    rows: 4
  - path: inputs/pipeline.py
    sha256: fb122bed11f58973887818405e1b992b1589a72f8faf0ea13daf98ddb2f3da63
    bytes: 204
---

# Resumen

La feature `recovered_kwh` introduce leakage. Su valor solo existe para el sistema desde `recovered_available_at` (2025-06-09 a 2025-06-12), posterior al scoring (`prediction_at` = 2025-06-01T00:00:00Z). `history_kwh_90d` está disponible antes del scoring (2025-05-31T23:00:00Z) y no presenta leakage temporal verificable. La severidad del hallazgo es alta: `recovered_kwh` debe excluirse de las features de scoring antes de cualquier evaluación.

# Hallazgos

## H1 — `recovered_kwh` usa información posterior al scoring
- **Componente:** `inputs/pipeline.py`, `FEATURE_COLUMNS` (línea 2) y `build_features` (líneas 3-4); columna `recovered_kwh` en `inputs/observations.csv`.
- **Mecanismo:** `recovered_kwh` se determina al procesar la inspección (`inputs/context.md`). Su disponibilidad (`recovered_available_at`) es 2025-06-09T12:00Z, 2025-06-10T12:00Z, 2025-06-11T12:00Z y 2025-06-12T12:00Z para S01-S04, todas posteriores a `prediction_at` 2025-06-01T00:00Z. Incluso los ceros (S02, S04) no eran conocidos al scoring, según el contexto.
- **Fuente:** `inputs/context.md` (párrafo único); `inputs/observations.csv` filas S01-S04; `inputs/pipeline.py` líneas 2-4.
- **Confianza:** alta para la asimetría temporal (verificada en datos y contexto); media-alta para el impacto, porque el pipeline no muestra cómo se usa la feature después.
- **Severidad:** alta.
- **Acción propuesta:** eliminar `recovered_kwh` de `FEATURE_COLUMNS` para el scoring; si se requiere como información histórica, usarla solo con filtro as-of (`recovered_available_at <= prediction_at`), lo cual en este expediente excluiría todas las filas.

## H2 — `history_kwh_90d` sin leakage temporal verificable
- **Componente:** `inputs/pipeline.py` (`history_kwh_90d`); `inputs/observations.csv` columna `history_available_at`.
- **Mecanismo:** `history_available_at` = 2025-05-31T23:00Z para S01-S04, anterior a `prediction_at`. Según el contexto, usa días anteriores al scoring.
- **Fuente:** `inputs/context.md`; `inputs/observations.csv` filas S01-S04.
- **Confianza:** media. Se basa en metadatos declarados; no se pudo comprobar el cálculo original de la columna.
- **Severidad:** baja (sin hallazgo confirmado).
- **Acción propuesta:** mantener, pero documentar que la ventana de 90 días debe calcularse solo con datos con timestamp ≤ 2025-05-31T23:00Z.

## H3 — Ausencia de control as-of en el pipeline
- **Componente:** `inputs/pipeline.py`, `build_features` (líneas 3-4).
- **Mecanismo:** `build_features` toma filas tal cual y no filtra por `*_available_at` ni por `prediction_at`. El control temporal depende por completo de quien prepara `rows`.
- **Fuente:** `inputs/pipeline.py` líneas 3-4.
- **Confianza:** alta (lectura directa del código).
- **Severidad:** media.
- **Acción propuesta:** añadir validación explícita de disponibilidad temporal por feature antes de construir el vector.

# Evidencia

- Verificación determinista (utility `check_inputs.py`, sin ejecutar `pipeline.py`): hashes SHA-256 y tamaños de los cuatro inputs listados arriba; `observations.csv` con 4 filas y las columnas esperadas, incluidas `history_available_at` y `recovered_available_at`.
- Comparación de timestamps (lectura manual de `observations.csv`): `history_available_at` < `prediction_at` en 4/4 filas; `recovered_available_at` > `prediction_at` en 4/4 filas.
- Lectura de código: `pipeline.py` declara solo dos features.

# Preguntas abiertas

1. ¿Quién es el owner que acepta la definición de `prediction_at` y la regla de disponibilidad de `recovered_kwh`? No consta en el expediente.
2. ¿Existe una versión de `recovered_kwh` disponible antes del scoring (por ejemplo, un snapshot)? No consta.
3. ¿Cómo se usan las features aguas abajo (split, fit, métricas)? Fuera del expediente; no se concluye sobre ello.

# Recomendaciones

- Excluir `recovered_kwh` del conjunto de features de scoring (H1, severidad alta).
- Documentar y, si procede, validar la disponibilidad temporal de `history_kwh_90d` (H2).
- Añadir control as-of en `build_features` (H3).
- No usar cualquier evaluación derivada de este conjunto hasta resolver H1; este reporte no mide performance.

# Límites de inspección

- Se leyeron solo los inputs autorizados. No se ejecutó `pipeline.py`, no se entrenó ni se calcularon métricas.
- Los datos son sintéticos y son solo 4 filas; los hallazgos describen la estructura del expediente, no una población.
- No se invocó la skill `acos-eval:detect-leakage`: no figura entre las capacidades disponibles, por lo que `skill` queda en `none`.
- No se pudo verificar si ya existía un reporte previo en la ruta de salida (la herramienta de lectura está restringida a los inputs); la escritura se realizó como reporte nuevo.
- Las partes ausentes (split, fit de transformaciones, métricas) no se evalúan.
