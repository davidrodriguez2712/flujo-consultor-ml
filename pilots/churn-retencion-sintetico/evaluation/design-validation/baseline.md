# Estrategia de validación del scoring mensual de churn (piloto sintético)

**Alcance.** Es un diseño de solo lectura, basado únicamente en `context.md`, `dictionary.md` y `data-checks.json`. No ejecuté scripts, no entrené nada, no escribí archivos ni aprobé gates. Ninguna skill disponible aplicaba, así que no usé ninguna. Los datos son sintéticos. El escenario, K=50, el KPI y la definición de churn son propuestas del laboratorio, pendientes de aceptación humana, igual que la designación del reviewer. Lo que sigue condiciona a esas propuestas y no las da por aceptadas.

## 1. Hechos de partida y lo que implican

| Hecho (fuente) | Implicación |
|---|---|
| 35 990 snapshots, 2 400 clientes, 24 periodos (2024-02 a 2026-01) | Unos 15 snapshots por cliente. Hay fuerte dependencia entre filas. |
| 35 018 labels observadas y 972 pending, con 1 428 positivos (4,08 %) | Un modelo aleatorio acierta alrededor de 2 de cada 50 contactos. |
| Extracción simulada el 2026-01-15 y `label_available_at` = fin de ventana + 7 d | El snapshot de 2025-12 estaría disponible el 2026-01-08. El de 2026-01 lo estaría el 2026-02-08, o sea después de la extracción. Por eso los 972 pending corresponden con alta probabilidad al periodo 2026-01 *(inferido; verificar)*. |
| `cancellation_at` no nulo en 1 456 filas, frente a 1 428 positivos observados | Unas 28 filas pending ya traen cancelación *(inferido)*. Es un riesgo de leakage. Esas filas siguen siendo pending y nunca se etiquetan como 1. |
| El universo decrece y no hay altas después de 2024-06 | Hay deriva estructural. `tenure_months` crece con el calendario, así que el test verá tenures fuera del rango de entrenamiento. |
| Los clientes se repiten entre meses | Las particiones aleatorias por fila filtran información. |

Orden de magnitud: unas 1 500 filas observadas por mes en promedio, con 972 en el último mes. Eso da unos 60 positivos mensuales, y menos hacia el final. Por eso:

- **Recall@50:** su techo es aproximadamente 50 / positivos del mes. Si hay más de 50 positivos nunca llega a 1.
- **Varianza:** Precision@50 de un solo mes tiene error estándar de aproximadamente 3 puntos con p≈4 %, así que un mes aislado es muy ruidoso.

## 2. Reglas transversales

1. **Partición solo temporal.** Nunca K-fold aleatorio por fila.
2. **Regla de disponibilidad.** Una fila entra al entrenamiento en la fecha T solo si `label_available_at ≤ T` y `label_status` era observed en T. En la práctica, para puntuar el mes M se entrena con snapshots hasta M−2. El snapshot de M−1 todavía no tiene label, porque su label madura el día 8 de M+1. Esto se aplica con la fecha, no con el flag de extracción.
3. **Pending nunca es 0.** Se excluye de entrenamiento y de métricas. Solo se puntúa como shadow.
4. **Prohibidos como features:** `churn_next_month`, `cancellation_at`, `label_status`, `window_end_exclusive`, `label_available_at`, `extracted_at`, `is_synthetic`, `market`. `mrr_usd` es función determinista de `plan`, así que se usa uno solo de los dos.
5. **Un test solo se toca una vez.** Se congela la política (features, preprocessing, hiperparámetros, cadencia de reentrenamiento, desempates) antes de abrirlo, y se registra el acceso.

## 3. Particiones

Los periodos con label observada van de 2024-02 a 2025-12, es decir 23 meses.

| Bloque | Meses de scoring | Uso |
|---|---|---|
| **Desarrollo** | 2024-02 a 2025-05 | Entrenamiento y validación con orígenes móviles (rolling-origin), con ventana expansiva. Folds de validación de 2024-10 a 2025-05 (8 meses), con mínimo de 8 meses de historia. Cada fold entrena solo con labels disponibles a la fecha de scoring. |
| **Buffer** | 2025-06 | No se puntúa ni se mide. Evita que la selección de diseño use labels que maduran con el test ya abierto. Puede usarse como entrenamiento tras congelar. |
| **Evaluación final** | 2025-07 a 2025-12 (6 meses) | Se ejecuta una sola vez con la política congelada. El modelo se reentrena cada mes solo con labels disponibles ese día. Esto replica la operación. Se reporta también un modelo único congelado a 2025-07-01 como sensibilidad. |
| **Operacional / shadow** | 2026-01 (pending) y meses futuros | Scoring prospectivo. Se evalúa cuando madura la label. Ver sección 7. |

