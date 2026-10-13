---
skill: detect-leakage
version: 0.1.0
fecha: 2026-10-11
proyecto: (sin especificar)
inputs:
  - case.md — sha256:89f1c1a622a64a73dafb5b641d871d372e72a1076533a23378ec2446f11e1e14
  - inputs/context.md — sha256:3e3db7db6249d33479a7e01fdcaee3f8f8fec3f898f7c863e2d252398e613552
  - inputs/observations.csv (4 filas, 7 columnas) — sha256:29e4badcbbcbf9e242bde9f2d31b80d1f55091a52d094b658e6992a457ad0f19
  - inputs/pipeline.py — sha256:fb122bed11f58973887818405e1b992b1589a72f8faf0ea13daf98ddb2f3da63
estado: Leakage post-evento confirmado en recovered_kwh; history_kwh_90d sin leakage observado; split, fit y validación no auditables con el expediente.
---

# Auditoría de leakage — L01 (datos sintéticos)

## Resumen

- Sí hay evidencia de **post-event leakage** en `recovered_kwh`, incluida en `FEATURE_COLUMNS` de `pipeline.py`. Su valor se determina en la inspección y queda disponible entre 2025-06-09 y 2025-06-12, después del `prediction_at` (2025-06-01T00:00:00Z).
- Componentes afectados: conjunto de features (`pipeline.py`). `history_kwh_90d` no presenta leakage con los datos disponibles.
- Familias de temporal, de entidad y de join no muestran incidencias con el expediente; las de split, CV, preprocesado, target encoding y resampling no son auditables porque el expediente no las contiene.
- Con la información disponible no se puede definir una estrategia de validación fiable: las métricas de cualquier modelo que use `recovered_kwh` estarían contaminadas por información posterior al scoring.

## Hallazgos

### Crítico

**H1 — Post-event leakage en `recovered_kwh`**
- Componente: `inputs/pipeline.py`, `FEATURE_COLUMNS` y `build_features`; columna `recovered_kwh` de `observations.csv`.
- Familia: post-event leakage (con componente de target-proxy: su valor distinto de cero coincide con el target en la muestra).
- Mecanismo: según `context.md`, `recovered_kwh` se determina al procesar la inspección y no existe para el sistema hasta `recovered_available_at`. Ese instante es posterior a `prediction_at` en las 4 filas, por lo que el modelo usaría un resultado de la inspección que aún no ocurre en el momento de decidir.
- Evidencia: `prediction_at` = 2025-06-01T00:00:00Z en todas las filas; `recovered_available_at` = 2025-06-09T12:00Z (S01), 2025-06-10T12:00Z (S02), 2025-06-11T12:00Z (S03), 2025-06-12T12:00Z (S04). Diferencia de 8,5 a 11,5 días después del scoring. Además, `recovered_kwh > 0` coincide con `fraud_confirmed = 1` en 4/4 filas (S01, S03 frente a S02, S04): indicio univariante, no prueba, dado el tamaño muestral.
- Confianza: **Confirmado** (ventana temporal incumplida según el contexto y los timestamps del CSV).
- Impacto potencial: métricas artificialmente altas y modelo que no generaliza a scoring real, porque en producción `recovered_kwh` no existiría en el momento de priorizar.
- Prueba para confirmar: verificar que el conjunto de features usado en el entrenamiento real no incluye `recovered_kwh` (o que se construye solo con `recovered_available_at <= prediction_at`, lo que aquí no es posible por ser post-evento intrínseco).
- Acción recomendada: retirar `recovered_kwh` del conjunto de features de scoring. Por ser intrínsecamente post-evento no cabe reconstruirlo con una ventana válida. La decisión de exclusión corresponde al owner del proceso.

### Informativo

**H2 — `history_kwh_90d`: dependencia temporal válida, sin leakage observado**
- Componente: `history_kwh_90d` en `observations.csv`.
- Familia evaluada: temporal (y entity).
- Mecanismo: la ventana usa historia anterior al scoring. `history_available_at` = 2025-05-31T23:00Z, una hora antes de `prediction_at` en las 4 filas (`context.md` confirma que usa días anteriores al scoring).
- Confianza: **Confirmado** como ausencia de leakage en este expediente. No es leakage temporal: es historia pasada legítima.
- Acción: ninguna sobre la feature. Conservar la comprobación de `history_available_at <= prediction_at` en el pipeline real.

## Evidencia

Checks deterministas ejecutados (lectura de CSV y comparación de timestamps; sin ejecutar `pipeline.py`):
- Conteo: 4 filas, 7 columnas; 4 `supply_id` distintos (sin entidades repetidas, por lo que no hay solape de entidades que comprobar).
- Ventana de la feature histórica: `history_available_at < prediction_at` en 4/4 filas (cumple).
- Disponibilidad de `recovered_kwh`: `recovered_available_at > prediction_at` en 4/4 filas (incumple).
- Relación feature-target: `recovered_kwh > 0` ⇔ `fraud_confirmed = 1` en 4/4 filas. Señal fuerte pero con muestra mínima; no constituye prueba de leakage por sí sola, el mecanismo es el temporal.
- Target no incluido en `FEATURE_COLUMNS`: `fraud_confirmed` no aparece como feature.
- Hashes: registrados en el frontmatter con la utilidad permitida `check_inputs.py`.

## Preguntas abiertas

- ¿El entrenamiento real usa `recovered_kwh` o solo el fragmento de `pipeline.py`? (determina si H1 afecta a métricas ya reportadas).
- ¿Existen otras features fuera de `FEATURE_COLUMNS` que el pipeline real incorpore? El contexto declara que estas dos son todas las auditadas.
- Confirmación del owner de negocio de que el momento de disponibilidad de `recovered_kwh` es el indicado en el CSV.
- Las familias de split temporal, cross-validation, preprocesado (`fit`), target encoding, resampling, agregaciones y joins no tienen artefacto en el expediente: **No determinable**.

## Recomendaciones

1. Excluir `recovered_kwh` del conjunto de features de scoring antes de cualquier evaluación posterior; reportar métricas previas que la incluyan como no válidas para decisión.
2. Mantener `history_kwh_90d` con control explícito de corte (`history_available_at <= prediction_at`).
3. Para auditar las partes ausentes, aportar el código de split, validación, preprocesado y cualquier join del pipeline real.
4. Con solo 4 filas sintéticas, ninguna métrica es interpretable; la auditoría no evalúa rendimiento.

## Límites de inspección

- Solo se leyeron los inputs autorizados; no se ejecutó `pipeline.py`, no se entrenó ni se calcularon métricas.
- El juicio sobre disponibilidad se basa en `context.md` y en los timestamps del CSV; no se verificó con el proceso de negocio.
- Muestra de 4 filas sintéticas: los indicios univariantes no tienen validez estadística.
