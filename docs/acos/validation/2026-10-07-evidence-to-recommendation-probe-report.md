# Síntesis de evidencia a recomendaciones — status

Fecha: 2026-10-07. Prueba exploratoria completada, con review del autor no independiente.

## Resultado

Cuatro casos, ocho ejecuciones del mismo modelo en contextos nuevos. Las pautas actuales y las pautas más template acertaron 12/12 campos numéricos y rechazaron escalamiento o extrapolación sin soporte; sus justificaciones y condiciones futuras tienen límites documentados en la segunda revisión. Estados de claims: 10/12 coinciden literalmente en ambas condiciones; los dos desacuerdos son unsupported frente a contradicted ante exposición/efecto y certeza de una afirmación. Los expected y outputs originales no se alteraron.

No aparece ventaja material del suplemento. Recomendación: mantener candidate como conocimiento y usar playbook/templates actuales; no crear ni promover skill.

## Casos

- Retención: MRR expuesto y capacidad predictiva no identifican retorno incremental ni ROI.
- Mercados: tasa global ponderada 13%, no promedio simple 25%; niveles no prueban mejora causal.
- A/B: +1 pp con intervalo que incluye cero y aumento de quejas 6 pp frente a guardrail 2 pp; no escalar.
- Auditoría: 35% en muestra de riesgo, sin tasa poblacional o ahorro identificables.

## Evidencia

[Protocolo](../../../evaluations/evidence-to-recommendation/2026-10-07-template-probe/protocol.md), [review](../../../evaluations/evidence-to-recommendation/2026-10-07-template-probe/review.md), [checks](../../../evaluations/evidence-to-recommendation/2026-10-07-template-probe/deterministic-checks.json), [metadata](../../../evaluations/evidence-to-recommendation/2026-10-07-template-probe/execution-metadata.json).

Baseline: USD 0,139010 / 51,13 s; treatment: USD 0,144640 / 48,78 s acumulados. Una repetición, sin inferencia de ahorro o eficacia general. Modelo claude-sonnet-5-5 effort medium, sin invocación nativa de skill. Refs válidas no prueban soporte completo: la review documenta matices de lineage y de certeza.

## Continuación

Las tres prioridades de capacidades del post-piloto ya tienen rondas exploratorias: maduración, selección operacional y síntesis de recomendaciones. Ninguna justificó nueva skill con evidencia de mejora. Foundry y piloto permanecen intactos; ACOS está instalado para uso diario.

Pendientes de producto: mejorar la UX de cierre de status/next en iniciativa separada y ejecutar Windows nativo. Pendientes de evidencia: review independiente y piloto con datos reales. Las rondas sintéticas no sustituyen estas comprobaciones.


## Segunda revisión — 2026-10-07

[Segunda revisión por agentes](2026-10-07-independent-probe-review.md) confirma los números. C1 mezcla certeza y signo del efecto en el expected; el 10/12 se conserva como coincidencia literal. El linaje del umbral de quejas es incompleto en ambas ramas y ambas permiten reconsiderar B con una medición previa insuficiente para identificar causalidad. D incluye inferencias de sesgo no demostradas. No cambian expected/outputs ni el Foundry; revisión humana externa pendiente.