**Por qué estos cortes.** El test de 6 meses reúne unos 360 positivos, lo suficiente para intervalos útiles sin vaciar el desarrollo. Los meses más recientes son los más parecidos al scoring futuro. Las fechas son propuestas ajustables. Los conteos por mes no están en `data-checks.json` y deben verificarse antes de congelarlas.

## 4. Entidades repetidas

- **Split temporal con clientes compartidos.** Es el diseño correcto aquí, porque en producción se vuelve a puntuar a los mismos clientes. Pero la métrica mide "clientes ya vistos", y como no hay altas nuevas después de 2024-06, no se puede evaluar la generalización a clientes nuevos. Hay que declararlo como limitación.
- **Sensibilidad por grupos.** Se repite el test con clientes del test excluidos del entrenamiento (partición por `customer_id`). Sirve solo para cuantificar cuánto del rendimiento viene de memorizar al cliente.
- **Tuning interno.** Nada de CV aleatoria. Si se necesita CV dentro de un fold, se agrupa por `customer_id` y se respeta el orden temporal.
- **Incertidumbre.** Bootstrap por clúster de cliente, remuestreando clientes completos con todos sus meses. Reportar IC95 %.
- **Dependencia temporal.** Un churner deja de generar snapshots, así que los clientes de larga permanencia están sobrerrepresentados. Reportar el desempeño segmentado por tenure.
- **Pesos.** El agregado mensual da el mismo peso a cada mes. El agregado agrupado (pooled) da más peso a los meses grandes. Se reportan ambos.

## 5. Preprocessing y joins

**Preprocessing (ajustado solo con entrenamiento, dentro de cada fold):**
- **`active_days_prev_month`.** Tiene un 2,03 % de nulos (730 filas), que representan missing simulado y no cero. Se imputa con la mediana del entrenamiento y se añade un indicador `missing`. Se comprueba que el missing no se concentre en un periodo ni en churners.
- **`active_days_prev2_month`.** Para historias anteriores al primer snapshot es un agregado simulado, no reconstruible. Se hace una sensibilidad que excluya los primeros meses y a los clientes con menos de 2 meses de historia.
- **`plan` y `channel`.** `plan` es fijo y `channel` es el canal de alta, así que no hay fuga temporal. Se codifican con categorías ajustadas en el entrenamiento y una categoría "desconocida".
- **`tenure_months`.** Es diferencia de meses calendario, no meses completos. Se usa tal cual y se documenta la extrapolación temporal.
- **Escalado y selección de variables.** Ajustados solo en el entrenamiento.
- **`discount_active`.** Es un predictor observacional y no sirve para inferir uplift.

**Joins:**
- **Snapshots y labels.** 1:1 por `(customer_id, prediction_timestamp)`. Se verifica que el número de filas no cambia.
- **Snapshots y customers.** N:1 por `customer_id`, solo para `plan`, `channel` y `signup_date`.
- **Tickets.** Usar `support_tickets_prev_month` ya disponible, o agregar `support_tickets` por `(customer_id, snapshot_prediction_timestamp)` antes del join. Nunca ambos como suma. El join directo genera 36 853 filas frente a 35 990 snapshots, es decir un fan-out de 863. Si se usan categorías (billing/technical/account), se agregan primero.
- **Labels en el join.** Se unen solo para construir el target. Las columnas de labels distintas del target no pasan a la matriz de features.

## 6. Métricas

**Primaria, propuesta y sujeta a aceptación de K=50:**
- **Precision@50 y Recall@50 por mes**, con media mensual, valor agrupado e IC por clúster. Orden determinista con desempate fijo (por ejemplo `customer_id`).
- **Lift@50** = Precision@50 / tasa base del mes. Con un universo que se encoge, 50 contactos son el 3,3 % de ~1 500 clientes pero el 5,1 % de 972. Eso cambia la dificultad entre meses.
- **Baselines obligatorios:** aleatorio (≈4 %), una regla simple (pagos fallidos, baja actividad, tickets) y el modelo del mes anterior. Sin superar la regla simple no hay valor que demostrar.

