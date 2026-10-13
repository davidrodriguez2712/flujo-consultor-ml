---
skill: detect-leakage
version: "0.2.2"
fecha: 2026-10-13
condicion: treatment
estado: sin_leakage_identificado_en_expediente
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

No se identifica un mecanismo de leakage en el expediente. La evaluación corresponde a ofertas mensuales sobre cuentas existentes y predice bajas durante los siete días siguientes. Esta conclusión se limita a la muestra y al proceso declarado; no certifica producción ni generalización. Se aplicó la guía textual 0.2.2, sin verificación de Skill/plugin nativo.

## Hallazgos

- **Entidad e identidad:** C1 y C2 reaparecen entre train y evaluation. Para la cartera conocida, usar su código preexistente es coherente con el scoring declarado; el solape no demuestra contaminación. Fuente: context.md y observations.csv. Confianza alta sobre el alcance documentado; severidad de leakage no aplicable al no demostrarse un mecanismo. Acción: mantener explícita la población y evaluar cuentas nuevas por separado si se amplía el objetivo.
- **Temporalidad y target:** el consumo resume los 30 días previos y su disponibilidad antecede a cada predicción. Los labels de train están disponibles el 9 de octubre, antes del ajuste declarado el 20 de octubre; los outcomes de evaluation posteriores sirven al backtest y se excluyen del fit. Fuente: context.md y observations.csv. Confianza alta sobre lo documentado, limitada para ejecución real. No se identifica impacto por leakage. Acción: corroborar estos cortes y la exclusión de outcomes mediante linaje y registros de producción.
- **Preprocessing y encoding:** encoder y scaler se ajustan exclusivamente con train; evaluation recibe transform. No aparece aprendizaje de transformaciones sobre evaluation. Fuente: pipeline.py, inspección estática. Confianza alta en el orden escrito; severidad no aplicable para ese orden. Acción: conservarlo y corroborar que el proceso ejecutado coincide.

## Evidencia

La utilidad fija autorizada se ejecutó y devolvió hashes SHA-256 y cuatro filas para observations.csv. Por lectura, las decisiones son del 1 de octubre y 1 de noviembre de 2025; available_at corresponde al día anterior en ambos cortes. client_code existe desde un alta anterior a septiembre. El código separa particiones antes de ajustar transformaciones y no incorpora target entre las features devueltas.

No se ejecutó el pipeline ni se entrenó o calculó performance. La utilidad comprueba integridad y conteos, no leakage.

## Preguntas abiertas

¿Qué registros de ejecución y linaje corroboran en producción las disponibilidades, el ajuste del 20 de octubre y la exclusión de outcomes de evaluation? ¿Qué implementaciones concretas de encoder y scaler se utilizan? El expediente aporta el orden, pero no sus internals ni el entrenamiento completo.

## Recomendaciones

Conservar el diseño declarado para el backtest de cartera existente y obtener las corroboraciones anteriores antes de extender esta conclusión a producción. No retirar client_code únicamente por recurrencia. La aceptación del backtest y cualquier uso operativo corresponden al owner; este informe no aprueba decisiones de negocio.
