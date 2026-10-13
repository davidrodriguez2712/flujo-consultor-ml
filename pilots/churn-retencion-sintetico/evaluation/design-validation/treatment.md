# Estrategia de validación: scoring mensual de churn (piloto sintético)

**Estado:** diseño solo lectura. No escribí archivos, no entrené, no ejecuté scripts y no aprobé gates. Aplico la skill `design-validation`, pero omito su paso de persistir el reporte en `reports/validation/` porque pediste solo lectura.

**Inputs leídos:** `context.md`, `dictionary.md` y `data-checks.json`. No calculé sha256 porque no podía ejecutar nada.

**Evidencia:** todas las cifras salen de `data-checks.json` o de derivar sus reglas. Marco como *(inferido)* lo que no verifiqué sobre las filas. Las cifras por período (positivos y prevalencia por mes) son **No determinables** con lo leído.

## Resumen

- **Estrategia:**
  - Walk-forward con ventana expansiva mensual y gap de label.
  - Test final temporal aislado.
  - Evaluación operacional mensual con Precision/Recall/Lift@K.
  - Reproduce el scoring de inicio de mes sobre los mismos clientes, con solo las labels ya disponibles en esa fecha.
- **Precaución principal:** el delay de label (cierre de mes + 7 días) hace que la label del mes anterior nunca esté disponible en el momento del scoring. El train de cada fecha T solo puede llegar hasta el snapshot de T−2 meses. Además, el universo se reduce y no hay altas desde 2024-06, así que la generalización es limitada y el K=50 pesa más con el tiempo.
- **Fiabilidad:** es posible diseñar una validación fiable. Los resultados quedan condicionados a que un humano acepte el escenario, K=50, la definición de churn y el reviewer. Todos son propuestas del laboratorio pendientes de aceptación. Trato K como parámetro y 50 como valor provisional.

## Objetivo de validación

Estimar qué tan bien el modelo priorizaría cada inicio de mes a los clientes activos que cancelarán en el mes calendario siguiente. Debe usar solo información disponible a esa fecha y solo labels ya maduras en la fecha de entrenamiento. La métrica de decisión es la calidad de los 50 primeros. Esto no mide uplift ni beneficio de una campaña.

## Estructura de datos relevante

- **Unidad y entidad:** snapshot cliente×mes, con clave `(customer_id, prediction_timestamp)`.
  - 2.400 clientes y 35.990 snapshots, unos 15 por cliente.
  - Es un panel con entidades repetidas.
- **Períodos:** 24 inicios de mes, de 2024-02-01 a 2026-01-01.
- **Target:** `churn_next_month`, con 35.018 observadas, 1.428 positivos (4,08%) y 972 pendientes.
- **Labels pendientes:**
  - Extracción: 2026-01-15.
  - Disponibilidad: `window_end_exclusive + 7d`.
  - El snapshot 2025-12-01 queda disponible el 2026-01-08, así que está observado.
  - El snapshot 2026-01-01 queda disponible el 2026-02-08, así que está pendiente.
  - Las 972 pendientes son *(inferido)* ese último período completo.
  - Quedan 23 períodos evaluables, de 2024-02 a 2025-12.
- **Churn terminal:** el cliente deja de generar snapshots al cancelar. Cada cliente tiene como máximo un positivo y está en su última fila *(inferido de la definición)*. Un cliente no puede tener positivos en train y en test.
- **Deriva estructural:**
  - El universo decrece y no hay altas nuevas desde 2024-06.
  - `tenure_months` crece con el calendario, así que en test aparecerán valores que train no vio. La confusión tenure/tiempo es un riesgo real de extrapolación.
  - El número de positivos por mes probablemente baja al final *(no verificado)*.
- **Volumen:** unos 62 positivos por mes de promedio, pero quizá menos de 50 en los meses finales *(no verificado)*. Con K=50, Precision@50 tiene un techo menor que 1 en esos meses.

## Estrategia recomendada y definición de splits

### Línea temporal (T = fecha de scoring)

```
Train para scoring en T: predicciones ≤ T−2 meses (label_available_at ≤ T)
Gap: el snapshot T−1 se excluye (su label madura el día 7 de T+1... de T, tras el scoring)
```

Regla de implementación: filtrar por `label_available_at <= fecha_de_entrenamiento`. No usar `label_status`, que es relativo al corte de extracción y no a la fecha simulada.

### 1. Desarrollo (selección de modelo e hiperparámetros)

