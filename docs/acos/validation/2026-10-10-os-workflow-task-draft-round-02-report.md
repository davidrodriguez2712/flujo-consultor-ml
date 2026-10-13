# Task concreto — ronda02 completada: resultado mixto

## Resultado

Se recogieron el smoke y las ocho respuestas con Claude Code2.1.296/Haiku5.5, sin reintentos, nueve HTTP200/end_turn y usage conocido. El smoke explícito pasó. La revisión semántica está terminada; **no se cumple la regla exploratoria favorable** y no queda acreditada eficacia general.

| Medida, sobre cuatro casos | Baseline | Treatment |
|---|---:|---:|
| Formato válido | 4/4 | 3/4 |
| Contenido completo según rúbrica | 1/4 | 2/4 |
| Formato y contenido completos | 1/4 | 1/4 |
| Estado esperado | 3/4 | 3/4 |

No se agregan obligaciones con denominadores diferentes. Contenido de formato inválido se reconoce solo como diagnóstico; el raw y su FAIL no se reparan.

## Lectura por caso

| Caso | Baseline | Treatment | Comparación conjunta |
|---|---|---|---|
| D01 forecast/inventario | Objetivo e informe propuesto, pero redacción delegada y sin criterios observables | Borrador más concreto, pero output futuro genérico y sin criterios observables | Ambas FAIL |
| D02 anomalías sin labels | Contenido utilizable distribuido en bullets, formato válido | Borrador concreto, pero READY como prefacio y sin H2 Estado | Regresión de formato |
| D03 preparación de evaluación RAG | Instrucciones para redactar después, sin outputs/criterios específicos | Preguntas con respuestas/fuentes y rúbrica, criterios revisables y límites | Mejora |
| D04 seguimiento sin task | Tres acciones sin tarea, pero NOT_DETERMINABLE | Tres acciones sin tarea, pero NOT_DETERMINABLE | Ambas FAIL de estado |

D02baseline comienza «Redactar una tarea», pero los bullets siguientes sí entregan objetivo, criterio provisional, output con sensor/timestamp/valor/motivo, dependencias y límites. Se acepta ese contenido distribuido: la rúbrica no exige heading o key específica. Es un juicio de frontera que queda documentado. Aun si una revisión más estricta lo rechazara, D02treatment seguiría sin cumplimiento conjunto por formato y D04 seguiría fallando; no aparecería señal favorable completa.

D01treatment tiene `task_draft`, pero el nombre del campo no suple los outputs futuros y criterios faltantes. D03treatment cumple en strings de `proposed_actions` sin necesitar ese campo. Esto evita puntuar por estructura o palabras aisladas.

D04 marca indeterminación del trabajo posterior aunque el encargo actual permite preparar seguimiento; el contrato común define READY por preparación dentro del mandato. Ambas ramas sí entregan las tres acciones: hay clasificación restrictiva de estado, no rechazo operativo a entregar seguimiento. No se atribuye una nueva regresión exclusiva al treatment.

La regla exige al menos dos mejoras conjuntas en los tres casos de draft, ninguna regresión y contenido PASS en ambas ramas del control. Solo mejora D03, D02 pierde cumplimiento conjunto y D04 falla ambas. Resultado: **COMPLETED_MIXED_NO_FAVORABLE_SIGNAL**. No se cambiaron expected, fixtures ni regla tras outputs, ni se identificó defecto de preparación que justificase excluir un par.

## Límites y observaciones adicionales

Revisión manual del autor, no independiente ni ciega. Las citas y juicios por obligación se conservan en semantic-review.json. Cuatro contextos/datos sintéticos, una repetición por condición; no muestra representativa ni comparación estadística de variación. Estos cuatro casos ya fueron expuestos al runtime y no deben llamarse inéditos en otra ronda.

No se observaron acuerdos inventados, ejecución prohibida afirmada ni gate aceptado. Se anotaron coordinaciones adicionales: reviewers/rutas y, en RAG, acceso a tickets privado agrupado como dependencia de ejecución aun cuando una evaluación de muestra pudiera no requerirlo. No se interpreta como permiso concedido ni bloqueo de redacción.

## Coste y evidencia

- Ronda02: **US$0.01455995** estimados por usage.
- Ronda01 fallida:US$0.000241; total task-draft-01: **US$0.01480095**, bajo el límite acumulado autorizadoUS$0.10.
- Todos los estudios de workflow anteriores más este: **US$0.05633583**. Este acumulado no incluye otros pilotos/validaciones Windows.
- Costes estimados, no factura ni impuestos. El ledger conserva floats originales; el summary redondea a12 decimales para eliminar ruido de representación, sin reescribir entradas.
- Integridad:501 archivos anteriores intactos; freeze63 archivos de ronda02, manifest SHA256 `e94a9c45115b6b45bccfa2b1f90a7bcaaf5ed343b17c9ab2628ebf222bb251c1`. Hashes locales, sin anclaje externo.
- Nueve payloads coinciden con las fuentes congeladas, raw preservado y secreto exacto ausente de evidencia. No nueva suite de tests. Producto y Foundry sin cambios ni promociones.

`round-status.json` conserva el fin de colección; `evaluation-summary.json` y `semantic-review.json` son el registro de la revisión posterior. Configuraciones y aprobación de preparación históricas permanecen intactas.

## Siguiente paso recomendado

Cerrar esta ronda sin nuevas llamadas. Diseñar un ajuste local acotado para: (1) entregar al menos un output futuro con contenido y criterios observables, (2) respetar todos los headings Markdown, (3) referir el estado a la acción solicitada y separar permisos de trabajo posterior. Revisar ejemplos completos y contraejemplos antes de cambiar pautas o pagar otra evaluación. El problema actual es la calidad del encargo/contrato entregado; esta evidencia no evalúa eficacia de las capacidades del Foundry.

Cualquier diseño/código/nueva ronda se acuerda por separado; el saldo no autoriza invocaciones adicionales.
