# Contrato temporal — resultado de la ronda 03

Fecha local: 2026-10-08 (America/Lima). Diseño aprobado y **24 llamadas Claude ejecutadas**, seis escenarios nuevos con tres registros y dos repeticiones por condición. Evaluación sintética cerrada con revisión del autor; revisión humana de las conclusiones pendiente.

## Conclusión

**No se observó mejora en decisiones temporales al añadir treatment.** Ambas condiciones acertaron todos los campos y decisiones. La revisión del autor encontró dos preguntas problemáticas en baseline y ninguna en treatment; es una señal secundaria exploratoria, insuficiente para demostrar eficacia o justificar una skill nueva/promoción.

El criterio prospectivo exigía mejora decisional en al menos dos escenarios, dirección consistente entre repeticiones y ausencia de errores adicionales. No se cumple: hay empate completo en las decisiones. No aumentar rondas temporales sintéticas automáticamente para buscar una ventaja.

## Qué se comparó

Baseline recibió el snapshot de design-validation 0.1.0 usado anteriormente; treatment recibió exactamente lo mismo más el contrato temporal local 0.1.0. Mismo task, schema 0.1.0, runner 0.2.0, expedientes y modelo solicitado/reportado claude-sonnet-5-5. No se probó descubrimiento ni invocación nativa de skill: las pautas se incluyeron en el payload.

Los expedientes combinan notas y registros de negocio. La tarea conserva definiciones mínimas de los tres ejes; se eliminaron instrucciones de resolución detalladas, pero no toda la guía. Los escenarios son nuevos, no nuevos tipos de riesgo temporal ni un benchmark externo oculto al autor.

| Escenario | Riesgo revisado | Elegibilidad baseline/treatment, cada repetición |
|---|---|---|
| A — Churn reversible | Solicitud, plazo de retirada y certificación | 3/3 y 3/3 |
| B — Churn retrospectivo | Fecha del evento frente a publicación; cero sin semántica | 3/3 y 3/3 |
| C — Retención incompleta | Negativo certificado frente a seguimiento abierto | 3/3 y 3/3 |
| D — Crédito tardío | Evento, firma y publicación en almacén | 3/3 y 3/3 |
| E — Features reconstruidas | Fecha de referencia frente a disponibilidad real | 3/3 y 3/3 |
| F — Documentos contradictorios | Prioridad explícita, conflicto y exclusión comprobada | 3/3 y 3/3 |

## Resultados

| Comprobación | Baseline | Treatment |
|---|---:|---:|
| Llamadas exitosas y schema local válido | 12/12 | 12/12 |
| IDs exactos y gate NEEDS_REVIEW | 12/12 | 12/12 |
| Campos temporales correctos | 108/108 | 108/108 |
| Decisiones de elegibilidad correctas | 36/36 | 36/36 |
| Admisiones indebidas | 0 | 0 |
| Registros válidos excluidos o indeterminados | 0 | 0 |
| Errores materiales en razones, revisión del autor | 0 | 0 |
| Outputs con preguntas problemáticas, revisión del autor | 2/12 | 0/12 |
| Entradas redundantes / outputs que las contienen | 18 / 10 | 16 / 11 |
| Coste reportado por CLI, USD | 0.7838402 | 0.8652664 |
| Tiempo de pared acumulado, segundos | 146.481 | 161.178 |

Coste total reportado: **USD 1.6491066**, estimación del CLI, no factura. No se ejecutaron llamadas adicionales ni reintentos del runner; el mecanismo nativo puede realizar pasos internos. Ambos tuvieron dos turns reportados por llamada. Effort medium y restricciones de herramientas/MCP/sesión constan solicitados en argv; su aplicación efectiva no está acreditada por el envelope. CLI observado: 2.1.294 (Claude Code).

## Revisión semántica

La pregunta 4 de A/baseline/2 equipara una retirada a churn=0 sin regla documentada de certificación negativa. La pregunta 1 de C/baseline/1 plantea reclasificar un seguimiento abierto mediante un acta anterior a extracción, aunque el cierre obligatorio de ventana es posterior a extracción. Sus clasificaciones finales siguen siendo correctas; estos hallazgos no se suman como errores de elegibilidad.

Ambas condiciones incluyen preguntas redundantes y comentarios fuera del objetivo inmediato. Treatment tiene menos entradas redundantes, pero más outputs con alguna: no presentar esto como reducción uniforme. Las categorías son interpretativas y fueron asignadas por el autor leyendo las respuestas, sin cegamiento ni revisor independiente. Algunos strings en open_questions son declaraciones; el schema no verifica forma interrogativa.

## Evidencia y verificación

- [Protocolo](../../../evaluations/delayed-outcomes/2026-10-08-contract-probe-03/protocol.md) y [preregistro local](../../../evaluations/delayed-outcomes/2026-10-08-contract-probe-03/preregister.json): 32 archivos congelados antes del primer call. Hashes y timestamps locales no acreditan preregistro externo.
- [Checks deterministas](../../../evaluations/delayed-outcomes/2026-10-08-contract-probe-03/deterministic-checks.json), [resumen](../../../evaluations/delayed-outcomes/2026-10-08-contract-probe-03/summary.json), [revisión](../../../evaluations/delayed-outcomes/2026-10-08-contract-probe-03/review.md) y [detalle semántico](../../../evaluations/delayed-outcomes/2026-10-08-contract-probe-03/semantic-review.json).
- Cada llamada conserva payload, schema, argv, stdout/stderr, envelope, structured_output, metadata y ejecución del checker. Los 24 checks fueron reproducidos al cierre.
- Pruebas del runner y checker: **23 passed**. Suite ampliada de producto, piloto y utilidades: **138 passed**, ejecutada en esta sesión.
- Integridad: **456 archivos previos** (incluido el check técnico 0.2.0) y **48 entradas protegidas del piloto** conservan hashes; freeze de ronda 03 también intacto. [Check](../../../evaluations/delayed-outcomes/2026-10-08-contract-probe-03/integrity-check.json).
- [Manifest de cierre](../../../evaluations/delayed-outcomes/2026-10-08-contract-probe-03/evidence-manifest.json).

## Límites y siguientes pasos

Seis casos sintéticos y dos repeticiones no prueban generalidad, significancia ni desempeño con clientes reales. Las repeticiones no convierten 18 registros en 36 casos independientes. Se evalúa el suplemento temporal, no la eficacia general de la skill baseline ni todo ACOS. El contrato sigue propuesto; no hubo cambios en Foundry ni compiler ni paquete instalado.

1. Revisar estas conclusiones con el responsable humano antes de decidir adopción documental. La ejecución y la revisión del autor están completas; revisión humana externa pendiente.
2. Cerrar esta línea exploratoria temporal sin crear otra skill por el empate. Conservar los hallazgos sobre preguntas como hipótesis de pertinencia, sin candidate nueva automática; comprobar primero si una capacidad existente cubre esa necesidad.
3. Siguiente evaluación recomendada: selección operacional bajo costes y capacidad. Revisar primero los criterios ambiguos de su ronda anterior y diseñar una comparación que distinga ranking, factibilidad y valor esperado. Esa continuación requiere su diseño concreto; no está ejecutada.

En el proyecto general continúan pendientes la ejecución nativa Windows y un piloto con datos reales.