- **Datos:** predicciones de 2024-02 a 2025-05 (16 períodos).
- **Esquema:** walk-forward expansivo, con una fold por mes de validación V.
  - Train: predicciones ≤ V−2.
  - Validación: el mes V completo, con su label ya madura en la simulación.
  - Train mínimo: 6 meses (2024-02 a 2024-07).
  - Validaciones: V = 2024-09 a 2025-05, o sea 9 folds mensuales.
- **Ventana rodante de 12 meses:** solo como análisis de sensibilidad. Se justifica por la deriva y la reducción del universo, no como esquema principal.
- **Sin nested CV ni embargo adicional.** El gap ya cubre el delay de label. Los hiperparámetros se eligen en estos folds, que ya son temporales.

### 2. Evaluación final (aislada)

- **Datos:** 2025-07 a 2025-12 (6 meses). Ninguna decisión puede tocarlos: ni preprocessing, ni selección de features, ni umbrales, ni hiperparámetros.
- **Modelo congelado:** especificación y features fijadas con desarrollo.
  - Entrenar con predicciones ≤ 2025-05, cuyas labels estaban disponibles el 2025-06-08, antes del 2025-07-01.
  - El snapshot 2025-06 se excluye por label no madura al 2025-07-01.
- **Variante A (congelado):** un solo modelo puntúa los 6 meses. Mide decaimiento temporal.
- **Variante B (simulación operacional):** reentrenamiento mensual con la regla de disponibilidad, misma especificación fija. Es la más cercana a producción *(la cadencia de reentrenamiento real es una pregunta abierta)*.
- Se pre-registran ambas variantes y se ejecutan una vez.

### 3. Out-of-time

- Reportar la variante A por mes y en dos bloques, 2025-07 a 09 y 2025-10 a 12. Sirve para ver deriva de discriminación y de prevalencia, y el efecto de la extrapolación de tenure.
- El snapshot 2026-01-01 (972 pendientes) **no se evalúa**. Se puntúa como scoring prospectivo, y sus métricas solo se pueden calcular desde 2026-02-08.

### 4. Evaluación operacional

- Cada mes de validación o test, ordenar por score y tomar los K primeros (provisional K=50).
- Calcular Precision@K, Recall@K y Lift@K por mes, y el promedio y la dispersión entre meses.
- Usar un desempate determinista y registrado ante scores iguales.

## Diseño de cross-validation

- No hay CV aleatoria. Los folds son los meses del walk-forward descrito.
- **Estratificación:** no aplica. Se respeta la prevalencia natural de cada mes.
- **Gap:** de un mes, justificado solo por el label delay.
- **Número de folds:** 9, viable con 16 períodos de desarrollo.
- Una fold mensual con unos 50 positivos es ruidosa. Con ~50 contactos, Precision@50 tiene un error estándar de ~0,06 si p≈0,3. Por eso se agregan los meses y no se decide por un mes aislado.

## Manejo de entidades

- **Los mismos clientes pueden estar en train y en test.** Es válido porque el scoring mensual futuro vuelve a puntuar a los mismos clientes. No uso GroupKFold por defecto.
- **Cuidados:**
  - `customer_id` no es feature.
  - Las filas del mismo cliente están correlacionadas, así que las incertidumbres se estiman con bootstrap por bloques de cliente y por mes, no por fila.
  - Un cliente que canceló desaparece naturalmente de los períodos siguientes.
- **Diagnóstico opcional:** una evaluación disjunta por cliente solo serviría para medir memorización de rasgos estáticos como `channel`. No es el escenario de producción y no se usa para decidir.
- **Cohorte nueva:** no hay altas después de 2024-06, así que la validación no dice nada sobre clientes nuevos.

## Salvaguardas de leakage

- **Ajustar solo con el train de cada fold o fecha:**
  - Imputación de `active_days_prev_month` (missing ≈ 2,0%: 730 de 35.990).
  - Escalado, codificación de `channel`, selección de features y umbrales.
  - Resampling, si se usa.
  - Hiperparámetros.
- **Missing:** no imputar con 0. Un vacío es missing simulado, no actividad cero. Considerar un indicador de missing.
- **`active_days_prev2_month`:** antes del primer snapshot es un agregado simulado, y vale 0 si el cliente no existía. Son semánticas distintas. Revisar los primeros meses y no tratarlos como equivalentes.
- **Excluir como predictors:**
  - `churn_next_month`, `cancellation_at`, `label_status`.
  - `window_end_exclusive`, `label_available_at`, `extracted_at`.
  - `is_synthetic` y `market` (constantes).
  - `customer_id` y las fechas crudas.
  - `mrr_usd` es función directa de `plan`: redundante, no leakage.
