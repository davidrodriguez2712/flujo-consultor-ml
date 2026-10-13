---
skill: detect-leakage
version: 0.2.1
fecha: 2026-10-13
estado: confirmado
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

El backtest declarado contiene leakage confirmado de preprocessing: el scaler aprende de entrenamiento y evaluación conjuntamente antes de separarlos. Los importes de solicitudes de noviembre influyen en parámetros que deberían estar fijados al entrenar el 1 de octubre. El expediente no sustenta ese uso para la decisión descrita. No se calculó performance ni se ejecutó el pipeline.

Se aplicó la guía textual detect-leakage 0.2.1; no hubo invocación nativa ni verificación del runtime de esa skill.

## Hallazgos

- **Componente:** scaler sobre `amount`. **Conclusión:** Confirmado. **Mecanismo:** `fit_transform(data[["amount"]])` recibe todas las filas; las máscaras de partición se aplican después. Según el contexto, aprende media y desviación de las filas recibidas. Por tanto, R3 y R4 de evaluación participan en el ajuste que transforma también R1 y R2 de entrenamiento. Esto incorpora distribución futura de noviembre al procesamiento del entrenamiento declarado para octubre. **Fuente:** `inputs/pipeline.py`, función `prepare`; `inputs/context.md`; `inputs/observations.csv`. **Confianza:** alta respecto del orden declarado, sin comprobación de ejecución real. **Severidad:** alta por contaminación de la evaluación y falta de correspondencia temporal con el escenario; magnitud y dirección del efecto sobre métricas desconocidas. **Acción:** separar primero, ajustar exclusivamente con train y transformar evaluación con parámetros congelados; reconstruir el backtest antes de usarlo como evidencia.

## Evidencia

La utilidad fija `.runtime/check_inputs.py` se ejecutó mediante el Python autorizado: produjo los hashes anteriores y contó cuatro filas, con columnas `application`, `partition`, `prediction_at`, `amount`, `target`. No detecta leakage ni verifica comportamiento del pipeline.

Por lectura directa, R1/R2 pertenecen a train en agosto de 2025, con importes 100/200; R3/R4 pertenecen a evaluación en noviembre de 2025, con importes 9000/12000. No se calcularon estadísticas del scaler.

El contexto acredita disponibilidad de `amount` al recibir cada solicitud y maduración de labels de entrenamiento antes del 1 de octubre. Esas condiciones son compatibles con su uso declarado. Los targets de evaluación pueden servir como outcomes retrospectivos de mora a 30 días; el código mostrado no los usa para ajustar el scaler. No hay joins ni encoding según el expediente. Estas observaciones no certifican ausencia universal de leakage.

## Preguntas abiertas

¿Existen artefactos del ajuste y separación corregidos que permitan verificar el backtest reconstruido? ¿Quién acepta su revisión? El expediente no identifica owner ni demuestra ejecución real; tampoco permite cuantificar impacto estadístico.

## Recomendaciones

Proponer al responsable del backtest reservar el uso de sus resultados actuales hasta corregir y revisar el preprocessing. Conservar importes disponibles y labels maduros, aplicar parámetros aprendidos solo de train y, si posteriormente se incorporan folds, ajustar dentro de cada fold. Solicitar evidencia del nuevo orden y parámetros persistidos. La aceptación corresponde al owner; esta auditoría no aprueba decisiones de negocio ni gates.
