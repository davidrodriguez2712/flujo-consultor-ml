# Evaluación exploratoria de disponibilidad temporal

Fecha: 2026-10-07. Continuación del piloto de churn ya cerrado. No se modificó el Foundry ni la evidencia del piloto.

## Status

Cuatro cases, ocho respuestas evaluables del mismo modelo en contextos nuevos. Las pautas actuales y las pautas más contrato breve acertaron 9/9 decisiones de elegibilidad cada una. No hay ventaja observada en la decisión principal; no se recomienda crear otra skill ni promover madurez.

Se detectó ambigüedad del autor en label_state: extracción frente a cutoff. Los checks literales y expected permanecen intactos. Tres mismatches de etiqueta en baseline y dos en treatment no se presentan como mejora: las decisiones de elegibilidad coinciden con el criterio previsto. D baseline añade un intervalo de disponibilidad sin respaldo; no todos los motivos son enteramente correctos. Fences JSON presentes en los ocho outputs pese a la instrucción de JSON puro.

## Evidencia

[Protocolo](../../../evaluations/delayed-outcomes/2026-10-07-contract-probe/protocol.md), [review](../../../evaluations/delayed-outcomes/2026-10-07-contract-probe/review.md), [checks](../../../evaluations/delayed-outcomes/2026-10-07-contract-probe/deterministic-checks.json), [metadata](../../../evaluations/delayed-outcomes/2026-10-07-contract-probe/execution-metadata.json) y [aclaración propuesta](../../../evaluations/delayed-outcomes/2026-10-07-contract-probe/proposed-contract-clarification.md).

Baseline: USD 0,249146 / 47,55 s; treatment: USD 0,239488 / 34,80 s acumulados. Una repetición por case, coste del CLI, sin inferencia de ahorro. Primer intento sin conexión archivado; ejecución fuera del sandbox resolvió acceso a API. Modelo claude-sonnet-5-5, effort medium; contenido de skill proporcionado, sin invocación nativa.

## Qué sigue

Mantener el candidate como conocimiento, tal como estaba decidido. Considerar contrato con estados separados si ese problema reaparece; la propuesta no se ha probado. Segunda prioridad preparada en el roadmap: selección operacional bajo capacidad. Antes de otro experimento fijar protocolo y expected, conservar referencias temporales explícitas y solicitar review independiente para decisiones canónicas Foundry.


## Segunda revisión — 2026-10-07

[Segunda revisión por agentes](2026-10-07-independent-probe-review.md) completada en contexto separado. Confirma los conteos y detecta la afirmación demasiado favorable sobre motivos, corregida arriba. La revisión humana externa permanece pendiente; no cambia expected ni el Foundry.
