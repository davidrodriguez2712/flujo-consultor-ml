# Checker, pricing y borrador de task — ajustes locales

## Estado

**IMPLEMENTED_LOCALLY_VERIFIED**, eficacia de agentes pendiente. David aprueba los tres ajustes mediante «aprobado». Cero llamadas API, US$0 adicionales. Acumulado de los dos estudios anteriores US$0.04153488 estimados; autorización de llamadas anterior concluida.

## Cambios

### Checker Markdown0.2.0

Primera línea no vacía de Estado debe ser status válido; se permite explicación posterior. Rechaza otro status declarado en línea separada, duplicado o distinto, así como prefacios, fences envolventes y estructura incorrecta. La contradicción dentro de prosa requiere revisión semántica, no queda resuelta por formato. Énfasis se interpreta sin reescribir raw. JSON conserva checker original.

TDD: tres tests de explicación fallan antes, después35tests focalizados PASS. Siete tests nuevos incluyen rechazos de status repetido/contradictorio y CLI que conserva el archivo. No reejecutar checker actualizado sobre respuestas anteriores para convertir sus scores: snapshot0.1.0 y resultados permanecen intactos.

### Fixture P02-v02 corregido

Se documentan precio/cantidad/coste y recálculo de ingresos:

|Dato|Base|Escenario|
|---|---:|---:|
|Cantidad|1000|1000|
|Precio unitario|100|120|
|Coste unitario|75|75|
|Ingresos|100000|120000|
|Coste de bienes|75000|75000|
|Beneficio bruto|25000|45000|
|Margen bruto|25%|37,5%|

Diferencia12,5pp. Volumen/coste fijo por construcción, sin elasticidad ni efecto observado. Verificación aritmética PASS. Contrato Markdown ahora explicita primera línea y explicación posterior. Es corrección de pricing expuesto, **no caso inédito**, ni simulación de un agente. Expected anterior sin cambios; expected de versión nueva separado, aún sin ejecución aprobada.

### Borrador concreto de tarea

Workflow, template y MANUAL exigen entregar tarea redactada cuando se pide borrador: objetivo, inputs, outputs propuestos con contenido mínimo, criterios observables de revisión y dependencias. No sustituir por instrucciones para redactar después. Pendientes y propuestas explícitos; sin owners/fechas/permisos/gates inventados. JSON incorpora borrador en campos permitidos, sin anexar Markdown externo. Template añade Outputs propuestos; no cambia schema de profile/state ni comandos.

[Ejemplo redactado por el autor](../../../evaluations/os-workflow/2026-10-09-local-refinement-02/examples/task-commercial-coverage.md) sobre fixture de crédito: outputs de informe de cobertura y registro de preguntas, ambos propuestos, criterios/reviewer pendientes y acciones dependientes bloqueadas. No respuesta de agente ni aprobación real.

## Verificación y distribución

Suite completa **189passed**, sin failures/skips,5,49s con proveedores simulados; no API. Proyecto temporal compilado sin Foundry: template generado igual al canónico, source/bundle exactos. `acos status`/`next` exit0; `validate` exit3NEEDS_REVIEW esperado, sin aceptación automática. Manual y template generados conservados para revisión del autor; no test de prosa ni evidencia de eficacia.

Integridad de **402 archivos históricos** PASS. Siete archivos modificados congelados en snapshot, junto a fixtures/revisión/checks. Paquetes, experimentos y proyectos históricos no actualizados. No publicación de release ni cambios/promociones del Foundry. La configuración pagada anterior fija snapshots0.1.0; no debe reutilizarse como autorización para ejecutar código0.2.0.

[Paquete](../../../evaluations/os-workflow/2026-10-09-local-refinement-02/README.md) · [Checks](../../../evaluations/os-workflow/2026-10-09-local-refinement-02/local-checks.json) · [MANUAL generado](../../../evaluations/os-workflow/2026-10-09-local-refinement-02/generated-MANUAL.md).

Freeze de **19 archivos**, SHA-256 `61f945d10b10ae6a215903279d60195993d89f988bab0a0c3d8091ae67ebf3f3`. [Manifest](../../../evaluations/os-workflow/2026-10-09-local-refinement-02/change-manifest-02.json).

## Pendientes

Medir si las pautas producen borradores concretos mediante casos nuevos, con rúbrica/configuración congeladas antes de outputs. Diseñar cobertura Markdown que separe formato de contenido con supuestos claros. Reutilizar P02-v02 solo como regresión expuesta, no prueba de transferencia inédita. Preparación y presupuesto nuevos antes de calls; no gastar saldo remanente por existir. La revisión local del autor no acredita independencia ni eficacia general.
