# Review exploratoria — selección operacional

Fecha: 2026-10-07. Reviewer: asistente que preparó la prueba; no independiente. Tratamiento documental local, no skill nativa ni experimento canónico del Foundry.

## Resultado

Cuatro cases y ocho ejecuciones válidas. El baseline recibió el playbook actual experiments-and-models; treatment recibió exactamente ese playbook más selection-supplement-v0.1.md. El baseline resolvió selección ordenada, capacidad, métricas, decisión estructurada y autoridad en los cuatro cases. El suplemento no mostró mejora y produjo dos diferencias desfavorables en campos de salida.

| Check, por case | Baseline | Treatment |
|---|---:|---:|
| Selección en orden requerido | 4/4 | 3/4 |
| Miembros seleccionados | 4/4 | 4/4 |
| K efectivo | 4/4 | 4/4 |
| Métricas numéricas o null según identificación | 4/4 | 4/4 |
| Campo decision | 4/4 | 3/4 |
| Gate NEEDS_REVIEW | 4/4 | 4/4 |

No se suman checks en un score compuesto. Una ejecución por condición/case no demuestra superioridad general ni frecuencia de fallos.

## Casos y hallazgos

### A — Capacidad y empates

Ambos eligieron [A,B] con K=2, preservando empate por ID antes de labels. Precision=0,5, Recall=0,5, Lift=1. No escogieron [A,C] para mejorar retrospectivamente métricas. Ambos advierten fragilidad de los empates.

### B — Contactos repetidos y capacidad sin llenar

Ambos excluyeron A/D por cooldown y seleccionaron [B,C]. K efectivo=2 aunque capacidad=3; no rellenaron con excluidos. Métricas sobre elegibles: Precision=0,5, Recall=1, Lift=1. Reconocen que seleccionar toda la población elegible hace trivial el recall y lift; no confunden la población original de cuatro con la elegible de dos.

### C — Labels solo de inspeccionados

Ambos conservaron null para métricas de población/selección completa, sin convertir outcomes ausentes en negativos. Explicaron cobertura 50% de población y de seleccionados. Miembros elegidos correctos: U1 y H1.

El treatment devolvió [H1,U1], orden alfabético. Su propio rationale reconoce scores U1=0,99 y H1=0,80 y el top-2 correcto, pero cambia la presentación a orden por ID aunque no hay empate. El expected conserva [U1,H1] según score descendente. Es un fallo de orden del contrato, no un cambio de miembros ni un error en el K=2; sí importaría si un consumidor actuara por prefijos del ranking. No se modificó criterio ni se reintentó.

Baseline añadió cotas lógicas para outcomes binarios ausentes: P en [0,5;1], Recall en [0,5;1], Lift en [1;2]. Sus cuatro combinaciones de U1/U2 son aritméticamente consistentes. Las distingue de estimaciones poblacionales y no las usa para afirmar representatividad. El mecanismo de inspección no se conoce; las frases de ambos outputs que lo llaman probablemente dependiente del score se tratan como hipótesis, no evidencia.

### D — Riesgo frente a beneficio causal

Ambos seleccionaron [A,B] y calcularon Precision=0,5, Recall=0,5 y Lift=0,75. Ambos explicaron que no pueden identificar clientes salvados, ROI o campaña óptima con riesgo bajo política actual y sin efecto incremental.

Baseline devolvió decision=causal_not_identifiable como esperado para la pregunta de negocio. Treatment devolvió ranking_only, aunque su rationale dice que la decisión causal no es identificable. Es una inconsistencia del campo estructurado con la respuesta de negocio, no una afirmación de efecto causal demostrado. El esquema une tipo de output con identificación causal; para una próxima prueba convendría separarlos y definir inequívocamente el propósito del campo. Los expected originales se conservan.

## Otras limitaciones

Las ocho respuestas incluyen fences de JSON pese a pedir JSON puro. El checker extrae el payload y reporta esa diferencia de formato para ambas ramas. Los outputs hacen varias preguntas sobre condiciones ya fijadas y contienen afirmaciones amplias sobre no poder estimar incertidumbre por n pequeño; no se requerían intervalos y esas frases no son una evaluación estadística independiente. La prueba verifica aritmética y límites de identificación, no calibración ni significancia.

## Tiempo y coste observados

| Condición | Tiempo acumulado | Coste reportado CLI |
|---|---:|---:|
| Baseline | 52,46 s | USD 0,122268 |
| Treatment | 83,10 s | USD 0,123574 |

Claude-sonnet-5-5, effort medium, contextos separados, sin herramientas/MCP ni persistencia. La latencia de treatment B fue 47,90 s; no se atribuye a la pauta sin repetir ni controlar servicio/cache. No hay ahorro o eficiencia general demostrados.

## Integridad

Inputs, expected, playbook y suplemento congelados antes de ejecutar. Solo cambia suplemento. Ocho session_id distintos, mismos modelo/configuración y orden alternado. Expected fuera de prompts. Outputs íntegros sin ajustes ni selección favorable. No se reentrenó ni se usó el test de churn; el laboratorio permanece cerrado e intacto.

## Recomendación

Mantener evaluate-operational-selection como conocimiento y conservar el playbook actual. No crear skill ni ampliar un gate canónico por esta ronda: no aparece un fallo del baseline en capacidad, empates, labels parciales o límites causales. La pauta adicional no justifica adopción con esta evidencia.

Registrar los dos fallos de representación del treatment como hipótesis para contratos de output: ordenar listas según el criterio de negocio y separar ranking de identificabilidad causal. Una revisión posterior necesitaría casos más amplios y reviewer independiente; no se promueve ni modifica el Foundry.