**Secundarias:**
- PR-AUC, ROC-AUC y Brier con calibración (reliability).
- Sensibilidad de K (25, 50, 100 y un porcentaje fijo del universo).
- Rendimiento por plan, canal y tramo de tenure.

**Contexto, no beneficio:** MRR en riesgo = MRR de los churners capturados en el top-50. No es margen ni efecto incremental. Sin asignación aleatoria de retención no se puede estimar uplift ni ROI, y el reporte debe decirlo.

## 7. Evaluación operacional (scoring mensual futuro)

1. **Scoring.** Se puntúa el primer día de cada mes con features cortadas a las 23:00 UTC del día anterior. El modelo se reentrena solo con labels disponibles en esa fecha.
2. **Congelado.** El archivo de scores se guarda con hash y marca de tiempo antes de que madure la label.
3. **Evaluación diferida.** El mes M se evalúa en M+1 + 7 días, o sea unos 5 semanas después del scoring. El shadow de 2026-01 se evalúa desde el 2026-02-08.
4. **Monitoreo mientras no hay label.** Se vigilan:
   - deriva de features (PSI);
   - tasa de missing de `active_days_prev_month` (referencia ~2 %);
   - distribución de scores;
   - tamaño del universo;
   - tasa de positivos observada con retraso.
   
   Los umbrales de alerta los fija el reviewer.
5. **Bucle de retroalimentación.** Si en algún momento se contacta a clientes, sus labels posteriores quedan contaminadas por la intervención. Hay que registrar `contactado` y `grupo`. Si se quiere medir efecto, se necesita un holdout aleatorio. Es una decisión humana pendiente y este piloto no ejecuta campañas.
6. **Capacidad.** Se registra cuántos contactos reales hubo, por si difiere de 50.
7. **Gates.** El resultado se presenta como evidencia para revisión humana. Esta estrategia no aprueba ni simula la aprobación de ningún gate.

## 8. Checks

**Ya reportados como PASS estructural en `data-checks.json`** (la revisión semántica sigue pendiente):
- claves sin duplicados;
- joins 1:1 sin huérfanos;
- `features_after_prediction` = 0;
- `labels_known_at_prediction` = 0;
- `pending_zero_filled` = 0;
- `post_cutoff_labels_exposed` = 0;
- coherencia con `signup`.

**Checks adicionales que propongo implementar** (el JSON no los cubre):
- `label_available_at` = `window_end_exclusive` + 7 d, y `window_end_exclusive` = inicio del mes siguiente.
- `churn_next_month` nulo si y solo si `label_available_at > extracted_at`. Confirmar que los pending son solo 2026-01.
- Para churn=1, `cancellation_at` cae dentro de `[prediction_timestamp, window_end_exclusive)`. Para churn=0, no. Contar las ~28 filas pending con cancelación.
- Cada fila de entrenamiento cumple `label_available_at ≤ fecha de entrenamiento`. Test automático por fold.
- Ningún cliente de test tiene filas de entrenamiento de un fold posterior.
- `support_tickets_prev_month` coincide con el conteo agregado de `support_tickets`.
- `opened_at` de los tickets es anterior a `features_available_at`, no solo al scoring. El check actual compara contra `prediction_timestamp`.
- Rango de `active_days_*` acotado por días del mes y por alta.
- Sin snapshots posteriores a la cancelación.
- Tasa de missing por periodo y por clase.
- Ningún predictor entre los prohibidos de la sección 2.
- Número de filas igual antes y después de cada join.
- Registro de que el test se abrió una vez, con semilla y hash del manifest (`data/raw/manifest.json`).
- Todas las métricas excluyen pending.
- Alerta si algún mes de test tiene menos de 20 positivos.

## 9. Limitaciones y decisiones humanas pendientes

- **Datos sintéticos.** Los resultados no representan demanda ni comportamiento real.
- **Universo menguante y sin altas nuevas.** Limita la generalización y confunde tenure con tiempo.
- **Sin causalidad.** No hay base para uplift, ROI ni efecto de la campaña.
- **Un solo ciclo de 24 meses.** No hay estacionalidad plurianual.
- **Pendientes de aceptación humana:** el caso, K=50, el KPI, la definición de churn, el entregable y la designación del reviewer. Los cortes de la sección 3 y los umbrales de la sección 7 son propuestas mías y también requieren revisión.
