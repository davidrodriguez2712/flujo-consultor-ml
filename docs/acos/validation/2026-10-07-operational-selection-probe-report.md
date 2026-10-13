# Selección operacional — status de la prueba

Fecha: 2026-10-07. Prueba exploratoria completada; no evaluación canónica del Foundry.

## Resultado

Cuatro cases, ocho outputs evaluables. Baseline playbook actual resolvió las decisiones de los cuatro cases. Treatment mismo playbook más pauta adicional no mostró ventaja: invirtió orden de selección en C (miembros correctos) y devolvió en D un campo decision diferente del expected, aunque niega correctamente identificación causal en texto; el significado del campo no quedó definido de forma inequívoca. Capacidad, métricas y límites sustantivos correctos en ambos.

Conclusión recomendada: mantener candidate como conocimiento; no crear skill, adoptar suplemento ni promover madurez. Review del autor no independiente; una repetición por case.

## Casuísticas

1. Top-K con empate de scores y desempate fijado antes de labels.
2. Cooldown de contactos, elegibles menos que capacidad y denominadores de la población correcta.
3. Labels solo de inspeccionados: cobertura parcial, métricas no identificables y null distinto de negativo.
4. Riesgo de churn distinto de beneficio causal de contacto; sin ROI o clientes salvados inventados.

## Evidencia

[Protocolo](../../../evaluations/operational-selection/2026-10-07-playbook-probe/protocol.md), [review](../../../evaluations/operational-selection/2026-10-07-playbook-probe/review.md), [checks](../../../evaluations/operational-selection/2026-10-07-playbook-probe/deterministic-checks.json) y [metadata](../../../evaluations/operational-selection/2026-10-07-playbook-probe/execution-metadata.json).

Claude-sonnet-5-5 effort medium; sin invocación nativa de skill, herramientas ni expected en payload. Baseline USD 0,122268 / 52,46 s; treatment USD 0,123574 / 83,10 s acumulados. No inferencia de ahorro, superioridad general o recurrencia real.

## ACOS instalado para uso diario

Instalación persistente 0.1.0 con uv realizada. `acos` disponible en `/Users/davidrodriguez/.local/bin/acos` y resuelto desde PATH fuera del checkout. Proyecto copiado fuera del repositorio: status COMPLETED/integrity OK y handoff PASS. [Registro](2026-10-07-persistent-install-checks.json).

Siguiente prioridad propuesta: síntesis de evidencia a recomendaciones, contrastando playbook/template antes de nueva skill. Windows y piloto real siguen pendientes; no se publicó en PyPI.


## Segunda revisión — 2026-10-07

[Segunda revisión por agentes](2026-10-07-independent-probe-review.md) confirma los checks. Los inputs ya prescriben buena parte de las decisiones: el resultado no aísla el aporte del playbook. C treatment afirma no representatividad sin mecanismo conocido; corresponde no asumirla. Los hashes acreditan consistencia actual, no preregistro temporal completo. No se recalifican outputs ni se modifica Foundry; revisión humana externa pendiente.
