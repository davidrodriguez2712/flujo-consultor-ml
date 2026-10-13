---
skill: detect-leakage
version: "0.2.0"
fecha: 2026-10-12
condicion: treatment
estado: "Auditoría documental; sin leakage confirmado en el expediente"
inputs:
  - path: case.md
    sha256: 71613379fe4387f19de862020de6bcdedec00623aeb452bbdff9491690b61d39
  - path: inputs/context.md
    sha256: 2d20272658305e9620515452c404e52d7b2015db0d0a30412287c4aa02a0c1b0
  - path: inputs/observations.csv
    sha256: cbcae4e4f891739ea487feda3f7e1eac58cf9fbe3303b774b5563770f7127462
  - path: inputs/pipeline.py
    sha256: 8fc757e4a3209efdedd3e1b8de6f0b77109557fb6335ac263cd3cea9b3788011
---

## Resumen

El expediente sustenta un uso temporalmente válido de la información mostrada para predecir cancelación en los siete días siguientes de clientes conocidos. No se identifica un mecanismo confirmado de leakage. La conclusión cubre la muestra y el procedimiento declarado; no acredita el código real de producción ni performance.

## Hallazgos

1. **Componente: consumo histórico.** Mecanismo revisado: una agregación podría incluir hechos futuros o llegar después del scoring. El contexto especifica treinta días previos, cierre anterior a la predicción y ausencia de uso del target; en el CSV la disponibilidad precede una hora al scoring en las seis filas. Fuente: `inputs/context.md`, segundo párrafo; `inputs/observations.csv`, filas de datos 1–6. Confianza alta sobre la evidencia documental; severidad informativa, sin contaminación observada. Acción: conservar esta historia y contrastar su construcción con cortes y disponibilidad verificables en la fuente real.

2. **Componente: particiones y labels.** Mecanismo revisado: entrenar con labels aún desconocidos o incorporar outcomes de evaluación. Los tres labels de train están disponibles el 9 de mayo de 2025, antes del entrenamiento declarado del 1 de junio a las 00:00 UTC. El scoring de evaluation ocurre el 2 de junio; sus labels llegan el 10 de junio y se declaran exclusivos de evaluación retrospectiva. Fuente: contexto, primer párrafo; CSV, filas 1–6. Confianza alta sobre el calendario declarado; severidad informativa. Acción: mantener la exclusión de outcomes posteriores del entrenamiento y acreditar el fit efectivo mediante registros.

3. **Componente: entidades recurrentes.** Mecanismo revisado: confundir dependencia por cliente con contaminación o extrapolar a altas nuevas. C01, C02 y C03 reaparecen en evaluation; esto corresponde al scoring posterior de clientes conocidos. `customer_id` es metadata y no entra en las features mostradas. Fuente: contexto; CSV; `pipeline.py`, asignación de `feature_columns`. Confianza alta; severidad informativa. Acción: explicitar ese alcance; si se requiere generalización a clientes nuevos, diseñar una evaluación específica sin sustituir unilateralmente la actual.

4. **Componente: preprocessing y ejecución real.** `prepare` separa las particiones, ajusta el scaler con train y únicamente transforma evaluation: no muestra aprendizaje sobre evaluation. La ejecución real y otras etapas son **No determinables** porque no se aporta su código ni registros. Fuente: `inputs/pipeline.py`, función completa; límite explícito del contexto. Confianza alta sobre el fragmento y limitada sobre producción; severidad media para esa incertidumbre. Acción: conservar el orden mostrado y revisar configuración, artefacto ajustado y flujo de entrenamiento antes de extender la conclusión.

## Evidencia

La utility fija `.runtime/check_inputs.py`, ejecutada con el Python autorizado, produjo los hashes anteriores y contó seis filas y siete columnas. No evalúa leakage. El calendario, recurrencia y orden de operaciones se inspeccionaron por lectura; no se ejecutó el pipeline ni se entrenó. No hay AUC aportado: una señal predictiva alta no prueba contaminación, ni su ausencia certifica seguridad.

## Preguntas abiertas

¿Qué registros reproducen la construcción y disponibilidad histórica del consumo? ¿Qué configuración y artefacto del scaler se usaron? ¿Qué evidencia acredita el timestamp del fit y la exclusión de evaluation de entrenamiento y selección de features?

## Recomendaciones

Solicitar esas evidencias de proceso para contrastar documentación y ejecución. Mantener los outcomes posteriores exclusivamente en el backtest y la población de clientes conocidos. Esta auditoría no autoriza gates ni certifica ausencia universal de leakage.
