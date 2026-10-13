---
skill: detect-leakage
version: "0.2.0"
fecha: 2026-10-11
condicion: treatment
estado: "Auditoría documental; sin leakage confirmado"
inputs:
  - path: case.md
    sha256: 072562c9846d5469c9041edf8e3fb5e23cc42d440441b8204aa40e3b9c949a96
  - path: inputs/context.md
    sha256: 5417d10f78d29b1f98792a7aed6b198a39fdd07b4693dd07446dbcf0fa87ea55
  - path: inputs/observations.csv
    sha256: 56ee9a0e4e5e5a02703509266b3df2b071ef47fc526891c53837916d338835ee
  - path: inputs/pipeline.py
    sha256: ef460cae4444fd60c18b1a6a2906c3e6850312f39fc1c3bc254c22b737ce4cda
---

## Resumen

La evidencia es compatible con un uso válido para ofertas mensuales a la cartera existente, prediciendo baja durante los siete días siguientes. No se identifica un mecanismo confirmado de leakage. Esta conclusión acotada depende del proceso declarado: no certifica producción, generalización a nuevas cuentas ni performance.

## Hallazgos

- **Entidad e identidad:** C1 y C2 aparecen en train y evaluation. La identidad puede recuperar información aprendida de cuentas conocidas, lo cual corresponde a la población declarada; el solape no demuestra contaminación. Fuente: contexto y CSV. Confianza alta sobre el escenario documental; severidad informativa. Acción: conservar la evaluación recurrente y explicitar su población; exigir otra evaluación si cambia el objetivo a altas nuevas.
- **Disponibilidad temporal:** el consumo resume los treinta días anteriores y `available_at` precede una hora a `prediction_at` en las cuatro filas. El código de cuenta existía antes de septiembre. No se observa acceso a hechos posteriores mediante estas features. Fuente: contexto y CSV. Confianza alta sobre lo suministrado; severidad informativa. Acción: preservar la reconstrucción histórica y verificar su correspondencia con la fuente operacional.
- **Preprocesamiento:** encoder y scaler se ajustan con train y transforman evaluation. No aparece ajuste con información de evaluation en este fragmento. Fuente: `pipeline.py`, función `prepare`. Confianza alta sobre el código leído; severidad informativa. Acción: mantener este orden y verificar la configuración concreta del encoder y scaler.
- **Entrenamiento y labels — No determinable en ejecución real:** los labels de train se disponibilizan el 9 de octubre de 2025; el ajuste se declara para el 20 de octubre, sin año ni timestamp completo. Bajo la interpretación de octubre de 2025, estarían disponibles al ajustar. Los outcomes de evaluation llegan el 9 de noviembre y se declaran exclusivos del backtest. No hay mecanismo documentado de uso ilegítimo, pero tampoco código de fit del modelo. Fuente: contexto, CSV y alcance de `prepare`. Confianza media; severidad media si el proceso efectivo difiere. Acción: obtener fecha completa y evidencia del fit antes de aceptar esa dependencia.

## Evidencia

Se ejecutó únicamente `.runtime/check_inputs.py` con el Python autorizado: produjo hashes SHA-256 reales y confirmó cuatro filas y siete columnas del CSV. La utility no evalúa leakage. Las comparaciones de fechas y el orden de transformación proceden de lectura documental; no se ejecutó el pipeline ni se calcularon métricas. Skill y condición corresponden al snapshot y report-context leídos.

## Preguntas abiertas

¿Cuál fue el timestamp completo del entrenamiento? ¿Qué implementaciones de encoder y scaler se usan? ¿Qué registro acredita las ventanas, disponibilidad efectiva y exclusión de outcomes de evaluation del fit y de cualquier selección de features?

## Recomendaciones

Solicitar esos registros y contrastarlos con el procedimiento declarado. Mantener las features históricas disponibles y el alcance de cartera existente. Cualquier outcome posterior debe quedar restringido a evaluación retrospectiva. No retirar identidad automáticamente ni aprobar gates a partir de esta revisión.
