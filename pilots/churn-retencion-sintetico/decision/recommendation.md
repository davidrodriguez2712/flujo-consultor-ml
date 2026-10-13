# Decision memo — Priorización de churn

**Proyecto:** piloto sintético de churn y retención.  
**Fecha:** 2026-10-07.  
**Audiencia:** responsable ficticio de retención y equipo analítico.  
**Reviewer:** David Rodríguez.  
**Estado:** propuesta para revisión de delivery; entrega local de laboratorio.

## Decisión propuesta

Aceptar el ranking como resultado analítico del laboratorio y como referencia para un futuro piloto con datos reales. Antes de justificar una campaña o inversión, validar disponibilidad de datos y desempeño en el contexto real, definir la intervención y comprobar su efecto incremental.

La decisión original es a quién priorizar, con capacidad de 50 revisiones mensuales. La evidencia disponible permite describir cómo el baseline ordena el riesgo en este fixture y revisar el flujo ACOS hasta validation, ya aprobado. Aún falta aprobar delivery y completar handoff para cerrar el piloto de punta a punta.

## Evidencia principal

Modelo por grupos con cuatro señales históricas: actividad de los dos meses previos, pagos fallidos y tickets. Imputación y tasas aprendidas solo del train; modelo final fijo al 1 de julio de 2025, sin reentrenamiento ni tuning en el holdout.

| Métrica, media mensual | Desarrollo, 9 meses | Holdout, 6 meses | Aleatorio esperado en holdout |
|---|---:|---:|---:|
| Precision@50 | 13,56% | 10,67% | 4,28% |
| Recall@50 | 10,74% | 11,02% | 4,40% |
| Lift@50 | 3,49 | 2,52 | 1,00 |

En julio–diciembre de 2025: 6.860 observaciones cliente-mes y 292 cancelaciones; 300 selecciones cliente-mes contienen 32 positivos. Son selecciones de riesgo, no contactos ejecutados ni clientes retenidos. Las entidades pueden repetirse entre meses.

Con 50 selecciones por mes, el baseline incluye más cancelaciones que la expectativa analítica aleatoria en este caso. Precision mensual varía de 6% a 16%; Recall medio de 11,02% deja la mayoría de cancelaciones fuera del top 50. La capacidad limitada y la incertidumbre deben formar parte de la decisión.

Fuentes: [evaluación final](../validation/model_validation.md), [resultados por mes](../analysis/outputs/holdout-final/results.json), [auditoría](../analysis/outputs/holdout-audit.json) y [especificación del baseline](../modeling/model_brief.md). Las medias son macro por mes; el lift medio no es el cociente de precisiones medias.

## Opciones consideradas

| Opción | Qué permite | Límite | Recomendación |
|---|---|---|---|
| Selección aleatoria de 50 | Referencia simple con expectativa Precision 4,28% | No aprovecha señales del fixture | Conservar como comparación |
| Ranking congelado de 50 | Priorizar riesgo con Precision media 10,67% en el fixture | No estima respuesta a contacto | Aceptar como baseline del laboratorio |
| Desplegar una campaña con el modelo | Exigiría medir resultados operacionales | Faltan datos reales, intervención y evaluación incremental | Proponer un piloto real separado, antes de inversión o despliegue |

## Interpretación y límites

- Datos 100% sintéticos: las relaciones provienen del generador; no representan resultados de un cliente real.
- La Precision cae 2,89 puntos respecto de desarrollo. No hay causa demostrada: cambian meses, prevalencia y población, y el protocolo del holdout usa modelo fijo mientras desarrollo reentrena por fold.
- No hay evidencia de calibración, significancia estadística, readiness de producción ni desempeño en clientes nuevos; no entran altas después de junio de 2024.
- No existe tratamiento/control: riesgo alto no implica mayor beneficio de contactar. No se estima uplift, retención incremental, ROI, margen recuperado o ahorro.
- MRR representa exposición descriptiva, no beneficio realizable. No se usa para seleccionar el ranking.
- Empates resueltos por customer_id ascendente; ID no determina el score. No se probó otra regla después de ver labels.
- El holdout ya está observado. Cambios motivados por sus resultados necesitan otra reserva y un protocolo nuevo para evaluar mejoras.
- El mismo asistente construyó y auditó el trabajo; la aprobación humana del laboratorio no sustituye review técnico independiente.

## Próximos pasos propuestos

1. Revisar este memo y el [contrato de entrega](../delivery/delivery_contract.md) mediante el gate delivery.
2. Tras aprobación, completar handoff: runbook, rutas de evidencia, reproducción y pendientes.
3. Para un proyecto real separado: definir owner operacional, datos históricos, consentimientos/contactabilidad, costes y reglas de supresión; confirmar timestamps y target con negocio.
4. Establecer un protocolo nuevo y datos de evaluación reservados. Comparar con la política vigente y medir capacidad, estabilidad y criterios de negocio previamente acordados.
5. Diseñar una evaluación de la intervención cuando existan las condiciones y autorización; cuantificar valor incremental solo con evidencia pertinente.

Estas propuestas no crean compromisos de plazo, presupuesto ni permisos externos. El paquete permanece local; no hay campaña, publicación ni modificación del Foundry autorizada por este memo.
