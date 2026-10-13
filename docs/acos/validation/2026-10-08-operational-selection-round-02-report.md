# Selección operacional — resultado de la ronda 02

Fecha local: 2026-10-08 (America/Lima). Diseño y **24 llamadas aprobados**, seis casos nuevos y dos repeticiones por condición. Ejecución, checks, revisión del autor y revisión separada por agente completas. Revisión humana externa de conclusiones pendiente.

## Conclusión

**No se observó mejora decisional del treatment respecto del baseline.** Las 12 respuestas por condición coinciden en todos los campos comprobados. La revisión semántica encuentra afirmaciones adicionales incorrectas, ambiguas o fuera de alcance en ambas condiciones. Un schema válido y campos correctos no convierten todo el texto en correcto.

El criterio previo requería mejora en al menos dos escenarios, consistente entre repeticiones y sin errores adicionales. No se cumple por empate. Recomendar mantener el candidate `evaluate-operational-selection` como conocimiento y el contrato 0.2.0 como propuesta local. No crear/promover una skill, adoptar una nueva capacidad ni integrar el suplemento automáticamente en ACOS.

## Diseño y cambios

Baseline recibió el snapshot del playbook `experiments-and-models` de la ronda anterior; treatment añadió únicamente un contrato local de selección operacional 0.2.0. Mismos inputs, task, schema y modelo. Esta versión extiende el alcance del contrato 0.1.0: selección pequeña indivisible con costes variables y presupuesto, además de Top-K. No recalifica ni modifica la ronda anterior.

Se añadieron runner de selección 0.1.0, schema 0.1.0 y checker/oracle. El transporte deriva del runner temporal 0.2.0, conservado intacto. Son utilidades del checkout; el paquete instalado de ACOS no cambió. [Uso y límites](../evaluation-contracts/selection-runner.md), [propuesta 0.2.0](../evaluation-contracts/operational-selection-0.2.0.md).

El schema separa selección, ranking descriptivo, capacidad, factibilidad, optimalidad, métricas por población y estado causal. `schema_conformant` incluye Pydantic estricto más guards locales de texto no blanco, Unicode válido y unicidad; JSON Schema no expresa todos esos guards. No fuerza decisiones correctas ni aprobación humana. El runner no lee expected, repara resultados o reintenta; el mecanismo nativo puede tener pasos internos.

## Casos y respuestas verificadas

| Caso | Decisión y comprobaciones principales |
|---|---|
| A — Capacidad y elegibilidad | Y,Z por empate/ID; 2 elegibles frente a capacidad 3; coste 4; precision 0.5, recall 1, lift 1. |
| B — Outcomes parciales | W,Q; coste 2; precision 0.5 identificable, recall/lift no identificables. |
| C — Presupuesto/greedy | B,C, coste 10 y valor neto 20; A solo da 13. Greedy por score o ratio pierde. |
| D — Valor negativo | Vacío óptimo, coste/valor 0; precision/lift indefinidos, recall 0. |
| E — Experimento válido | Efectos promedio estimados 0.10, 0.04, -0.01; netos 5,6,-4. M2,M1, coste 7, valor 11. Óptimo de point estimates bajo supuestos. |
| F — Datos insuficientes | Selección pendiente; ranking P,Q,R descriptivo. Faltan efectos de contacto y coste de P; no afirmar campaña óptima. |

Expected se derivó manualmente; C/D/E se comprobaron enumerando todos los subconjuntos factibles. El reviewer recomputó E desde los conteos del experimento y confirmó los tres oracles antes del freeze. E optimiza estimaciones promedio por estrato transportadas bajo supuesto explícito; no conoce efectos individuales ni acredita optimalidad real bajo incertidumbre.

## Resultados por condición

| Comprobación, 12 outputs por condición | Baseline | Treatment |
|---|---:|---:|
| Runtime exitoso, schema local válido y modelo verificado | 12/12 | 12/12 |
| Miembros seleccionados | 12/12 | 12/12 |
| Orden seleccionado / ranking completo | 12/12 / 12/12 | 12/12 / 12/12 |
| Elegibles, capacidad y tamaño seleccionado | 12/12 | 12/12 |
| Coste y valor esperado | 12/12 | 12/12 |
| Factibilidad / optimalidad | 12/12 / 12/12 | 12/12 / 12/12 |
| Métricas, estados y población | 12/12 | 12/12 |
| Estado de identificación causal | 12/12 | 12/12 |
| Gate NEEDS_REVIEW | 12/12 | 12/12 |
| Coste reportado por CLI, USD | 0.4061322 | 0.4543664 |
| Tiempo de pared acumulado, segundos | 180.317 | 206.286 |

Cada dimensión se informa por separado, sin score compuesto. Texto de estimand y razones no se comparan literalmente: se revisaron semánticamente. Los valores null de estimand en el esqueleto privado de expected E/F no representan un estimand correcto; el checker deliberadamente no los usa y los cuatro outputs E/F por condición sí expresan el efecto relevante. No presentar los checks como validación completa de todas las frases.

