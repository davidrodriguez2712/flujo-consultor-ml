---
skill: detect-leakage
version: "0.2.2"
fecha: 2026-10-13
estado: leakage_confirmado
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

El expediente demuestra leakage en el ajuste del scaler: incorpora solicitudes de evaluación de noviembre antes de separar las particiones, aunque el entrenamiento se declara para el 1 de octubre. El backtest preparado así no sustenta una evaluación independiente para esa decisión. No se calculó performance ni se estima su alteración.

Auditoría en modo textual con la guía detect-leakage 0.2.2; no se verificó una Skill/plugin nativo. Los hashes y el conteo CSV proceden de la utility autorizada ejecutada.

## Hallazgos

**Componente:** preprocessing, con contaminación temporal y entre particiones. **Conclusión:** confirmado. **Mecanismo:** `scaler.fit_transform(data[["amount"]])` aprende media y desviación de toda la tabla; después se seleccionan train y evaluación. Los importes de R3 y R4, solicitudes del 1 y 2 de noviembre de 2025, determinan parámetros aplicados a train antes de una decisión de entrenamiento fijada al 1 de octubre. La evaluación deja de estar reservada durante el ajuste. **Fuente:** `inputs/pipeline.py`, `inputs/context.md` y `inputs/observations.csv`. **Confianza:** alta sobre el mecanismo declarado, sin ejecución del pipeline. **Severidad:** comprometida la validez del backtest para el escenario declarado; magnitud del impacto predictivo no estimable con esta auditoría. **Acción proporcional:** separar primero las particiones, ajustar el scaler exclusivamente con train y transformar evaluación con esos parámetros; solicitar al responsable un backtest corregido antes de aceptar resultados.

## Evidencia

El contexto documenta nuevas solicitudes de noviembre como población de scoring, disponibilidad de `amount` al recibir cada solicitud y labels de train maduros antes del 1 de octubre. Estas condiciones permiten usar importe como predictor y outcomes retrospectivos como labels; no justifican aprender parámetros de solicitudes futuras durante el entrenamiento.

El CSV contiene R1 y R2 en train, con fechas de agosto, y R3 y R4 en evaluación, con fechas de noviembre. El código no utiliza `target` para ajustar el scaler. El contexto declara ausencia de joins y encoding; no se infieren mecanismos adicionales.

La utility `.runtime/check_inputs.py` terminó correctamente y reportó cuatro filas CSV y los hashes consignados. Solo verifica datos genéricos de archivos: no evalúa leakage. El pipeline se inspeccionó, no se ejecutó; no hubo entrenamiento ni cálculo de métricas.

## Preguntas abiertas

¿Quién aceptará la corrección del backtest y aportará evidencia del ajuste exclusivo sobre train? ¿Qué efecto tendrá la corrección en los resultados? Esto requiere trabajo posterior autorizado; no altera la conclusión sobre el orden declarado.

## Recomendaciones

Mantener `amount` como predictor según su disponibilidad documentada. Corregir el alcance del ajuste, conservando la fecha de entrenamiento y las particiones declaradas. Si posteriormente se utiliza validación cruzada, ajustar las transformaciones dentro de cada fold de entrenamiento. El responsable debe revisar la evidencia del proceso corregido y decidir su aceptación; este informe no certifica producción ni ausencia universal de leakage.
