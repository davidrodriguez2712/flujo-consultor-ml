---
skill: detect-leakage
version: 0.1.0
fecha: 2026-10-11
proyecto: (sin especificar)
inputs:
  - case.md — sha256:71613379fe4387f19de862020de6bcdedec00623aeb452bbdff9491690b61d39
  - inputs/context.md — sha256:2d20272658305e9620515452c404e52d7b2015db0d0a30412287c4aa02a0c1b0
  - inputs/observations.csv — sha256:cbcae4e4f891739ea487feda3f7e1eac58cf9fbe3303b774b5563770f7127462 (6 filas, 7 columnas)
  - inputs/pipeline.py — sha256:8fc757e4a3209efdedd3e1b8de6f0b77109557fb6335ac263cd3cea9b3788011
estado: sin leakage confirmado en la muestra y el código declarado; riesgos menores y preguntas abiertas; no es validación del código de producción
---

## Resumen

- **Evidencia de leakage confirmado: no.** Con los inputs autorizados no se observa información posterior a `prediction_at` en las features, ni solape temporal entre particiones, ni ajuste de transformaciones con datos de evaluación.
- Familias revisadas: preprocessing (aplicable, sin hallazgo), train-test contamination temporal (sin hallazgo), contaminación por entidad (dependencia esperada por el escenario), target/post-event/temporal sobre `usage_previous_30d` (sin mecanismo de leakage con los datos disponibles). Resampling, target encoding, joins y cross-validation no aplican: no aparecen en los inputs.
- ¿Es viable una estrategia de validación fiable? **Parcialmente.** El split temporal declarado es coherente en la muestra, pero la muestra tiene 6 filas y no permite estimar métricas ni señal univariante.

## Hallazgos

**Crítico:** ninguno.
**Alto:** ninguno.

**Medio:** ninguno confirmado.

**Bajo**

1. *Componente:* validación / entidad (`observations.csv`).
   *Familia:* entity leakage / train-test contamination por entidad.
   *Mecanismo:* `C01`, `C02` y `C03` aparecen en `train` y en `evaluation`. Esto no es contaminación si el modelo no usa identidad ni features por cliente; el `context.md` declara que producción vuelve a puntuar clientes conocidos. El riesgo es que la evaluación mida memorización de cliente y no generalización.
   *Evidencia:* solape de `customer_id` = {C01, C02, C03}; `customer_id` declarado como metadata, no feature.
   *Confianza:* Confirmado el solape; No determinable si afecta a métricas.
   *Impacto:* métricas de evaluación potencialmente optimistas si se incorporan identificadores o features agregadas por cliente.
   *Prueba:* confirmar que ningún input del modelo depende de `customer_id` y, si se usan features por cliente, comprobar su ventana.
   *Acción:* documentar el escenario de entidades conocidas; si se requiere generalización a clientes nuevos, añadir una evaluación separada por grupos.

**Informativo**

2. *Componente:* preprocessing (`pipeline.py`, líneas 3–7).
   *Familia:* preprocessing leakage (revisado, sin hallazgo).
   *Mecanismo:* `scaler.fit_transform` se aplica solo sobre `train`; `evaluation` usa `transform`. No hay ajuste con filas de evaluación.
   *Evidencia:* lectura del código declarado. Limitación: el `scaler` se recibe como argumento; no se verifica si se reutiliza un objeto ajustado previamente.
   *Confianza:* Confirmado para el código mostrado.
   *Acción:* mantener el ajuste dentro del flujo de train, y verificar en el código de producción que el scaler no se ajusta en scoring.

3. *Componente:* `usage_previous_30d` (features).
   *Familia:* temporal / post-event (revisado, sin leakage observado).
   *Mecanismo:* la feature cubre 30 días previos y `feature_available_at` está antes de `prediction_at` en las 6 filas (23:00 del día anterior). Esto es dependencia temporal válida (historia pasada), no leakage.
   *Confianza:* Probable como ausencia de leakage; el `context.md` afirma su construcción, pero no hay código de generación de la feature.
   *Nota:* el `context.md` indica señal predictiva "alta" sin AUC ni resultados; no se afirma poder predictivo ni se sospecha leakage por ello (falso positivo evitado).

## Evidencia

- **Orden temporal de features:** `feature_available_at` < `prediction_at` en 6/6 filas (train: 2025-04-30T23:00 < 2025-05-01T00:00; evaluation: 2025-06-01T23:00 < 2025-06-02T00:00).
- **Disponibilidad del target en entrenamiento:** `label_available_at` de train = 2025-05-09T00:00Z, anterior al instante de entrenamiento 2025-06-01T00:00Z (en `context.md`). Cumple.
- **Solape temporal entre particiones:** `max(prediction_at, train)` = 2025-05-01 < `min(prediction_at, evaluation)` = 2025-06-02. Sin solape.
- **Labels de evaluación:** `label_available_at` = 2025-06-10 (posterior a la puntuación); `context.md` las restringe a evaluación retrospectiva. Cumple.
- **Solape de entidades:** {C01, C02, C03} en ambas particiones (ver hallazgo 1).
- **Relación feature-target:** no determinista. Train: (4→1), (28→0), (8→1); evaluation: (6→1), (31→0), (12→0). Ningún mapeo 1:1 ni igualdad. Sin AUC univariante: 6 filas no permiten estimarla con significación.
- **Orden de operaciones (`pipeline.py`):** `fit_transform` sobre train; `transform` sobre evaluation. Sin resampling, target encoding ni selección de features.
- **Cardinalidad de joins:** no aplica; no hay joins en los inputs.
- **Check determinista de inputs** (`check_inputs.py`): hashes y conteos listados arriba; no ejecuta pipeline ni evalúa leakage.

## Preguntas abiertas

1. ¿El modelo de producción usa `customer_id` o features agregadas por cliente? (Determina si el solape de entidades es contaminación o dependencia esperada.)
2. ¿Quién genera `usage_previous_30d` y en qué pipeline? ¿Se verifica que su ventana termina en `feature_available_at`?
3. ¿Cuál es la definición exacta del evento "cancelación en 7 días" y de `prediction_at`? (Confirmar que la ventana de 7 días empieza en `prediction_at`.)
4. ¿El código real de producción coincide con `pipeline.py`? La muestra no acredita el código desplegado.
5. ¿Se dispone de un tamaño de muestra suficiente para medir la señal univariante y las métricas?

## Recomendaciones

- No eliminar `usage_previous_30d`: no hay mecanismo de leakage con los datos disponibles.
- Mantener el ajuste de transformaciones solo sobre train, y verificar en el código real que no se reajusta en scoring.
- Separar en la evaluación el escenario de clientes conocidos (acorde a producción) del de clientes nuevos, si se quiere medir generalización.
- Antes de confiar en métricas, responder las preguntas abiertas 1–4 y ejecutar la auditoría sobre el dataset completo, no sobre 6 filas.

## Límites de la inspección

- Solo se leyeron los inputs autorizados (6 filas de `observations.csv`). El código se inspeccionó, no se ejecutó. No se entrenó ningún modelo, no se usó red, y no se consultó el código de producción.
- Las afirmaciones sobre el momento de generación de features y labels proceden de `context.md`, no de verificación independiente.
- Herramientas usadas: skill `acos-eval:detect-leakage` (cargada), lectura de archivos autorizados y la utilidad `check_inputs.py`. No se han ejecutado los checks deterministas de solape sobre un dataset completo.
