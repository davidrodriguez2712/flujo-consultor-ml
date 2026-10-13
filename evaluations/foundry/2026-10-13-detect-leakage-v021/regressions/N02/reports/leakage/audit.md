---
skill: detect-leakage
version: "0.2.1"
fecha: "2026-10-13"
condicion: treatment
estado: "Sin leakage demostrado en el expediente; validez condicionada al proceso declarado"
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

La documentación sustenta un backtest para ofertas mensuales a cuentas existentes, con target de baja en los siete días siguientes. No demuestra leakage por recurrencia, temporalidad ni preprocessing. Esta conclusión depende del escenario y orden declarados; no acredita producción, performance ni generalización a nuevas altas. Se aplicó la guía textual 0.2.1; no se verificó una invocación nativa ni su runtime.

## Hallazgos

1. **Componente:** identidad y particiones. **Conclusión:** recurrencia válida para el escenario documentado. **Mecanismo:** C1 y C2 aparecen en train y evaluation, pero se puntúa una cartera conocida y las altas posteriores quedan excluidas. `client_code` identifica historia disponible desde el alta previa a septiembre; su uso puede aprovechar patrones de cuentas conocidas legítimamente. **Fuente:** `inputs/context.md`, filas de `inputs/observations.csv` y selección de features en `inputs/pipeline.py`. **Confianza:** alta sobre el alcance declarado. **Severidad:** alta si se extrapolara a clientes nuevos; no hay contaminación demostrada aquí. **Acción:** conservar historia e identidad para este alcance y declarar explícitamente su población.

2. **Componente:** disponibilidad de features y labels. **Conclusión:** cronología compatible con el backtest, condicionada a la fecha de entrenamiento. **Mecanismo:** consumo de los 30 días anteriores, disponible el 30 de septiembre y 31 de octubre a las 23:00Z, antes de predicciones del 1 de octubre y 1 de noviembre de 2025. Labels de train disponibles el 9 de octubre; el ajuste declarado el 20 de octubre permite usarlos si corresponde a 2025. Outcomes de evaluation del 9 de noviembre son posteriores, legítimos para evaluación retrospectiva y declarados excluidos del fit. **Fuente:** contexto y CSV. **Confianza:** alta sobre fechas observadas; condicionada sobre año del ajuste. **Severidad:** alta si el fit incorporara labels todavía indisponibles. **Acción:** confirmar año y registro del ajuste; conservar outcomes como etiquetas de backtest.

3. **Componente:** encoder y scaler. **Conclusión:** orden declarado correcto. **Mecanismo:** ambos ejecutan `fit_transform` exclusivamente sobre train y `transform` sobre evaluation; no se muestra aprendizaje con evaluación. **Fuente:** `inputs/pipeline.py`, función `prepare`. **Confianza:** alta sobre código inspeccionado, sin verificación de ejecución. **Severidad:** alta ante un orden real distinto. **Acción:** mantener este orden y acreditar su ejecución antes de aceptar el backtest.

## Evidencia

La utility autorizada terminó correctamente: hashes SHA-256 consignados arriba y cuatro filas de CSV. Lectura manual: dos filas por partición y los mismos dos códigos en ambas. Las comparaciones temporales y el orden de transformaciones proceden de inspección, no de checks ejecutados. No se ejecutó el pipeline, entrenó modelo ni calculó performance. No hay evidencia de joins, resampling o selección adicional.

## Preguntas abiertas

¿El ajuste del 20 de octubre corresponde a 2025? ¿Los registros operativos corroboran disponibilidad, exclusión de outcomes de evaluation y ejecución del orden aportado?

## Recomendaciones

El owner debe confirmar estos puntos y aceptar el alcance de cartera existente antes de utilizar resultados del backtest. La fecha del ajuste sin año es una brecha documental: confirmaría riesgo una cronología que usara labels indisponibles; permitiría validez un ajuste posterior al 9 de octubre de 2025 y anterior al scoring de noviembre, con linaje declarado acreditado. No se justifica eliminar cuentas recurrentes ni convertir la identidad en una prohibición general.
