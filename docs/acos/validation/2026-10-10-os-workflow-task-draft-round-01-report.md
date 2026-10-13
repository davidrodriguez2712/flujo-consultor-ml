# Task concreto — ronda01 detenida en smoke

## Estado actual

David aprobó paquete, configuración y hasta US$0.10 adicionales mediante «aprobado». La ronda se detuvo conforme al protocolo: el único smoke recibió respuesta válida del runtime, pero incumplió el contrato Markdown. No se enviaron los ocho casos; la eficacia del tratamiento sigue **NOT_EVALUATED**.

Los estados PENDING de los documentos congelados describen su preparación histórica. Las aprobaciones posteriores están en `review-approval.json` y `budget-approval.json`; el estado de esta ejecución está en `runs/round-01/evaluation-summary.json`.

## Ejecución y coste

- Preflight: manifests, snapshots, CLI 2.1.296 y flags conformes. Intento inicial sin API detenido porque el sandbox impide abrir localhost; conservado como `preflight-local-01`. La ejecución escalada permitió el proxy local aprobado.
- Una solicitud a Claude Haiku 5.5, HTTP200, `end_turn`, usage conocido y runtime exitoso; sin reintentos ni rechazos del proxy.
- Coste estimado por usage: **US$0.000241**. Coste anterior de estos estudios: US$0.04153488; acumulado: **US$0.04177588**. Son estimaciones de API, no factura/impuestos.
- Ocho respuestas del benchmark pendientes; ninguno de sus inputs se envió al modelo en esta ronda.

## Fallo observado

El raw empieza con `READY` y una explicación antes de `## Estado`. El contrato exige empezar por los cinco H2 en orden y poner READY como primera línea del cuerpo de Estado. Además, ese cuerpo contiene prosa sin un status válido. El checker0.2.0 lo rechaza correctamente. No se reparó la respuesta ni se modificaron checker, expected o protocolo para hacerla pasar.

Una llamada demuestra este incumplimiento específico, no una causa general ni que otra redacción lo resuelva. No hay comparación baseline/treatment ni resultados semánticos del benchmark.

## Evidencia y verificación

- Raw, metadata, payload, ledger, diagnóstico, aprobaciones e intento local conservados.
- Integridad PASS:421 archivos históricos,39 de preparación y12 de configuración. Freeze de esta ejecución:17 archivos, manifest SHA256 `bb39f208bc6287a153e4202c8b102687a63c0e2a33f9306e500e6ce1f08183fc`.
- Se comprobó ausencia del secreto exacto en los archivos de la ejecución, sin imprimir/copiar/hash de la credencial. Los hashes son control local, sin anclaje externo.
- No se ejecutó otra suite de tests ni se modificó producto o Foundry. Revisión del autor, no independiente ni ciega.

## Siguiente propuesta concreta

Revisar `evaluations/os-workflow/2026-10-09-task-draft-01/proposed-smoke-02.txt`: incluye una plantilla literal que empieza por `## Estado` y sitúa READY debajo. Es solo una propuesta local **no ejecutada**; no evalúa razonamiento de negocio. Mantener los ocho casos, condiciones, expected y rúbrica intactos, y el mismo prompt neutral en sus invocaciones.

Si se aprueba, preparar y congelar una configuración02 con ese único cambio y nueva ronda manual, conservando esta ronda fallida. Recomiendo mantener un límite acumulado de **US$0.10 entre ambas rondas de este estudio**: quedarían como máximo US$0.099759 para un nuevo smoke + ocho respuestas, sin reintentos. Se debe vincular ese límite acumulado al nuevo manifest antes de cualquier llamada; no basta con reutilizar la aprobación de configuración01 ni el saldo.

No hay llamadas adicionales autorizadas tras esta parada.
