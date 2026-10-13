---
skill: none
version: null
fecha: "2026-10-11T23:54:09-05:00"
condicion: baseline
estado: requiere_correccion_temporal
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

El expediente no sustenta usar payment_sum_previous_day para decidir contactos a las 08:00 en las tres observaciones suministradas. Aunque los pagos corresponden al día previo, el motor recibe la tabla después de la decisión. Esto invalida su disponibilidad histórica para ese instante; no permite cuantificar un sesgo de performance. Auditoría por inspección, sin ejecutar el pipeline ni entrenar.

## Hallazgos

**H1 — Disponibilidad posterior a la decisión.** Componente: feature payment_sum_previous_day y reconstrucción temporal del backtest. Mecanismo: utilizar retrospectivamente un valor cuyo primer acceso por scoring ocurre después de prediction_at introduce información operacionalmente futura, aun cuando los hechos subyacentes sean anteriores. Fuente: inputs/context.md define available_at como primer acceso; inputs/observations.csv muestra, para A1, A2 y A3, prediction_at=2025-11-01T08:00:00Z y available_at=2025-11-02T03:00:00Z, diferencia de 19 horas. Confianza: alta para las tres filas. Severidad: alta, porque afecta a la única feature declarada y a toda la muestra. Acción proporcional: reconstruir los valores efectivamente accesibles al decidir; si no existen, excluir esta feature de ese backtest o proponer otro instante de decisión para aceptación humana.

**H2 — Selección sin control temporal visible.** Componente: inputs/pipeline.py, función features. Mecanismo: devuelve rows[FEATURE_COLUMNS] sin comprobar available_at frente a prediction_at, por lo que el fragmento no impediría consumir las filas tardías. Fuente: declaración FEATURE_COLUMNS y retorno de features. Confianza: alta sobre el fragmento; no determinada sobre un pipeline completo, que no se suministra. Severidad: media como brecha de control observada, asociada a H1, sin contabilizarla como otra fuga confirmada. Acción proporcional: incorporar o documentar una selección temporal anterior a features que impida usar valores todavía inaccesibles, con tratamiento explícito de valores faltantes.

## Evidencia

La utility fija, ejecutada con el Python del workspace, produjo los hashes consignados y contó tres filas con seis columnas. Es una comprobación de integridad y conteo, no un detector de leakage. Las diferencias temporales anteriores provienen de inspección de timestamps UTC.

period_end=2025-10-31T23:59:00Z precede a la predicción en 8 horas y 1 minuto; describe antigüedad del hecho, no disponibilidad para scoring. El contexto declara solo payment_sum_previous_day como feature, consistente con el código. missed_next_7d queda fuera de FEATURE_COLUMNS y se declara exclusivo de evaluación retrospectiva: no hay evidencia aquí de incorporación del target a X. Exportar el 20 de noviembre con outcomes conocidos tampoco constituye, por sí solo, fuga; requiere conservar la disponibilidad histórica.

## Preguntas abiertas

¿Existe una tabla o snapshot anterior disponible a las 08:00? ¿Hay filtrado temporal aguas arriba, y cómo maneja estas filas? ¿Se conservan revisiones históricas y tiempos de acceso por variable? No se aportan split, preprocessing, entrenamiento ni protocolo de evaluación; su contaminación no puede determinarse con este expediente.

## Recomendaciones

Solicitar al responsable de datos la trazabilidad del primer acceso y snapshots utilizables. Proponer la reconstrucción por disponibilidad y documentar cualquier exclusión, sin cambiar unilateralmente el horario, población o KPI. Antes de calcular performance, resolver H1 y acreditar el control temporal completo. El informe no aprueba gates, promociones del Foundry ni acciones de negocio.
