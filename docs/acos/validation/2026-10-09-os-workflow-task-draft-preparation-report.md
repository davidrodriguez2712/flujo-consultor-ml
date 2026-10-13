# Task concreto — cuatro casos preparados

## Estado

**PREPARED_PENDING_PACKAGE_REVIEW**. David aprueba diseño mediante «aprobado». Cuatro fixtures sintéticos y ocho payloads preparados, checks locales PASS; sin agente evaluado invocado ni llamadas API. No resultados de eficacia.

## Casos y contraste

|ID|Encargo|Formato|Datos/decisiones pendientes|
|---|---|---|---|
|D01|Borrador para evaluación retrospectiva de forecast de ventas|JSON|Raw, ventana, métrica/threshold, owner nominal y fecha.|
|D02|Borrador de revisión exploratoria de sensores sin labels|Markdown|Historia/calibración/rangos, reviewer y umbrales aprobados.|
|D03|Borrador de preparación de evaluación de RAG|JSON|Tickets privados, permisos API, runtime/config, reviewer y thresholds.|
|D04|Solo tres acciones de seguimiento, sin task|JSON|Decisión, población/ventana y acceso.|

READY se refiere a preparar el encargo autorizado, no ejecución posterior. D01–D03 tienen seis obligaciones y tres prohibiciones cada uno; D04 cuatro obligaciones y tres prohibiciones. Puntuar por caso, no promedio agregado de obligaciones. Rúbrica exige un borrador con contenido de tarea, al menos un output futuro con contenido específico y revisión; el propio borrador no cuenta como output futuro. No exige filename, field ni wording particular. Propuestas explícitas permitidas; acuerdos inventados no.

Baseline es el workflow congelado anterior al párrafo de task concreto. Treatment añade únicamente ese párrafo de751bytes. Comprobación de eliminación exacta PASS. Task/context/artifacts/contrato idénticos por par. Sin templates, MANUAL ni ejemplo del autor en payloads. Checker0.2.0 común propuesto para ambos, no tratamiento. No claims sobre eficacia de compiler/template completo.

La señal favorable se fija antes de outputs: mejora en cumplimiento conjunto en al menos dos de los tres drafts, sin empeorar otro case; control D04 conforme en ambas, sin nuevos falsos bloqueos/violaciones. Empate no demuestra mejora; defectos de preparación impiden señal sobre cobertura completa. Un run por celda es exploratorio, no prueba variabilidad/generalización.

## Verificación

`verify_preparation.py`: PASS. Reensambla los ocho payloads solo desde fuentes públicas; verifica contraste/diff/hashes y rúbrica. Comprueba520filas descritas=10SKU×52semanas, sin convertir metadata en raw; parsea tres lecturas sin labels; confirma restricciones RAG y tres preguntas del control. No modelos, anomalías inferidas ni evaluación semántica de respuestas.

Integridad **421archivos** históricos PASS. Fuente/snapshots anteriores intactos. No cambios de código/producto/Foundry ni promotions. No suite nueva del producto: solo checks de preparación;189tests del último ajuste son evidencia histórica, no nueva ejecución ni eficacia.

Revisión del mismo autor, no independiente ni ciega. Casos nuevos respecto de los expedientes previos, pero diseñados con conocimiento del fallo T05. Expecteds/protocolo privados no van al runtime; igualdad de ensamblaje no prueba por sí sola aislamiento nativo.

Freeze de **39archivos**, SHA-256 `cb7f2ae23e03418af3081005c17586719b2152bb604274d9235b314a504f5aba`.

[Paquete](../../../evaluations/os-workflow/2026-10-09-task-draft-01/README.md) · [Protocolo](../../../evaluations/os-workflow/2026-10-09-task-draft-01/protocol.md) · [Rúbrica](../../../evaluations/os-workflow/2026-10-09-task-draft-01/reviewer/rubric.md) · [Checks](../../../evaluations/os-workflow/2026-10-09-task-draft-01/preparation-checks.json).

## Consumo y pendientes

US$0 adicionales; coste anterior acumuladoUS$0.04153488 estimados sin cambios. Ninguna nueva llamada pagada autorizada. Pendiente revisión concreta del paquete/criterios, configuración/runtime/versiones/control de gasto, autorización nueva, ejecución de ocho celdas y review semántica con citas. Smoke, si se añade, debe separarse y no reutilizar estos cases. No retries automáticos, expected/criterios sin cambiar después de outputs. Saldo previo no habilita gasto ni promociones Foundry.
