# Estado del piloto — 2026-10-07

## Completado

- Workspace compilado mediante `acos init` con ambas rutas de runtime y tres snapshots experimental: understand-dataset, design-validation y detect-leakage, versión 0.1.0.
- Datos de suscripciones 100% sintéticos: 2.400 clientes, 35.990 snapshots, 35.990 labels y 11.804 tickets; 24 meses entre febrero de 2024 y enero de 2026.
- 35.018 labels observadas, 1.428 positivos (4,08%) y 972 pendientes. Las pendientes no se rellenan con cero.
- Generador portable con biblioteca estándar; CSV reproducidos idénticos byte a byte y SHA-256 comprobados.
- Checks de claves, disponibilidad, alta y joins. El join directo de tickets crearía 36.853 filas frente a 35.990 snapshots; hay que agregar antes de unir.
- Primera versión del generador tenía inconsistencias previas al alta. Se corrigieron, se ejecutaron checks de regresión y se archivó v0 para trazabilidad; no usarla.
- Primera comparación exploratoria de design-validation, con baseline/treatment y criterios fijados previamente. Misma tarea, modelo e inputs; contextos independientes y solo lectura.
- `acos status` y `acos next`: exit 0. `acos validate`: exit 3, NEEDS_REVIEW esperado para discovery. Comandos sin escritura; integridad de snapshots preservada.
- Suite del producto repetida: 92 passed en 2,19 s.

## Resultado de la comparación

Ambos outputs cubren los riesgos principales. El treatment es más cuidadoso con la separación por entidades y con no inventar conteos por período, pero ambos explican mal una parte del calendario de maduración. El baseline propone un mínimo de meses de entrenamiento incompatible con su primer fold. Se comprobaron los puntos contra las labels generadas y se documentaron correcciones separadas de los outputs originales.

**No hay evidencia suficiente de mejora consistente en un solo caso.** La review no es independiente. La skill sigue experimental; no se modificó Foundry. [Review y evidencia](evaluation/design-validation/review.md).

## Estado vigente

COMPLETED. David aprobó handoff y cierre; siete etapas y doce gates registrados con evidencia. [Balance final](handoff/closure.md) y [runbook](handoff/runbook.md). Holdout sintético: Precision@50 10,67%, Recall@50 11,02%, Lift@50 2,52. No se demostró campaña, ROI o generalización real; Foundry sin modificaciones ni promociones.

Las actualizaciones siguientes conservan la historia y no sustituyen este estado vigente ni .acos/state.yaml.

## Contexto y framing aceptados; diagnóstico pendiente

Propuesta del laboratorio:

- Empresa ficticia de suscripciones.
- Decisión: priorizar clientes activos para revisión de retención mensual.
- Capacidad: 50 contactos/mes.
- Churn: cancelación durante el mes calendario que comienza al scoring; label disponible al comenzar el mes siguiente + 7 días.
- KPI analítico: Precision@50 y Recall@50 por mes; MRR en riesgo como contexto, no como recupero incremental.
- Entregable: informe analítico y decision memo del piloto.
- Reviewer: David Rodríguez.

Revisar [contexto](context/business_context.md) y [manual](MANUAL.md). Discovery ya fue aprobado; evidencia en evidence/approvals/2026-10-07-discovery.md. Revisar ahora reports/dataset, reports/leakage y data/data_contract.yaml antes de aprobar diagnosis/data-quality. Si se cambian hechos del perfil confirmado, V1 exige revisar/recompilar un workspace nuevo; no editar hashes para forzar PASS.

## Siguientes pasos

1. Discovery cerrado tras aceptación humana del contexto y supuestos.
2. Framing y diseño temporal aceptados; diagnóstico v2 preparado para revisión.
3. Producir un baseline analítico reproducible y evaluar el ranking en períodos posteriores, con labels disponibles en cada fecha.
4. Revisar calidad de los outputs, continuidad y feedback de capacidades; ampliar comparación y review independiente si se desea evidencia Foundry.
5. Entregar decision memo con límites sintéticos. Un piloto con datos reales será otro contexto de evaluación.

## Actualización: discovery aprobado

David aceptó el contexto y las definiciones presentadas. Discovery validado PASS y estado avanzado a framing. Contrato y diseño corregido preparados para revisión; no se aprobó otra etapa ni se entrenó un modelo.

## Actualización: diagnóstico preparado

Framing/protocolo aprobados y estado avanzado a diagnosis. V2 del generador corrige un evento fuera del corte; 26 checks sin infracciones. Reports de comprensión y leakage listos para revisar, sin entrenamiento ni métricas de test.

## Actualización: diagnosis aprobado y baseline ejecutado

David aprobó diagnosis/data-quality; ambos gates validados PASS antes de avanzar. Nueve folds ejecutados; ocho tests pasan y cinco JSON reproducidos idénticos. Datos v2 y protocolo sin cambios. Pipeline auditado mediante aplicación manual de pautas detect-leakage; revisión no independiente. Modelo final de 26.839 filas congelado al 1 de julio. Gate execution pendiente; holdout aún no evaluado. Ningún estado del Foundry se ha promovido.

Siguiente paso vigente: revisar execution, evaluar holdout tras aprobación, completar validation, decision memo, delivery y handoff.

## Actualización: execution aprobado y holdout evaluado

Aprobación humana registrada y execution validado PASS antes de avanzar. Modelo de 26.839 filas fijo al 1 de julio utilizado en seis meses, sin refit ni tuning. Resultados y scores preservados; nueve checks globales y recálculos por mes correctos. Precision menor que desarrollo, sin causa atribuida ni significancia afirmada. El holdout ya está observado. Revisión de validation y módulos pendiente, seguida de delivery/handoff. No se modificó Foundry.

## Actualización: validation aprobado y delivery preparado

David aprobó evaluación y límites incluyendo cuatro gates de módulos. Los cinco gates se comprobaron PASS antes de avanzar a delivery. Memo propone baseline de laboratorio y piloto real separado; contrato documenta archivos y criterios de aceptación. Inventario SHA-256 del subconjunto de evidencia listo para review. Delivery y handoff requieren sus propias revisiones; no se publicó ni se modificó Foundry.

## Actualización: delivery aprobado y handoff preparado

David aprobó memo y contrato para continuar; delivery validado PASS antes de avanzar. Runbook documenta uso, reproducción, integridad, test observado y responsables/pendientes. Feedback separa aplicación manual de skills y comparación exploratoria; sin promoción ni cambios Foundry. Handoff requiere revisión propia antes de declarar cierre.

## Actualización: handoff aprobado y laboratorio cerrado

David respondió «aprobaod seguimos» a la solicitud de aprobar handoff para cerrar. Handoff validado PASS antes de declarar COMPLETED. State y vistas actualizados; inventario previo conservado y revisión de cierre separada. Las propuestas posteriores se registran como iniciativas distintas, sin atribuir eficacia de skills al cierre del laboratorio.
