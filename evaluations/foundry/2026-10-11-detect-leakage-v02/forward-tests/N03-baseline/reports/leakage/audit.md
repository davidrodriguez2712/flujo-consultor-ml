---
skill: none
version: null
fecha: 2026-10-12
inputs:
  - path: case.md
    sha256: e1d12b31dde7a50dcea6ebaa6b85b70ad122d08ee1a89114e350c57282462d71
  - path: inputs/context.md
    sha256: deb9571ae9f2845e216a625a6a29c60d97711c729593a501bda547023494b9b0
  - path: inputs/observations.csv
    sha256: 8b76235137652929a91a69070534ededf5cc8fcabb7aced2d93acb69d1108f16
  - path: inputs/pipeline.py
    sha256: 1d13b0673a0a08cdc98f85641555dacbbd5062fb94a2632c01980e236f78f3ec
estado: uso_de_informacion_no_valido_en_backtest_declarado
condicion: baseline
---

## Resumen

El orden de preparación declarado incorpora información de evaluación al ajustar el scaler. Por ello, el expediente no sustenta un backtest que reproduzca el entrenamiento del 1 de octubre y la puntuación posterior de solicitudes nuevas. El importe está disponible al recibir cada solicitud, pero los importes de noviembre no estaban disponibles para ajustar parámetros en octubre. No se calculó performance ni se ejecutó el pipeline.

## Hallazgos

**H1. Contaminación del preprocesamiento por evaluación.** Componente: scaler de `amount`. Mecanismo: `fit_transform` recibe todas las filas antes de separar particiones; aprende media y desviación incluyendo R3 y R4, de noviembre. Esos parámetros se aplican también a train. La población futura modifica así la representación usada para entrenar, y la evaluación deja de ser independiente del ajuste. Fuente: `inputs/pipeline.py`, función `prepare`; `inputs/context.md`; filas R1–R4 de `inputs/observations.csv`. Confianza: alta para el orden mostrado y declarado. Severidad: alta para la validez del backtest; no se puede cuantificar su efecto sobre métricas. Acción proporcional: separar primero las particiones, ajustar el scaler exclusivamente con train y transformar evaluación con parámetros congelados; volver a preparar el backtest antes de interpretar resultados.

## Evidencia

- `inputs/context.md` declara entrenamiento el 1 de octubre, nuevas solicitudes de noviembre, importe disponible al recibirlas y labels de train maduros antes del entrenamiento. Esta última afirmación es contextual: el CSV no aporta fechas de maduración para comprobarla independientemente.
- `inputs/observations.csv` contiene R1 y R2 en train, fechadas en agosto, con importes 100 y 200; R3 y R4 en evaluación, fechadas en noviembre, con importes 9000 y 12000. No se dedujeron parámetros numéricos del scaler.
- `inputs/pipeline.py` ajusta sobre `data[["amount"]]` y después selecciona train y evaluación. El target no aparece entre las columnas del ajuste mostrado. La presencia de targets de evaluación en el CSV, por sí sola, no demuestra que sean usados como predictores.
- La utility fija `.runtime/check_inputs.py`, ejecutada con el Python del entorno del workspace, devolvió hashes, tamaños, cinco columnas y cuatro filas del CSV. Estos resultados identifican las fuentes; la utility no diagnostica leakage. El análisis del mecanismo proviene de lectura del código y contexto.

## Preguntas abiertas

¿Qué modelo consume los datos normalizados y cómo afectan sus parámetros al resultado? ¿Existen registros de disponibilidad y maduración de labels que corroboren el contexto? El fragmento no permite auditar otros pasos, rendimiento ni magnitud del sesgo. Estas limitaciones no eliminan H1.

## Recomendaciones

Preparar train antes de ajustar cualquier transformación aprendida; conservar el scaler ajustado y utilizar únicamente su transformación para solicitudes posteriores. Documentar corte temporal y maduración de labels con evidencia verificable. Solicitar revisión humana del backtest corregido antes de usar sus resultados para decisiones. Esta auditoría no aprueba gates ni decisiones del Foundry.
