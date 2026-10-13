# Decision memo — riesgo de crédito sintético

**Versión:** 0.1.0 · **Fecha:** 2026-10-08 · **Owner/reviewer:** David  
**Audiencia:** revisión interna del piloto · **Estado:** preparado para aprobar Delivery.

## Decisión recomendada

Conservar el prototipo y su evidencia como resultado de laboratorio. La evidencia actual permite evaluar riesgo en la población histórica de créditos concedidos; la decisión de priorizar revisión de todas las solicitudes queda **parcialmente respondida**.

El siguiente trabajo debe definir una política de revisión aplicable al llegar solicitudes y cómo medir sus resultados. Este paquete no autoriza automatizar concesión/rechazo, desplegar una política real ni atribuir ahorro a la revisión.

## Qué sabemos

El fixture contiene 7.200 solicitudes sintéticas en 24 meses. Se entrenó una regresión logística L2 con cinco features disponibles al scoring, transformaciones solo en train y configuración fija. El refit final usó 2.140 solicitudes y labels disponibles al 2025-07-01. Se puntuaron 900 solicitudes de julio–septiembre y se evaluaron 447 créditos concedidos con outcomes maduros al 2026-01-15.

| Resultado final — concedidas maduras | Modelo | Referencia constante |
|---|---:|---:|
| Brier score, menor es mejor | 0,102487 | 0,116530 |
| ROC-AUC | 0,752283 | 0,500000 |

La diferencia de Brier es 0,014043: mejora puntual en las mismas filas del fixture. El Brier también mejora frente a la referencia en los tres meses y en clientes conocidos/nuevos respecto del train. No se probó significancia ni generalización a datos reales. La referencia se estimó en train, sin usar la tasa de evaluation.

Fuentes: [summary final](../analysis/outputs/baseline-final/summary.json), [results](../analysis/outputs/baseline-final/results.json) e [informe de validación](../validation/model_validation.md).

## Qué cambia al considerar todas las solicitudes

Hay 453 solicitudes rechazadas sin outcome de pago observado en el periodo final. Los Top-100 de todas las solicitudes incluyen principalmente casos sin label:

| Mes | Solicitudes | Seleccionadas | Outcomes observados entre seleccionadas | Coverage |
|---|---:|---:|---:|---:|
| Julio | 300 | 100 | 26 | 26 % |
| Agosto | 300 | 100 | 22 | 22 % |
| Septiembre | 300 | 100 | 26 | 26 % |

Precision, Recall y Lift de estas listas no están identificados. Las métricas del ranking limitado a concedidas maduras no se transfieren al ranking de todas las solicitudes. Un rechazo no representa target negativo; si no se concedió el crédito, el outcome de mora de ese préstamo no está observado.

Además, el Top-K mensual se conoce al cerrar el mes. No reproduce revisar cada solicitud antes de aprobar/desembolsar con presupuesto restante. El score predice una asociación en la población seleccionada; mayor riesgo no demuestra mayor beneficio de revisar.

## Calibración y límites

La media de score es 0,126957 frente a una tasa observada de 0,134228. Esa cercanía global no certifica calibración: el bin 0,2–0,4 presenta media 0,269492 y tasa 0,345455 en 55 solicitudes; los bins altos tienen 14, 4 y 0 filas. En clientes nuevos, media 0,151913 frente a tasa 0,186992. Mantener esos desajustes visibles; no recalibrar usando el holdout ya observado.

Toda la evidencia es sintética y el autor podía acceder al raw y generator; no fue una evaluación ciega. No hubo tuning posterior a final, nuevas llamadas a APIs ni promoción de skills. El impacto causal de revisión y el ahorro no están identificados.

## Siguiente paso propuesto

| Acción | Responsable propuesto | Output antes de decidir |
|---|---|---|
| Definir momento de revisión y cómo distribuir la capacidad conforme llegan solicitudes | David con el owner de negocio que se designe | Contrato de decisión y política online explícita |
| Definir población, exposición y outcome realmente observables | Owner de datos/negocio por designar | Contrato de datos y límites de identificabilidad; sin inventar labels de rechazadas |
| Diseñar una evaluación de la política de revisión | David con reviewers que se designen | Protocolo con comparador, métricas y supuestos antes de ejecutarlo |
| Evaluar una nueva versión con datos independientes | Owner técnico por designar | Validación temporal/calibración, costos y evidencia de operabilidad |

Estos responsables son propuestas, no personas asignadas ni instrucciones enviadas. Obtener datos de originación/outcomes de créditos concedidos no resuelve por sí solo el riesgo contrafactual de solicitudes rechazadas. Habrá que definir qué pregunta es identificable y qué supuestos requiere.

## Aceptación solicitada

Aprobar este memo y el paquete local de Delivery como conclusión del piloto, conservando los límites anteriores. Después: handoff con runbook, inventario de evidencia y pendientes. La aprobación del entregable no equivale a aprobar una política crediticia real.
