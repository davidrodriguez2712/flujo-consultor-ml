---
skill: none
version: null
fecha: 2026-10-11
inputs:
  - path: case.md
    sha256: 072562c9846d5469c9041edf8e3fb5e23cc42d440441b8204aa40e3b9c949a96
  - path: inputs/context.md
    sha256: 5417d10f78d29b1f98792a7aed6b198a39fdd07b4693dd07446dbcf0fa87ea55
  - path: inputs/observations.csv
    sha256: 56ee9a0e4e5e5a02703509266b3df2b071ef47fc526891c53837916d338835ee
  - path: inputs/pipeline.py
    sha256: ef460cae4444fd60c18b1a6a2906c3e6850312f39fc1c3bc254c22b737ce4cda
estado: auditado_con_limitaciones
condicion: baseline
---

## Resumen

No se identifica leakage en la evidencia aportada para ofertas mensuales a cuentas existentes. La reutilización de cuentas entre meses coincide con la población declarada. La preparación ajusta transformaciones exclusivamente con train y las fechas permiten entrenar antes de la evaluación de noviembre. Esta conclusión es acotada: no certifica el entrenamiento completo, la construcción del consumo ni resultados predictivos. No se aprueban decisiones de negocio ni gates del Foundry.

## Hallazgos

1. **Componente: fechas de features y etiquetas.** Mecanismo examinado: incorporar información futura al predecir o etiquetas aún desconocidas al ajustar. Fuente: inputs/context.md y observations.csv. Todas las features figuran disponibles una hora antes de su prediction_at; las etiquetas train del 9 de octubre anteceden al ajuste declarado del 20 de octubre. Las etiquetas evaluation del 9 de noviembre son posteriores a la predicción y, según contexto, solo sirven al backtest. Confianza: alta sobre las fechas visibles, limitada sobre su trazabilidad. Severidad: sin fuga observada; incertidumbre material si la disponibilidad declarada no representa la real. Acción: conservar evidencia de disponibilidad y del corte de entrenamiento.

2. **Componente: encoder y scaler.** Mecanismo examinado: aprender categorías o estadísticas usando evaluation. Fuente: inputs/pipeline.py, función prepare. Ambos fit_transform reciben solo train; evaluation recibe transform. Confianza: alta para el fragmento inspeccionado. Severidad: sin contaminación observada; alcance incompleto respecto al resto del pipeline. Acción: revisar las entradas reales del fit del modelo y cualquier selección o transformación adicional.

3. **Componente: client_code y particiones.** Mecanismo examinado: transferencia de identidad entre train y evaluation. Fuente: contexto y CSV; C1 y C2 aparecen en ambos meses. Las cuentas ya existían y la decisión se aplica a esa misma cartera: compartir identidad no demuestra fuga por sí mismo. Confianza: alta respecto a la población declarada. Severidad: sin fuga demostrada; limitación material de generalización. Acción: mantener el backtest temporal para esta cartera y documentar que no estima desempeño sobre nuevas altas. El identificador puede permitir memorizar diferencias históricas entre cuentas; su utilidad y estabilidad requieren evidencia adicional.

## Evidencia

La utility fija se ejecutó con el Python del workspace: devolvió hashes SHA-256 anteriores y cuatro filas del CSV. No evalúa leakage. La inspección fue estática: no se ejecutó pipeline.py, no se entrenó y no se calculó performance. El ajuste del 20 de octubre permite evaluar noviembre; no sustenta afirmar que ese modelo emitió predicciones el 1 de octubre, fecha histórica de train.

## Preguntas abiertas

¿Cómo se demuestra que el consumo excluye eventos posteriores y revisiones tardías? ¿El entrenamiento completo excluye targets y resultados de evaluation de toda selección, ajuste e ingeniería? ¿Cómo se define y completa la etiqueta de baja en siete días? No se aporta código ni registro para resolver estas preguntas.

## Recomendaciones

Documentar el corte del 20 de octubre, la procedencia temporal de las features y el uso exclusivo de outcomes de noviembre para evaluar. Inspeccionar el fit completo antes de ampliar la conclusión. Mantener explícita la población de cuentas existentes; cualquier evaluación de altas futuras necesitaría otro diseño. Cuatro observaciones y ausencia de performance impiden concluir precisión, estabilidad o conveniencia comercial.
