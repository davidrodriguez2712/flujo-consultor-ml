# Review exploratoria — evidencia a recomendación

Fecha: 2026-10-07. Review por el asistente que preparó los cases; no independiente. Tratamiento documental local, no skill nativa ni evaluación canónica del Foundry.

## Resultado

Cuatro cases y ocho contextos distintos. Baseline conserva playbook research-impact-delivery y templates actuales findings-and-qa/delivery-and-handoff; treatment añade un template breve de memo. No se observa ventaja material del suplemento en las decisiones, cálculos o prevención de claims sin sustento evaluados.

| Comprobación | Baseline | Treatment |
|---|---:|---:|
| Campos numéricos y null requeridos correctos | 12/12 | 12/12 |
| Estados de claims coinciden literalmente con expected | 10/12 | 10/12 |
| Cases con referencias provistas y no vacías | 4/4 | 4/4 |
| Owner provisto, sin distinguir mayúsculas | 4/4 | 4/4 |
| Owner idéntico byte a byte | 1/4 | 1/4 |
| Gate NEEDS_REVIEW | 4/4 | 4/4 |

No score compuesto. El check de refs confirma existencia de IDs, no prueba soporte semántico; el contenido fue leído para esta review. Capitalizar el nombre del rol no inventó otro responsable: los mismatches exactos se conservan por separado. Tres baseline y cuatro treatment incluyen fences pese a pedir JSON puro; se parseó payload sin editar originales.

## Revisión por caso

### A — Exposición distinta de ROI

Ambos conservaron Precision@50 20%, comparador aleatorio esperado 10% y USD 120000 como MRR expuesto. Impacto incremental y ROI null, retirando 300% y recuperación garantizada. Recomendaron diseño de piloto sujeto a review, no despliegue basado en riesgo. El doble o diferencia de 10 pp respecto del azar son derivaciones descriptivas correctas, no retorno incremental.

Ambos clasificaron A1 como contradicted, mientras expected pedía unsupported: interpretaron que E2 refuta equiparar exposición con recuperación. El expected se fijó pensando que una cifra futura no puede probarse falsa con esos inputs. Es un desacuerdo semántico entre refutar la equivalencia de magnitudes y no identificar el efecto futuro; ambas respuestas rechazan correctamente usar USD 120000 como beneficio demostrado. No se cambian criterios ni se usa ese mismatch para atribuir ventaja al suplemento.

### B — Denominadores y evidencia contradictoria

Ambos calcularon Norte 40/100=40%, Sur 90/900=10%, total 130/1000=13%, no promedio simple 25%. No confundieron niveles de un período con mejora. Recomendaron mantener rollout en revisión y reunir evidencia antes de justificarlo. Las diferencias regionales de 30 pp y proporciones de exposiciones son derivaciones verificables.

Una medición previa puede informar un cambio temporal, pero no identifica por sí sola causalidad. La frase del treatment sobre reconsiderar con medición previa o experimento no constituye aquí un diseño causal validado; esa condición debe precisarse en un proyecto real. No se inventó efecto de la solución en las cifras entregadas.

### C — Efecto incierto y guardrail incumplido

Ambos conservaron estimación +1 pp e intervalo provisto [-1,3] pp, sin recalcular. Quejas 8%-2%=6 pp excede máximo autorizado 2 pp. ROI null. Recomendaron no escalar y revisión/mitigación bajo autoridad humana; no cambiaron el guardrail.

Ambos llamaron contradicted a C1, donde expected pedía unsupported, porque la fuente afirma que el aumento positivo no es concluyente. Expected distinguía ausencia de evidencia de efecto y falsedad del efecto. Aquí se discute la afirmación «está demostrado», no si el efecto real es positivo o negativo. Se conserva el mismatch; no representa que alguno haya afirmado un efecto negativo demostrado ni aporta ventaja diferencial.

Un claim del baseline sobre guardrail referencia E2 (tasas), mientras el umbral de 2 pp reside en el contexto del case. El cálculo tiene soporte en el conjunto de inputs, pero una entrega real debería vincular además el contrato de guardrails; la existencia de un ID no garantiza lineage completa de todas las condiciones.

### D — Muestra de riesgo distinta de población

Ambos mantuvieron tasa 35/100=35% para el conjunto auditado y null para tasa poblacional/ahorro anual. Rechazaron 3500 errores y USD 50000, sin imputar datos del resto. Recomendaron contrastar diseño de muestra y inputs de costes antes de extrapolar.

Los 9900 expedientes restantes y 1% auditado son derivados de los conteos provistos. Ambos outputs sugieren posible sesgo al alza; selección de riesgo no demuestra su dirección ni magnitud en estos datos. Debe tratarse como hipótesis, no finding confirmado. No se hizo una estimación numérica poblacional basada en esa hipótesis.

## Límites de la prueba

Fuentes ficticias breves, claims problemáticos señalados y esquema de respuesta explícito: tarea acotada con fuerte estructura. No evalúa discovery, búsqueda externa, documentación larga, presión de negocio real ni consistencia repetida. No demuestra que el playbook funcione siempre ni que un template nunca aporte valor.

Las dos condiciones formularon condiciones de cambio y siguientes pasos, sin plazos/presupuesto inventados ni envío/publicación. Ninguna asumió autoridad para aprobar gates. Algunas limitaciones piden datos de período o capacidad pese a contexto provisto; no se considera precisión perfecta de lectura.

## Tiempo y coste observados

| Condición | Tiempo acumulado, cuatro calls | Coste reportado CLI |
|---|---:|---:|
| Baseline | 51,13 s | USD 0,139010 |
| Treatment | 48,78 s | USD 0,144640 |

Claude-sonnet-5-5 effort medium. Una ejecución por condición/case; no significancia ni ahorro demostrado. La variación del servicio y respuesta puede influir. Ocho sesiones nuevas sin herramientas/MCP ni persistencia, con orden alternado; expected no se incluyó en payload. Inputs y criterios conservan hashes previos.

## Recomendación

Mantener synthesize-evidence-to-recommendation como conocimiento/playbook/template, respetando la decisión canónica previa. No crear otra skill, adoptar el suplemento como mejora demostrada ni promover madurez. Las pautas actuales resolvieron las decisiones principales de los cuatro casos.

Registrar dos aprendizajes para contratos futuros: diferenciar soporte de una afirmación sobre el efecto frente a una afirmación sobre certeza; vincular claims derivados también con contratos/umbrales, no solo con tabla de tasas. El traslado al Foundry y cualquier cambio requieren su revisión; no se modificó Foundry ni el piloto cerrado.
