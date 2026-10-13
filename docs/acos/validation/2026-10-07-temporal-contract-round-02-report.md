# Contrato temporal — resultado de la ronda 02

Fecha local: 2026-10-07 (America/Lima). Seis cases nuevos, dos industrias sintéticas y dos repeticiones por condición: **24 invocaciones**. Ejecución, checks y revisión separada por agentes completados; revisión humana externa pendiente.

## Resultado

| Comprobación | Baseline | Treatment |
|---|---:|---:|
| Calls sin error de ejecución | 12/12 | 12/12 |
| JSON puro | 8/12 | 9/12 |
| Outputs con contenido estructurado evaluable | 11/12 | 12/12 |
| Elegibilidad correcta entre filas evaluables | 22/22 | 24/24 |
| Filas no evaluables | 2 | 0 |
| Outputs con preguntas redundantes/problemáticas | 6 | 0 |

La respuesta E baseline, repetición 1, omite un valor y contiene JSON inválido. Sus dos filas siguen en el denominador de 24, sin repararlas ni clasificarlas como decisiones temporales incorrectas. Los checks completos reportan 66/72 campos entregados correctos frente a 72/72; la diferencia viene exclusivamente de ese output no evaluable.

Entre las decisiones evaluables, ambas condiciones aciertan: no aparece una ventaja en razonamiento temporal. El contrato muestra señales exploratorias de mejor entrega estructurada y menos preguntas problemáticas; treatment conserva una pregunta de pertinencia incierta. Las razones legibles no contienen errores temporales, pero dos preguntas baseline añaden supuestos/afirmaciones incorrectos.

## Casos

1. Extracción posterior y disponibilidad histórica del label.
2. Igualdad permitida y un segundo después del entrenamiento.
3. Feature futura y disponibilidad de features desconocida.
4. Positivo temprano certificado frente a flag provisional.
5. Cero provisional y certificación desconocida.
6. Filas válidas y equivalencias entre zonas horarias.

Baseline recibió el contenido actual de design-validation 0.1.0; treatment, el mismo contenido más contrato temporal local 0.1.0. Task/schema/inputs comunes y orden invertido en segunda repetición. No invocación nativa de skill ni entrenamiento.

## Evidencia y límites

[Protocolo](../../../evaluations/delayed-outcomes/2026-10-07-contract-probe-02/protocol.md), [review previa](../../../evaluations/delayed-outcomes/2026-10-07-contract-probe-02/preregister-review.md), [checks](../../../evaluations/delayed-outcomes/2026-10-07-contract-probe-02/deterministic-checks.json), [review completa](../../../evaluations/delayed-outcomes/2026-10-07-contract-probe-02/review.md), [revisor A/B/C](../../../evaluations/delayed-outcomes/2026-10-07-contract-probe-02/review-abc.md), [revisor D/E/F](../../../evaluations/delayed-outcomes/2026-10-07-contract-probe-02/review-def.md) y [manifest](../../../evaluations/delayed-outcomes/2026-10-07-contract-probe-02/evidence-manifest.json).

Se verificaron 41 archivos congelados y se reprodujeron los 24 comandos del checker. Manifest final: 263 archivos. Antes del freeze pasaron 123 pruebas locales, incluidas 13 del checker/runner. Payloads, argv, CLI 2.1.293, respuestas raw, tiempos y costes conservados. Modelo efectivo reportado: claude-sonnet-5-5. Parámetros no expuestos por el runtime permanecen desconocidos; timestamps locales no acreditan preregistro externo.

Coste reportado: baseline USD 0,737532; treatment USD 0,825128; total USD 1,562660. Tiempo de pared acumulado: 109,811 s / 113,289 s. No inferir ahorro o velocidad general.

Dos repeticiones y casos con reglas explícitas no prueban generalidad o significancia. Los reviewers son agentes separados del autor; no sustituyen revisión humana externa. La evidencia anterior, el piloto y el Foundry permanecen sin cambios.

## Recomendación

Conservar el contrato como propuesta local. No justificar una skill nueva ni promoción por esta ronda. El fallo observado que impide consumir una respuesta es estructural; una futura continuación debería aislar cumplimiento de schema con un mecanismo común y ampliar evidencia antes de atribuir eficacia temporal. Esa continuación aún no está diseñada ni ejecutada.
