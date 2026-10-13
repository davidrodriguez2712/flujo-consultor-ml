# TASK — borrador de evaluación de cobertura comercial

**Ejemplo redactado por el autor sobre el fixture T05; no respuesta de agente ni acuerdo aprobado.**

- Estado: BORRADOR, permitido preparar; ejecución pendiente.
- Owner, ejecutor, reviewer y fecha: pendientes de asignación; no inventar nombres ni fechas.
- Decisión que informa: determinar qué información falta para evaluar una posible ampliación del score desde originación digital a cartera comercial.
- Objetivo propuesto: describir cobertura y carencias de datos para esa evaluación; no entrenar ni desplegar un modelo.

## Inputs conocidos

- `requests/task-draft.json`: encargo y dos dependencias pendientes del fixture.
- `reports/frozen-01/plan.md`, `reports/manifest-01.json` y `reports/approval-01.json`: alcance histórico de originación digital; conservarlo.
- `analysis/plan.md`: propuesta viva; no aceptación del nuevo alcance.
- Datos comerciales, definición de población, variables requeridas, KPI y ventana: pendientes de acuerdo y acceso autorizado.

## Outputs propuestos, pendientes de acuerdo

1. Informe de cobertura: fuentes autorizadas, población/ventana acordadas, variables disponibles frente a las requeridas, faltantes y límites. Identificar cada conclusión con su fuente. Formato y ruta final pendientes de acuerdo; no presumir write scope.
2. Registro de preguntas y decisión de viabilidad: qué puede evaluarse, qué información falta y qué acceso o definición necesita resolver el owner. Sin declarar viabilidad confirmada antes del análisis.

## Criterios de revisión propuestos

- El informe identifica población, ventana, fuentes y definiciones acordadas; distingue confirmado de pendiente.
- Cada conclusión de cobertura tiene evidencia; no inventa métricas, umbrales ni datos.
- El registro enumera faltantes y acciones para resolverlos, y permite al reviewer decidir si puede comenzar la siguiente tarea.
- La propuesta no modifica el freeze histórico, no extiende su aceptación a comercial y no aprueba gates.
- Reviewer y forma de aceptación: pendientes de asignación/acuerdo; revisión humana antes de dar por aceptados los outputs.

## Dependencias de ejecución

- Aprobación del nuevo alcance: pendiente; impide evaluar cartera comercial, no redactar este borrador.
- Acceso autorizado a datos comerciales: pendiente; impide consultar/procesar esos datos.
- Definir población, variables requeridas, KPI, ventana y write scope antes de ejecutar sus acciones dependientes; este borrador propone acordarlos, no afirma que estén aprobados.

## Límites y siguiente paso

Entregar este borrador al owner para acordar outputs, definiciones y responsables, y resolver las dos dependencias. No ejecutar análisis, consultar datos comerciales, congelar cada edición del plan vivo ni aprobar gates por preparar esta tarea.
