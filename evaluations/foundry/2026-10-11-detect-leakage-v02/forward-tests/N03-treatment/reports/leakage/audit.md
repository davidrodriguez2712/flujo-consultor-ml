---
skill: detect-leakage
version: "0.2.0"
fecha: 2026-10-12
estado: Confirmado
condicion: treatment
inputs:
  - path: case.md
    sha256: e1d12b31dde7a50dcea6ebaa6b85b70ad122d08ee1a89114e350c57282462d71
  - path: inputs/context.md
    sha256: deb9571ae9f2845e216a625a6a29c60d97711c729593a501bda547023494b9b0
  - path: inputs/observations.csv
    sha256: 8b76235137652929a91a69070534ededf5cc8fcabb7aced2d93acb69d1108f16
  - path: inputs/pipeline.py
    sha256: 1d13b0673a0a08cdc98f85641555dacbbd5062fb94a2632c01980e236f78f3ec
---

## Resumen

El expediente confirma leakage de preprocessing en el backtest declarado: el scaler aprende de solicitudes de evaluación futuras antes de separar particiones. Sus parámetros incorporan información que no estaba disponible al entrenar el 1 de octubre. No se calculó performance ni se ejecutó el pipeline; el impacto sobre métricas queda sin determinar.

Contrato aplicado: archivo Markdown nuevo en `reports/leakage/audit.md`, máximo 700 palabras; frontmatter con skill, versión, fecha real, inputs/hashes, estado y condición; cinco secciones requeridas y resumen final de máximo 80 palabras.

## Hallazgos

**Confirmado — componente: ajuste del scaler.** Mecanismo: `fit_transform(data[["amount"]])` se aplica a todo el conjunto antes de seleccionar train/evaluation. El scaler aprende media y desviación incluyendo R3 y R4, solicitudes de noviembre; esos parámetros también normalizan R1 y R2, destinadas al entrenamiento de octubre. Esto contamina el preprocessing con la distribución futura de evaluación aunque no use el target. Fuentes: `inputs/pipeline.py`, función `prepare`; `inputs/context.md`, definición del scaler y orden aplicado; `inputs/observations.csv`, particiones y fechas. Confianza: alta respecto del procedimiento declarado. Severidad: alta para la validez del backtest; magnitud estadística desconocida. Acción: dividir primero, ajustar exclusivamente con train disponible al corte y aplicar `transform` a evaluación con parámetros congelados; reconstruir el backtest antes de interpretar sus métricas.

## Evidencia

La unidad es una solicitud. Se declara entrenamiento el 1 de octubre y scoring de nuevas solicitudes en noviembre; el CSV sitúa train en agosto de 2025 y evaluación en noviembre de 2025. El año del entrenamiento no está escrito explícitamente en el contexto. El importe está disponible al recibir cada solicitud, pero los importes de solicitudes futuras no están disponibles al corte de entrenamiento.

El target es mora a 30 días. El contexto declara labels de train maduros antes del 1 de octubre; los outcomes posteriores de evaluación pueden utilizarse retrospectivamente. No hay evidencia de que el target entre al scaler. Tampoco hay joins ni encoding declarados.

Check ejecutado: utility fija `.runtime/check_inputs.py` mediante el Python autorizado; produjo los SHA-256 consignados y contó cuatro filas en el CSV. Esta utility no evalúa leakage. El mecanismo se estableció por lectura del código y contexto; no se ejecutaron transformaciones ni entrenamiento.

## Preguntas abiertas

Confirmar el año y corte exacto del entrenamiento, conservar evidencia de disponibilidad de labels y aportar el artefacto del scaler ajustado solo con train. No hay métricas ni ejecución corregida para estimar cuánto altera este error el resultado. La revisión no certifica producción ni ausencia universal de leakage.

## Recomendaciones

Preparar train y evaluación por separado, ejecutar `fit` sobre train y `transform` sobre ambas particiones. Si posteriormente se usa validación cruzada, ajustar el scaler dentro de cada fold de entrenamiento. Registrar corte, disponibilidad y procedencia de parámetros. La aceptación del backtest y cualquier gate corresponden al responsable autorizado.
