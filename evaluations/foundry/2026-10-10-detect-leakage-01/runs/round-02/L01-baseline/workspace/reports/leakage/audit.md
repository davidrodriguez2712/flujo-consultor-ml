---
fecha: 2026-10-11
case_id: L01
tarea: auditoría de leakage de features (detect-leakage), baseline
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
estado: completado
condicion: baseline; hallazgo material de leakage confirmado por lectura del expediente; sin métricas ni fit
skill: none
skill_version: null
---

## Resumen

La feature `recovered_kwh` introduce información no disponible en el momento del scoring (`2025-06-01T00:00:00Z`). Según `inputs/context.md`, este valor se determina al procesar la inspección y solo existe para el sistema a partir de `recovered_available_at`, que en las cuatro filas del CSV es posterior al scoring (2025-06-09 a 2025-06-12). Es un leakage temporal material: el conjunto de features auditado no es válido para la situación de predicción declarada.

`history_kwh_90d` sí está disponible antes del scoring (`history_available_at = 2025-05-31T23:00:00Z`, anterior a `prediction_at`) y no presenta leakage temporal en el expediente.

No se calcularon métricas, no se entrenó ni se ejecutó `pipeline.py`. Las conclusiones se limitan a la disponibilidad temporal de las features.

## Hallazgos

### H1 — `recovered_kwh` usa información posterior al scoring

- **Componente:** `inputs/pipeline.py`, constante `FEATURE_COLUMNS` (línea 2) y función `build_features` (líneas 3-4), que incluye `recovered_kwh` en las features.
- **Mecanismo:** `recovered_kwh` es un resultado de la inspección. Según `context.md`, se determina al procesar la inspección, no existe para el sistema hasta `recovered_available_at` y "un cero posterior tampoco era dato conocido al scoring". En el CSV, `recovered_available_at` es 2025-06-09T12:00:00Z, 2025-06-10T12:00:00Z, 2025-06-11T12:00:00Z y 2025-06-12T12:00:00Z para S01 a S04, todos posteriores a `prediction_at = 2025-06-01T00:00:00Z`. Por tanto, el valor usado al scoring no estaba disponible. Además, el valor es un proxy directo del outcome: `recovered_kwh > 0` ocurre en S01 y S03, que son los dos casos con `fraud_confirmed = 1`, aunque con 4 filas esto no permite concluir una relación estadística.
- **Fuente:** `inputs/context.md` (párrafo único); `inputs/observations.csv` filas S01-S04, columnas `recovered_kwh`, `recovered_available_at`, `prediction_at`; `inputs/pipeline.py` líneas 2-4.
- **Confianza:** alta para la brecha temporal (verificada en el texto y en las 4 filas); media para el efecto de sobreajuste/proxy del outcome (inferencia sobre datos sintéticos de 4 filas).
- **Severidad:** alta. Invalida el conjunto de features para la predicción declarada.
- **Acción propuesta:** excluir `recovered_kwh` de `FEATURE_COLUMNS` y de cualquier construcción de features para scoring. Si se necesita un histórico de recuperaciones, construirlo solo con inspecciones con `recovered_available_at <= prediction_at` (en la fecha de scoring) y documentar la regla. No reemplazar el valor por un cero o imputación, porque la ausencia de dato tampoco era conocida al scoring.

### H2 — `history_kwh_90d` sin leakage temporal verificado

- **Componente:** `inputs/pipeline.py`, `FEATURE_COLUMNS` (línea 2).
- **Mecanismo:** la ventana declarada usa días anteriores al scoring y `history_available_at = 2025-05-31T23:00:00Z` es anterior a `prediction_at = 2025-06-01T00:00:00Z` en todas las filas. No se observa un valor posterior al scoring.
- **Fuente:** `inputs/context.md`; `inputs/observations.csv` columnas `history_kwh_90d`, `history_available_at`, `prediction_at`.
- **Confianza:** media. Depende de que la ventana de 90 días efectivamente termine en `history_available_at`, lo cual está declarado pero no se puede verificar desde el código (el fragmento no calcula la columna).
- **Severidad:** baja (sin hallazgo activo; queda como verificación pendiente).
- **Acción propuesta:** mantener, y pedir la query o el proceso que genera `history_kwh_90d` para confirmar la ventana y el corte.

## Evidencia

- `case.md`: tarea de auditoría de features; prohíbe calcular performance, entrenar o ejecutar `pipeline.py`.
- `inputs/context.md`: scoring en `2025-06-01T00:00:00Z`; `history_kwh_90d` disponible desde `2025-05-31T23:00:00Z`; `recovered_kwh` no disponible hasta `recovered_available_at`; las dos columnas de `pipeline.py` son todas las features auditadas.
- `inputs/pipeline.py`: `FEATURE_COLUMNS = ["history_kwh_90d", "recovered_kwh"]`; `build_features` selecciona esas columnas sin filtro temporal. Es un fragmento sin lógica de split, fit ni métricas.
- `inputs/observations.csv` (4 filas de datos, revisión manual): todas las filas tienen `prediction_at = 2025-06-01T00:00:00Z` y `history_available_at = 2025-05-31T23:00:00Z`; `recovered_available_at` posterior en 8 a 11 días en cada fila.
- Verificación determinista disponible: la utilidad `.runtime/check_inputs.py` se ejecutó una vez y devolvió los hashes, tamaños, columnas y conteo de filas listados en el frontmatter. No verifica timestamps ni leakage; la comparación de fechas anterior se hizo por lectura del CSV, no con un script.

## Límites de la inspección

- Solo se leyeron los archivos autorizados; no se ejecutó `pipeline.py`, no se calcularon métricas ni se entrenó nada.
- El dataset tiene 4 filas sintéticas: sirve para mostrar la brecha temporal, no para estimar magnitud ni efecto estadístico.
- No se dispone del proceso que genera `history_kwh_90d` ni del código de split/fit; el hallazgo H1 se refiere solo a la feature declarada en el fragmento.
- No se verificó si el modelo productivo usa `build_features` tal cual.
- No se invocó ninguna skill (`acos-eval:detect-leakage` no estaba disponible); el análisis es manual.

## Preguntas abiertas

1. ¿Existe alguna versión de `recovered_kwh` disponible al scoring (por ejemplo, un histórico de inspecciones previas con fecha de conocimiento)? Si no existe, la feature debe retirarse.
2. ¿Qué proceso y query generan `history_kwh_90d`, y confirman que la ventana termina en `history_available_at`?
3. ¿El modelo o el scoring real consumen `build_features` de este fragmento, o hay otro camino de features?
4. ¿Hay otras features fuera de las dos declaradas que el expediente no incluye? El contexto indica que no, pero no se verificó con el código completo.

## Recomendaciones

1. Retirar `recovered_kwh` de las features de scoring (H1, severidad alta). Esta decisión afecta el alcance de features y debe aprobarla el owner del modelo antes de cualquier nueva evaluación.
2. Añadir un filtro temporal explícito por `*_available_at <= prediction_at` en la construcción de features, y un test que falle si una columna con timestamp posterior entra en el conjunto.
3. Confirmar la ventana de `history_kwh_90d` con su proceso fuente (H2) antes de dar por cerrada la auditoría.
4. Repetir la auditoría con el expediente completo (código de split, fit y métricas) antes de concluir sobre performance; esta auditoría no lo cubre.