- **Joins:**
  - Snapshots y labels: 1:1 por `(customer_id, prediction_timestamp)`. No unir solo por `customer_id`.
  - Snapshots y customers: N:1 por `customer_id`.
  - Snapshots y tickets: **agregar tickets antes del join**. El join directo produjo 36.853 filas frente a 35.990 snapshots (fan-out). Verificar tras el join que quedan 35.990 filas y que la clave es única.
  - Usar el conteo ya disponible `support_tickets_prev_month` **o** el agregado de tickets, nunca ambos sumados.
- **Orden:** apartar el test final (≥2025-07) antes de cualquier análisis exploratorio guiado por el target. La auditoría de un pipeline concreto corresponde a `detect-leakage`.

## Métricas

- **Selección de modelo:** Precision@K promedio entre los 9 folds, porque la decisión es priorizar los K primeros. Como es ruidosa, la acompaño con PR-AUC y Lift@K como estabilizadores. Elegir un modelo más complejo solo si la mejora supera el intervalo por bloques.
- **Globales:** PR-AUC (principal, con 4% de prevalencia), ROC-AUC y log-loss/Brier con curva de calibración.
- **Ranking:** Precision@K, Recall@K y Lift@K por mes. Usar K=25, 50 y 100, y K como % de la población activa, porque el universo decrece y 50 pesa cada vez más. Normalizar por el techo `min(1, positivos/K)` cuando los positivos del mes sean menos que K.
- **Baselines:** azar (prevalencia) y una regla simple, por ejemplo menor actividad o pagos fallidos, para que el Lift tenga referencia.
- **Contexto de negocio:** MRR de los positivos capturados en el top-K frente al total. Es MRR en riesgo, no beneficio incremental ni recuperación esperada.
- **Límite:** medir quién cancela no mide a quién se puede retener. `discount_active` no es una asignación aleatoria, así que no se puede estimar uplift.

## Riesgos, alternativas descartadas y preguntas abiertas

### Riesgos

- Pocos positivos por mes y por fold, y probablemente menos al final. Las métricas mensuales serán ruidosas.
- Deriva y encogimiento del universo. Confusión tenure/calendario y extrapolación en test.
- Test de 6 meses con pocos positivos: intervalos amplios. El resultado final es una estimación, no una garantía.
- Datos sintéticos: la evaluación valida el método, no el comportamiento comercial real.
- La validación previa a producción no es monitoreo. Este último queda fuera de alcance.

### Alternativas descartadas

- **Split aleatorio o estratificado por fila:** no reproduce el scoring futuro, ignora el label delay y no mide deriva.
- **GroupKFold / split por cliente:** el escenario real re-puntúa a los mismos clientes. Responde a otra pregunta, la de clientes nuevos.
- **K-fold estándar:** mezcla pasado y futuro.
- **Entrenar con la label T−1:** no está disponible en T. Es leakage por delay.
- **Nested CV, purging y embargo adicional:** sin razón concreta. El walk-forward ya separa por tiempo y el gap cubre el delay.
- **Rolling como esquema principal:** reduce el entrenamiento sin evidencia previa de que ayude. Queda como sensibilidad.
- **Usar `label_status` como filtro de entrenamiento o rellenar pendientes con 0:** incorrecto. Pending ≠ 0.

### Preguntas abiertas (pendientes de revisión humana)

1. Aceptar o ajustar el caso, K=50, la definición de churn (cancelación en el mes calendario siguiente) y el entregable. Designar reviewer.
2. Cadencia real de reentrenamiento y fecha efectiva de entrenamiento respecto al scoring. Esto define el gap exacto.
3. Si K debería ser fijo (50) o un porcentaje de la población activa.
4. Si la deriva por la caída del universo es aceptable o si debería acotarse el alcance.

### Checks pendientes de ejecutar (por quien tenga permiso)

- Positivos, filas y prevalencia por mes y por partición.
- Aserción de que todo train cumple `label_available_at <= fecha_de_entrenamiento`.
- Ninguna fila de test usada en ajustes.
- Confirmar que las 972 pendientes son solo el período 2026-01.
- Distribución de `tenure_months` entre train y test.
- Fan-out cero tras agregar tickets.

### Checks ya cubiertos por `data-checks.json`

- Claves únicas y sin huérfanos.
- Features con `features_available_at` anterior al scoring.
- Cero labels conocidas al scoring.
- Cero pendientes rellenadas con 0.
- Cero tickets posteriores al scoring.
- Cero actividad previa al alta.
- El resultado es "PASS estructural; revisión humana y semántica pendientes", sin aprobación de gates.
