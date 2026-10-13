---
skill: detect-leakage
version: 0.2.1
fecha: 2026-10-13
estado: confirmado
condicion: treatment
inputs:
  - path: case.md
    sha256: 4c41de990caa164c5749c2660a47dee3daa0dbd9b91c70018b5d5e59f3bae8e2
  - path: inputs/context.md
    sha256: 620e9e3f209b9c12361deb7147b318c6d3f6f346a24805348b55a9855c6d857e
  - path: inputs/observations.csv
    sha256: 8ec83a7f81b47dc4c80ab9097443af95f7feaccdaaf87e68c6157cbc018a111b
  - path: inputs/pipeline.py
    sha256: ca6985dbac6928444de93626f8e49cc18227e0c466c8fc6705b4910309f89483
---

## Resumen

El expediente demuestra leakage temporal de disponibilidad en la única feature declarada, `payment_sum_previous_day`. Aunque sus hechos terminan antes de la decisión, su primer acceso ocurre después. Por ello, el fragmento no sustenta un backtest que reproduzca la decisión diaria de las 08:00 sobre impago durante los siguientes siete días. El target posterior es legítimo para evaluación retrospectiva.

Se aplicó la guía textual detect-leakage 0.2.1; no se verificó una invocación nativa ni el runtime de la skill.

## Hallazgos

**H1 — Confirmado.** Componente: selección de `payment_sum_previous_day`. Mecanismo: el código selecciona esa columna sin controlar disponibilidad. En A1, A2 y A3, `period_end` es 2025-10-31T23:59:00Z, anterior a `prediction_at` (2025-11-01T08:00:00Z), pero `available_at` es 2025-11-02T03:00:00Z, posterior. El contexto define explícitamente este último como primer acceso del motor. La información no estaba accesible al scoring declarado; el origen histórico de los pagos no corrige esa demora. Fuentes: `inputs/context.md`, las tres filas de `inputs/observations.csv` y `FEATURE_COLUMNS`/`features` en `inputs/pipeline.py`. Confianza: alta en el mecanismo documentado; no se inspeccionó producción. Severidad: alta, pues compromete la validez temporal de toda la entrada predictiva declarada. Acción: excluir estos valores de las decisiones correspondientes y reconstruir features disponibles al corte, o someter otro horario de decisión al owner para aprobación explícita.

## Evidencia

La utility fija ejecutada generó hashes SHA-256 y contó tres filas y siete columnas del CSV. Esos checks acreditan identidad y tamaño de las fuentes; no evalúan leakage. La comparación de timestamps y la selección de columnas proceden de lectura directa, sin ejecutar el pipeline, entrenar ni calcular performance.

El contexto identifica `account` y fechas como metadata y `missed_next_7d` como outcome retrospectivo. El fragmento selecciona únicamente la suma de pagos, por lo que no evidencia uso del target como predictor. La exportación del 20 de noviembre tampoco demuestra por sí sola contaminación: la prueba temporal es `available_at`, cuyo significado está documentado.

## Preguntas abiertas

¿Existe una fuente alternativa con pagos realmente accesibles antes de las 08:00 y linaje verificable? ¿El pipeline completo aplica un filtro de disponibilidad previo a este fragmento? Solicitar su evidencia para determinar el alcance real del problema. No están documentados entrenamiento, madurez de labels al entrenar, splits ni transformaciones aprendidas; esas familias no pueden evaluarse con este expediente.

## Recomendaciones

El owner del backtest debe exigir ventana de hechos, disponibilidad efectiva y linaje por feature, con exclusión de valores posteriores al corte. Conservar pagos históricos cuando se acredite su acceso oportuno; el outcome posterior puede seguir usándose para evaluación. Si se propone mover la decisión, documentar y aprobar el nuevo contrato antes de evaluar. La aceptación corresponde al owner; este informe no aprueba producción ni gates y no demuestra performance o ausencia universal de leakage.
