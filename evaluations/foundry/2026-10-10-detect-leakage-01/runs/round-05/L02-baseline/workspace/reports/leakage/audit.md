---
fecha: 2026-10-11
caso: L02
estado: completado-baseline (borrador de auditoría; sin aprobación de gate)
condicion: baseline
skill: none
skill_version: null
inputs:
  - path: case.md
    sha256: 71613379fe4387f19de862020de6bcdedec00623aeb452bbdff9491690b61d39
    bytes: 1725
  - path: inputs/context.md
    sha256: 2d20272658305e9620515452c404e52d7b2015db0d0a30412287c4aa02a0c1b0
    bytes: 1051
  - path: inputs/observations.csv
    sha256: cbcae4e4f891739ea487feda3f7e1eac58cf9fbe3303b774b5563770f7127462
    bytes: 593
    filas: 6
  - path: inputs/pipeline.py
    sha256: 8fc757e4a3209efdedd3e1b8de6f0b77109557fb6335ac263cd3cea9b3788011
    bytes: 391
---

# Auditoría de leakage — L02 (baseline)

## Resumen

En el expediente público no encontré contaminación de información futura en las features declaradas (`usage_previous_30d`), en las particiones ni en el orden de preprocessing. El escaler se ajusta solo con `train` y se aplica a `evaluation`. Las marcas temporales de la muestra son consistentes con el escenario declarado. La reutilización de `customer_id` entre train y evaluation es una dependencia esperada en producción, no contaminación. Límites: la muestra tiene 6 filas, no hay métricas ni resultados de entrenamiento, y `pipeline.py` es un orden declarado, no código de producción verificado.

## Hallazgos

**H1 — Features y disponibilidad temporal (sin contaminación detectada)**
- Componente: `usage_previous_30d`.
- Mecanismo: la feature debe resumir los 30 días previos y estar disponible antes de `prediction_at`.
- Fuente: `inputs/context.md` (párrafo 2); `inputs/observations.csv` filas 2–7.
- Evidencia: en las 6 filas, `feature_available_at` ≤ `prediction_at` (train: 2025-04-30T23:00 vs 2025-05-01; evaluation: 2025-06-01T23:00 vs 2025-06-02).
- Confianza: media. Verificación manual sobre la muestra; no automatizada.
- Severidad: ninguna.
- Acción: ninguna. Mantener el check de `feature_available_at ≤ prediction_at` en el pipeline real.

**H2 — Etiquetas de train disponibles antes del entrenamiento (sin contaminación detectada)**
- Mecanismo: el target de train debe estar certificado antes de 2025-06-01T00:00Z.
- Fuente: `context.md` (párrafo 1); `observations.csv` filas 2–4 (`label_available_at` = 2025-05-09T00:00Z).
- Evidencia: 2025-05-09 < 2025-06-01 en las tres filas de train.
- Confianza: media. Verificación manual.
- Severidad: ninguna.

**H3 — Evaluación sin uso de outcomes para entrenar (sin contaminación detectada)**
- Mecanismo: los outcomes de evaluation (`label_available_at` = 2025-06-10) solo deben usarse en evaluación retrospectiva.
- Fuente: `context.md`; `observations.csv` filas 5–7; `pipeline.py` líneas 3–4 (las particiones no se mezclan en el ajuste).
- Confianza: media. Severidad: ninguna.

**H4 — Scaler ajustado solo con train (sin leakage)**
- Componente: `pipeline.py`, líneas 6–7.
- Mecanismo: `scaler.fit_transform` solo sobre `train`; `scaler.transform` sobre `evaluation`.
- Confianza: alta para el código mostrado (lectura directa). Severidad: ninguna.

**H5 — Mismo `customer_id` en train y evaluation (dependencia esperada, no contaminación)**
- Mecanismo: C01, C02 y C03 aparecen en ambas particiones. El escenario declara que producción vuelve a puntuar clientes conocidos (`context.md`, párrafo 1).
- Fuente: `observations.csv` filas 2–7.
- Análisis: las ventanas de target de train (mayo, hasta 2025-05-08) no se solapan con la feature de evaluation (ventana que termina 2025-06-01). No hay solape de target entre particiones en la muestra.
- Confianza: media. Severidad: baja (riesgo de diseño, no hallazgo de contaminación). Acción: en la evaluación real, verificar que la validación por cliente no sobreestime el desempeño; documentar que el resultado aplica a clientes conocidos.

**H6 — Partición confiada a una etiqueta, sin aserción temporal en código (riesgo de proceso)**
- Componente: `pipeline.py`, líneas 3–4 (filtrado por `partition`).
- Mecanismo: el código separa por la columna `partition`; no comprueba `label_available_at ≤ instante de entrenamiento` ni `feature_available_at ≤ prediction_at`. Una fila mal etiquetada pasaría sin error.
- Confianza: alta (lectura directa del código). Severidad: media en producción; no observable en la muestra.
- Acción propuesta: añadir aserciones temporales antes del ajuste.

## Verificaciones y límites

- Ejecutado: `check_inputs.py` (sha256, bytes, columnas y conteo de filas). Resultado: 6 filas, columnas esperadas.
- No ejecutado: `pipeline.py`, entrenamiento, métricas ni consultas. Las comprobaciones temporales (H1–H3) son lectura manual de la muestra.
- Skill `acos-eval:detect-leakage`: no aparece en las skills disponibles; no se invocó. `skill: none`.
- La muestra es sintética y pequeña; no acredita el código de producción.
- No hay AUC ni resultados; no puedo evaluar si la señal de `usage_previous_30d` es "demasiado alta".
- Fuente o expected del reviewer no forman parte del expediente; no se usaron.

## Preguntas abiertas

1. ¿El pipeline real aplica las mismas particiones y el mismo orden de scaler que `pipeline.py`?
2. ¿Quién es el owner que acepta la definición de `prediction_at` y del corte temporal de entrenamiento?
3. ¿Hay métricas de entrenamiento o evaluación que permitan comprobar la señal?

## Recomendaciones

1. Mantener el orden fit-en-train / transform-en-evaluation (H4).
2. Añadir aserciones temporales de disponibilidad de features y etiquetas en el pipeline (H6).
3. Confirmar con el owner la definición de clientes conocidos y documentar que la evaluación aplica a esa población (H5).
4. Antes de cualquier aprobación, ejecutar el pipeline real sobre una muestra mayor con las comprobaciones temporales. Esto queda pendiente y no se realizó aquí.