Coste total reportado: **USD 0.8604986**, estimación CLI, no factura. Modelo solicitado y reportado `claude-sonnet-5-5`; CLI 2.1.294 (Claude Code). Las 24 llamadas reportan 2 turns cada una. Effort medium y restricciones tools/MCP/persistencia constan solicitados en argv, no acreditados íntegramente como configuración efectiva. No se agregaron llamadas ni reintentos del runner.

## Revisión semántica

[Autor](../../../evaluations/operational-selection/2026-10-08-selection-probe-02/author-review.md) y [otro agente](../../../evaluations/operational-selection/2026-10-08-selection-probe-02/independent-review.md) revisaron las 24 respuestas. El reviewer conocía condiciones/casos desde antes del freeze y no leyó conclusiones del autor: revisión separada, no ciega ni humana externa.

Hallazgos que los campos correctos no reflejan:

- A/baseline/1 y A/treatment/2 afirman que con dos registros no se puede estimar incertidumbre. El tamaño pequeño no acredita esa imposibilidad; diferenciar métricas exactas del lote y generalización bajo supuestos.
- C/baseline/1 describe incorrectamente la sensibilidad a elevar el valor de A: A solo puede ganar a BC sin combinarse con otro, desde valor 20 por desempate de coste.
- B/baseline/1 y B/baseline/2 infieren que R no fue inspeccionado a partir de su label ausente. Esa causa no está documentada. Baseline1 además no delimita claramente el posible sesgo de generalización frente a la precision exacta del lote.
- F/baseline/2 no distingue claramente el límite de coste de P solo (8) del límite en pares (4); treatment2 sí distingue ambos.
- Varias respuestas F reabren clientes salvados frente a valor monetario, aunque el objetivo de conteo está definido. Treatment1 presenta monetización como algo que hace falta; cambiaría el objetivo. Ambas condiciones generan preguntas redundantes o proponen trabajo alternativo.

Los CIs adicionales de E coinciden con Wald no pooled y suma de varianzas de estratos independientes declarados: [comprobación aritmética](../../../evaluations/operational-selection/2026-10-08-selection-probe-02/additional-ci-arithmetic.json). No eran resultados requeridos; no acreditan supuestos reales, cobertura conjunta, intervalos postselección ni certeza del resultado individual. No asignar score semántico retrospectivo ni convertir diferencias de estilo en mejora demostrada.

## Evidencia y verificación

- [Protocolo](../../../evaluations/operational-selection/2026-10-08-selection-probe-02/protocol.md), [review previa](../../../evaluations/operational-selection/2026-10-08-selection-probe-02/preregister-review.md) y [preregistro](../../../evaluations/operational-selection/2026-10-08-selection-probe-02/preregister.json): **45 archivos** congelados antes del primer call; hashes/timestamps locales, sin anclaje temporal externo.
- [Checks](../../../evaluations/operational-selection/2026-10-08-selection-probe-02/deterministic-checks.json) y [resumen](../../../evaluations/operational-selection/2026-10-08-selection-probe-02/summary.json). Los 24 checks fueron reproducidos al cierre y por el reviewer.
- Cada llamada conserva payload, schema, argv, raw, stdout/stderr, structured_output, metadata y comando/resultados de checker.
- TDD: 12 pruebas inicialmente RED por utilidades ausentes; 12 GREEN; una prueba adicional RED por ranking_match ausente y 13 GREEN. Suite local fresca **125 passed**; ampliada **151 passed**.
- [Integridad](../../../evaluations/operational-selection/2026-10-08-selection-probe-02/integrity-check.json): **788 archivos anteriores** y **48 entradas protegidas del piloto** conservan hashes; freeze intacto.
- [Manifest de cierre](../../../evaluations/operational-selection/2026-10-08-selection-probe-02/evidence-manifest.json).

## Límites y siguiente hito

Seis casos sintéticos, dos repeticiones y un modelo no prueban generalidad ni significancia. Los inputs fijan objetivos y varias reglas para que expected sea inequívoco; eso eleva baseline y puede producir techo. Se evalúa el suplemento incluido en payload, no descubrimiento/carga nativa de skill ni eficacia general del playbook. No se cubren routing, objetivos no aditivos, optimización a gran escala o procesos reales de cliente.

Recomendación: cerrar estas comparaciones sintéticas temporal/selección como evidencia exploratoria, revisar conclusiones con el responsable humano y pasar a un segundo piloto e2e de riesgo de crédito con capacidades existentes. Si aún no hay datos reales, el piloto debe etiquetarse sintético y evaluar el workflow completo, no presentarse como validación de rendimiento en clientes. No seguir sumando skills o calls para buscar una ventaja no observada.

Foundry y compiler sin cambios. Revisión humana externa, ejecución nativa Windows y piloto con datos reales siguen pendientes; el segundo piloto propuesto aún no está diseñado ni ejecutado.
