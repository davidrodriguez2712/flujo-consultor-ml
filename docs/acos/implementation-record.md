# SDD ledger — plan: docs/superpowers/plans/2026-10-06-acos-project-compiler.md

Ruling: implementación en workspace actual sin Git — el plan prohíbe inicializar Git y el directorio no es un repo; no hay branch/worktree ni commits que crear. Scripts SDD dependientes de Git se sustituyen por este ledger y pruebas por tarea.
Pre-flight: tareas 1→2/3/4/5/6/7 usan los modelos compartidos; 2+3→4 componen catálogo/inventario; 4→5 usa CompilationPlan y root efímero; 5→6 usa Manifest; 6→7 expone solo lecturas; 7→8 pruebas del entry point. Sin conflictos de firma.
Ruling: aprobación del plan incluye las verificaciones del producto expresamente descritas; se ejecutan en .venv local sin instalar globalmente.
Task 1: complete — pytest test_contracts.py test_config.py: 17 passed; RED imports ausentes → GREEN.
Task 2: complete — pytest test_catalog.py test_classifier.py: 7 passed; 15 módulos, reglas cerradas y recursos empaquetados del OS.
Task 3: complete — pytest test_foundry.py: 8 passed; inventario operativo, veto por decisión y hash de recursos.
Task 4: complete — pytest test_resolver.py: 8 passed.
Ruling: proposed_paths se añade al empezar renderer durante tarea 4 — preview necesita paths exactos antes de compilar; renderer de contenido permanece tarea 5.
Task 5: complete — render/compiler 11 passed; suite 51 passed.
Ruling: reservar directorio final con mkdir exclusivo y escribir desde staging, manifest último — rename POSIX puede reemplazar un directorio vacío creado concurrentemente; coste: directorio incompleto visible hasta manifest, marcado como no inicializado.
Debug: rollback test detectó bypass de write_exclusive en archivos normales; usar un único writer con limpieza limitada de parciales y volver a ejecutar suite.
Task 6: complete — project/gates 8 passed; lectura local, revisión humana y protección de secuencia/hashes.
Task 7: complete — intake/cli/llm 11 passed; consentimiento por payload, cuatro comandos y cancelación sin escritura.
Task 8: complete — suite 82 passed; wheel/sdist construidos. Wheel instalado en /private/tmp/acos-install-check (Python 3.13.2/macOS), executable init/status/next/validate comprobado fuera del checkout; workspace movido sigue usable y comandos de lectura no alteran bytes.
Ruling: pruebas E2E/distribución ejercitan componentes ya implementados y pasan al añadirlas; no se induce un fallo artificial. Nuevos defectos sí requieren regression RED→GREEN.
Limitaciones verificables: ejecución nativa Linux/Windows, Python 3.11 y carga real de skills en Claude/Codex pendientes por falta de esos entornos; no publicación PyPI ni instalación global.
Final review: reviewer independiente /root/acos_final_review; sin Critical, cuatro Important reproducidos.
Fix pass único: hash_bundle incluye recursos ocultos; decisiones operativas son allowlist explícita; BLOCKED/COMPLETED respetan invariantes; GateSpec valida estructura interna y loader responde código4 sin traceback. Siete regresiones de review RED→GREEN; suite91 passed.
Post-review: ayuda argparse traducida (regression RED→GREEN), timeout LLM real controlado verificado. No editar Foundry ni reabrir candidates.
Ruling: finishing-a-development-branch no tiene rama/worktree que integrar — workspace sin Git por restricción del plan; conservar artifacts y entregar paquete local, sin merge/push ni menú inaplicable.
Aceptación adicional: API sin UI no declara capabilities UI requeridas ni gaps de Figma/visual QA; regression RED→GREEN. Suite92 passed.
Cache uv: un intento de reinstalación bloqueado por permisos del cache global; se resolvió con --cache-dir /private/tmp/acos-uv-cache, sin escalación ni cambios globales.

Entrega final: suite92 pruebas; wheel/sdist0.1.0; cuatro hallazgos Important corregidos. Verificación nativa Linux/Windows y harnesses pendientes en esa entrega, documentada en release.md.

## Ronda adicional solicitada por el usuario — 2026-10-06

- Suite macOS repetida: 92 passed en 2.22 s; repetición final: 92 passed en 2.23 s.
- Linux ARM64 en Docker, Python 3.11, instalación desde source: 92 passed en 2.36 s; contenedor temporal eliminado.
- Nuevo runner `scripts/validate_business_scenarios.py`: 24 casos y 164 comprobaciones de etapas por ejecución. PASS con source/Foundry en macOS, wheel instalado/Foundry en macOS y paquete instalado/sin Foundry en Linux.
- Scanner real: 9 skills operativas, ninguna incidencia; se seleccionaron 8 distintas según preconditions, sin cambios de madurez.
- Smoke del executable instalado: init/status/next exit 0; validate exit 3 (NEEDS_REVIEW esperado); queries sin cambios de bytes; workspace movido operativo.
- Build nuevo de wheel/sdist exit 0. No se modificó código del producto ni Foundry en esta ronda.
- Windows, carga efectiva por Claude Code/Codex y piloto real pendientes. Linux/Python 3.11 quedan verificados con alcance Docker; no se afirma ejecución en una laptop Linux independiente.
- Evidencia detallada: `docs/acos/validation/2026-10-06-validation-report.md` y JSON por caso.

### Continuación: harnesses reales

- Codex CLI 0.160.0 y Claude Code 2.1.290 ejecutados en macOS con workspace churn sintético y permisos de lectura.
- 4/4 pruebas: invocación guiada de skill y sesión nueva con mensaje exacto `continuemos`, para cada runtime.
- Ambos leyeron estado canónico, detectaron vistas obsoletas y conservaron bloqueo/gates sin aprobación. Carga de design-validation desde su carpeta nativa confirmada por trazas.
- Comparación SHA-256 de todos los archivos antes/después: sin cambios en las cuatro ejecuciones.
- Suite repetida: 92 passed en 2.51 s. Sin cambios de producto o Foundry.
- Evidencia: `docs/acos/validation/2026-10-06-runtime-report.md` y JSON de resultados. Recorrido Windows preparado en `windows-check.md`; ejecución Windows y piloto real siguen pendientes.

Verificación final: .venv/bin/python -m pytest -q → 92 passed; python -m build --no-isolation → wheel/sdist exitosos. Wheel final reinstalado con cache temporal; smoke init/status/next/validate → 0/0/0/3 (NEEDS_REVIEW), sin mutar archivos; proyecto movido usable.

### Runner temporal versionado — 2026-10-07

- Utilidad local `scripts/evaluations/temporal_runner.py` 0.2.0 y schema común 0.1.0 draft-07; sin cambios del paquete instalado.
- Separa éxito del runtime, validación estricta local y contenido externo. Sin expected en runner/payload ni fallback a result. Preserva Unicode inválido y metadata; cuatro regresiones RED→GREEN.
- 15 pruebas del runner, 112 en suite local y 138 en suite ampliada pasan. Reviewer separado confirmó corrección antes de los calls.
- Dos calls Claude CLI aprobados, case E reutilizado: ambos con structured_output válido, 6/6 campos y 2/2 decisiones correctos, gate NEEDS_REVIEW. Coste reportado USD 0.1337862; no es nueva evaluación de eficacia.
- Integridad conservada: 424 archivos anteriores y 48 entradas protegidas del piloto. Foundry sin promociones.
- Informe y siguientes pasos: `validation/2026-10-07-structured-runner-v02-report.md`.

### Evaluación temporal ronda 03 — 2026-10-08

- Seis escenarios inéditos, 18 registros sintéticos y 24 calls aprobados; runner común 0.2.0, schema 0.1.0 y contrato congelado 0.1.0. No cambios de producto.
- Empate: 108/108 campos y 36/36 decisiones por condición; ninguna admisión indebida ni pérdida de válidos. No eficacia temporal adicional demostrada.
- Revisión del autor: dos outputs baseline con preguntas problemáticas frente a cero treatment; ambas condiciones tienen preguntas redundantes. No es revisión ciega o independiente ni justifica promociones.
- Pruebas: 23 del runner/checker y 138 ampliadas pasan. Freeze de 32 inputs y 456 archivos previos/48 entradas protegidas del piloto verificados.
- Coste total reportado USD 1.6491066. Informe: `validation/2026-10-08-temporal-contract-round-03-report.md`. Revisión humana de conclusiones pendiente; siguiente propuesta: selección operacional.

### Selección operacional ronda 02 — 2026-10-08

- Runner/schema selección 0.1.0, checker con dimensiones separadas y enumerador exhaustivo pequeño. Transporte derivado de temporal0.2.0 sin modificarlo; sin cambios de paquete instalado.
- 13 pruebas nuevas RED→GREEN, 125 suite local y 151 ampliada pasan. Review de código y cases por otro agente antes de freeze sin Critical/Important pendientes.
- Seis escenarios nuevos, 45 inputs/criterios congelados y 24 llamadas aprobadas. Ambas condiciones: 12/12 outputs coinciden en campos comprobados; no mejora decisional adicional.
- Review autor y agente separado de24outputs: defectos de texto en ambas condiciones, CIs E numéricamente correctos bajo supuestos declarados. Sin score semántico compuesto ni promoción Foundry.
- Coste total CLI USD0.8604986. 788 archivos anteriores/48 entradas protegidas del piloto intactos. Informe: `validation/2026-10-08-operational-selection-round-02-report.md`.
- Próximo hito propuesto: segundo piloto e2e de crédito con capacidades existentes, después de revisar conclusiones; no diseñado/ejecutado. Windows nativo y datos reales pendientes.

## 2026-10-08 — Segundo piloto: riesgo de crédito, Discovery preparado

Diseño aprobado por David. Workspace nuevo con CLI instalada 0.1.0, configuración Foundry en memoria y clasificación local. Tres snapshots experimental 0.1.0 para ambos runtimes. Generator stdlib reproducible: 7.200 solicitudes, 24 meses, cinco CSV; pendientes y rechazadas sin target, disponibilidad explícita y leakage posterior deliberado. Seis pruebas RED antes de implementar y GREEN después; suite producto 125 y combinado 157 pasan.

Discovery está IN_PROGRESS / NEEDS_REVIEW, integridad OK y ninguna etapa aprobada. No se entrenaron modelos, no hubo nuevas llamadas API ni cambios al producto/Foundry. Revisión separada por agente sin hallazgos Critical/Important; dos mejoras Minor de regresión documentadas. Los 1.180 archivos previos protegidos conservan sus hashes.

[Paquete de Discovery](../../pilots/riesgo-credito-sintetico/reports/discovery/discovery-review.md), [verificación](../../pilots/riesgo-credito-sintetico/reports/discovery/verification.json) y [perfil fuente](pilots/riesgo-credito-profile.yaml). Próximo paso: revisión humana del paquete y, tras su aprobación, Framing con métricas, población y aceptación explícitas.

## 2026-10-08 — Piloto de crédito: Framing preparado

David indicó «continúa» tras presentar el paquete de Discovery y su revisión pendiente. Se registró su aprobación y evidencia; Discovery PASS, avance explícito a Framing. Contratos de población, target, métricas (Brier propuesto como primaria), scope, ranking hasta 100/mes y aceptación preparados para revisión humana. Framing NEEDS_REVIEW e integridad OK. No entrenamiento, cambios de fuentes, Foundry o producto ni calls adicionales a APIs. Verificación de hashes: cinco CSV y 1.180 archivos previos protegidos intactos.

[Revisión de Framing](../../pilots/riesgo-credito-sintetico/framing/review.md) y [checks](../../pilots/riesgo-credito-sintetico/reports/framing/verification.json). No se corrieron tests de código nuevos en este paso documental.

## 2026-10-08 — Piloto de crédito: Diagnosis preparado

Framing aprobado explícitamente por David, evidencia registrada y avance a Diagnosis. Aplicación manual de tres pautas experimental0.1.0 con reportes trazables. Checks ad hoc: joins1:1, fan-out hipotético35.914filas por cliente,455labels tardías al fit y presencia de información posterior. Diseño temporal propuesto:development al2025-01-01/validationenero–febrero, finalfit2025-07-01 con2.140filas y holdoutjulio–septiembre de900solicitudes (447concedidasmaduras). Sin entrenamiento ni métricas predictivas. No evaluación ciega: raw utilizado para checks de calidad.

Revisión técnica por otro agente sin hallazgos bloqueantes. Diagnosis y data-quality NEEDS_REVIEW, integridadOK. Perfil/módulos/snapshots, fuentes, generator, contratos de Framing aprobados y1.180archivos previos protegidos conservan hashes. Sin nuevas llamadas API ni cambios al producto/Foundry. No nuevas pruebas de implementación en este paso documental.

[Paquete de Diagnosis](../../pilots/riesgo-credito-sintetico/reports/diagnosis/review.md), [checks](../../pilots/riesgo-credito-sintetico/reports/diagnosis/verification.json). Próximo paso tras revisión humana: contrato/código de ejecución congelados, pruebas y baseline de development.

## 2026-10-08 — Piloto de crédito: development ejecutado

Diagnosis y data-quality aprobados por David, evidencia registrada y avance a Execution. Baseline stdlib de regresión logística L2 con configuración fija y referencia constante; 24 tests RED/GREEN iniciales. Revisión previa detectó reporting incompleto: se corrigió con RED/GREEN, total 25 tests del baseline. Suite de producto 125 y conjunto combinado 182 pasan.

Código/policy/cinco CSV/contratos congelados antes del run principal. Train 1.248, validation 298: Brier 0.104092 frente a referencia 0.116932; ROC-AUC 0.708430. Métricas por mes y clientes conocidos/nuevos, bins fijos y Top-100 retrospectivo. Recálculo aritmético y revisión por otro agente coinciden. Pruebas previas en copias temporales del mismo fixture declaradas; no se usaron para tuning.

Execution NEEDS_REVIEW, integridad OK. Sin evaluación final, nuevas llamadas API ni cambios al producto/Foundry. Fuentes, generator, contratos de Diagnosis aprobados y 1.180 archivos previos protegidos intactos. Dos mejoras Minor de cobertura de pruebas documentadas, sin bug observado. El resultado es puntual y sintético; no demuestra impacto de revisión ni eficacia de skills.

[Paquete de Execution](../../pilots/riesgo-credito-sintetico/reports/execution/review.md), [verificación](../../pilots/riesgo-credito-sintetico/reports/execution/verification.json) y [manifest](../../pilots/riesgo-credito-sintetico/reports/execution/evidence-manifest.json). Siguiente paso tras aprobación: wrapper probado/congelado y refit/evaluación final según diseño aprobado.

## 2026-10-08 — Piloto de crédito: evaluación final realizada

Execution aprobado por David; evidencia registrada y avance a Validation. Runner nuevo con nueve tests RED/GREEN de fixtures manuales; baseline/configuración y29archivos de development intactos. Freeze antes del run final; refit único2.140filas al2025-07-01,900scores persistidos antes de labels,447concedidasmaduras evaluables y453rechazadas sinoutcome. Brier0.102487vs0.116530,ROC-AUC0.752283. Sin tuning; el resultado es puntual y sintético.

Top-100 de todas las solicitudes coverage26%/22%/26%; Precision/Recall/Lift globales no identificados. Calibración con desajustes y bins pequeños, no certificada. Desempeño de concedidas no se transfiere a rechazadas; benchmark mensual retrospectivo, sin efecto causal o ahorro.

Suite producto125/conjunto combinado191 pasan. Recálculo independiente y review por otro agente coinciden; cinco gates de Validation NEEDS_REVIEW e integridadOK. Fuentes/generator/Diagnosis aprobado/development y1.180archivos históricos protegidos intactos. Sin nuevas llamadas API ni cambios al producto/Foundry. Mejoras Minor de cobertura de pruebas documentadas, sin bug observado.

[Paquete de Validation](../../pilots/riesgo-credito-sintetico/reports/final-validation/review.md), [verificación](../../pilots/riesgo-credito-sintetico/reports/final-validation/verification.json), [manifest](../../pilots/riesgo-credito-sintetico/reports/final-validation/evidence-manifest.json). Próximo paso tras aprobación: Delivery con decision memo y límites de la decisión operacional.

## 2026-10-08 — Piloto de crédito: Delivery preparado

David aprobó los cinco gates de Validation; evidencia/reviewer/hash registrados, etapa completada y avance a Delivery. Decision memo, informe analítico, recomendación, contrato y ocho claims trazables preparados. Recomendación propuesta: prototipo como evidencia de laboratorio; decisión sobre todas las solicitudes parcialmente respondida. Definir política online/población/outcomes/evaluación antes de uso real, sin inventar labels de rechazadas.

65campos y19enlaces locales reconciliados; review documental por otro agente sin hallazgos bloqueantes. Delivery NEEDS_REVIEW e integridadOK. Fuentes/código/Diagnosis/desarrollocerrado29archivos/finalcerrado35archivos y1.180archivos históricos protegidos intactos. Sin modelos nuevos, calls API, transferencia al Foundry o publicación. No nuevas pruebas de implementación en este paso documental;191pruebas de Validation son evidencia histórica.

[Decision memo](../../pilots/riesgo-credito-sintetico/delivery/decision_memo.md), [paquete de Delivery](../../pilots/riesgo-credito-sintetico/reports/delivery/review.md), [verificación](../../pilots/riesgo-credito-sintetico/reports/delivery/verification.json) y [manifest](../../pilots/riesgo-credito-sintetico/reports/delivery/delivery-manifest.json). Siguiente paso tras aprobación: handoff con runbook, inventario de evidencia y pendientes; cierre tras revisión de esa etapa.

## 2026-10-08 — Piloto de crédito: Handoff preparado

Delivery aprobado por David y avance a Handoff. Runbook, inventario, handoffs, feedback local de capacidades y pendientes preparados. Reproducción en copia fuera del checkout del mismo macOS/Python: seis archivos de datos, seis JSON development y siete JSON final idénticos; metadata coincide salvo timestamp. No nueva evaluación independiente ni prueba Windows nativa. Manifests/freezes de crédito y 1.180 archivos históricos protegidos intactos; cero llamadas adicionales a APIs. Handoff NEEDS_REVIEW, proyecto IN_PROGRESS; cierre tras revisión humana.

[Paquete de Handoff](../../pilots/riesgo-credito-sintetico/handoff/review.md), [reproducción](../../pilots/riesgo-credito-sintetico/reports/handoff/reproduction-checks.json).

## 2026-10-08 — Piloto de crédito cerrado

David aprobó Handoff y cierre mediante «aprobar». Registro canónico con siete etapas completadas y doce gates PASS; estado COMPLETED. Paquete de Handoff preparado y evidencia anterior conservados; inventario de cierre separado. Resultado técnico favorable puntual en concedidas, decisión global parcialmente respondida, capacidades experimental y Windows nativo pendiente. Sin nuevas llamadas API ni cambios al Foundry.

[Cierre del piloto](../../pilots/riesgo-credito-sintetico/handoff/closure.md).

## 2026-10-08 — Balance de ambos pilotos y continuación

Contrastados feedbacks de churn/crédito con cinco candidates canónicos existentes y las rondas temporal/selección cerradas. Se conserva la decisión de mantener como conocimiento; no nuevas fichas, skills, experimentos o promociones. Balance local con siete enlaces y cinco rutas de candidate comprobados. Recomendación: completar Windows nativo si hay host; alternativamente intake del próximo engagement independiente. Disponibilidad de Windows consultada al usuario.

[Balance y prioridades](validation/2026-10-08-post-two-pilots-review.md).

## 2026-10-08 — Preparación vigente de Windows

Revisión detectó conteo obsoleto de92tests y wheel histórico distinto de la fuente en acos/project.py. Construido wheel separado en artifacts/windows-readiness-2026-10-08;32archivos del paquete idénticos a fuente. Colección actual125tests (no ejecución de suite). Actualizado recorrido PowerShell para construir/instalar artefacto vigente y registrar skips/exit codes. Wheel histórico, instalación del usuario y pilotos cerrados conservados. Windows nativo sigue pendiente de host; no nueva release ni publicación.

[Recorrido](validation/windows-check.md), [checks de preparación](../../artifacts/windows-readiness-2026-10-08/readiness-checks.json).

## 2026-10-08 — Smoke del wheel actualizado

Contenido del wheel cargado desde carpeta temporal fuera del checkout con dependencias existentes. Nueve comandos pasan: creación, traslado, status/next/validate, conservación --here y rechazo de colisión sin sobrescritura. Config/discovery Foundry desactivados en memoria; no prueba wizard completo, instalación aislada de dependencias ni Windows. Primer intento cancelado correctamente por respuesta vacía del probe; corregido stdin sin cambiar producto. Sin APIs ni modificaciones a pilotos. Windows nativo continúa pendiente.

[Resultados](../../artifacts/windows-readiness-2026-10-08/wheel-smoke-checks.json).

## 2026-10-08 — GitHub Actions Windows completado

David eligió GitHub Actions y autorizó repo privado davidrodriguez2712/agentic-consulting-os. Publicados69archivos de código/pruebas en copia Git temporal; no Foundry/pilotos/evidencia histórica. Run01falló por setuptools65.5.0 frente a >=68; Run02suite/simulaciones/build pasan, smoke falso positivo por alias8.3Windows. Corregidos workflow/check, no compiler. Run03success commit051c46a71c80efaad3213e0b430d4cd4e18ada33:125tests sin errores/skips,24simulaciones/164checks,12comandos smoke con wheel instalado aislado. Artifacts de3intentos descargados y hashados; matriz actualizada para Windows Server2022x64/Python3.11.9. Harnesses/Windows11ARM/eficacia de skills no acreditados. Sin nuevas llamadas API de runtimes ni cambios al Foundry/pilotos.

[Informe](validation/2026-10-08-github-actions-windows-report.md).

## 2026-10-08 — Windows 11 ARM y descubrimiento de runtimes

David priorizó runtimes Windows y Windows 11 ARM. Matriz manual con Windows Server 2022 x64/Python 3.11.9 y Windows 11 ARM64/Python 3.13.16. Primer intento falló al mover el proyecto por proceso hijo del wrapper Codex; corregido el probe para ejecutar el binario nativo directamente, sin cambiar el compiler. Segundo intento, run 37882006292 / commit 5b52a83e196e304a8b4fb1663802c0cba6261aeb: ambas plataformas pasan 125 tests sin failures/errors/skips, 24 simulaciones / 164 checks y 12 comandos de smoke. Codex 0.160.0 y Claude Code 2.1.294 nativos descubren fixture local antes/después del traslado. Cero turns de modelos; conversación y continuidad autenticadas pendientes de autorización y límite de consumo. Descargados ambos intentos, inventario de 53 archivos; evidencia Windows previa y manifests de Handoff de crédito intactos. Sin cambios al Foundry ni publicación de release.

[Resultado, reproducción y límites](validation/2026-10-08-windows-arm-runtimes-report.md).

## 2026-10-09 — Integración autenticada Windows completada

Codex 0.160.0 y Claude Code 2.1.294 pasan skill nativa design-validation y
continuidad con `continuemos` en Windows x64 y Windows 11 ARM64: 4/4
combinaciones, ocho ejecuciones aceptadas, sin modificar el workspace.
Se usa snapshot experimental real; no se acredita eficacia ni se promueve
Foundry. Se conservan fallos y las revisiones del harness. Coste API estimado
US$0.346215125; total conservador con reservas rechazadas US$0.565150375,
bajo el dólar autorizado. Suite local final 144 tests. Fuentes anteriores
y manifests de Handoff de crédito intactos. Sin publicación en PyPI.

La siguiente prioridad es intake de un engagement independiente y revisión
de capacidades ante fallos observados. [Evidencia y límites](validation/2026-10-09-windows-authenticated-report.md).

## 2026-10-09 — Discovery retail con datos públicos reales

Diseño y plan aprobados. Workspace retail-valor-90d-publico inicializado por CLI con cinco módulos y cuatro snapshots experimentales. Online Retail II real descargado de UCI; 1.067.371 filas en dos hojas preservadas. Auditoría: 243.007 filas sin ID, 19.494 cancelaciones y 22.523 filas coincidentes entre hojas considerando multiplicidad. Nueve tests del piloto pasan; fuentes y evidencia previa verificadas. Gate discovery NEEDS_REVIEW; no labels, modelos ni avance de etapa. Encargo/capacidad simulados, coste API US$0; Foundry sin cambios.

[Paquete Discovery](../../pilots/retail-valor-90d-publico/reports/discovery/review.md).

## Retail público — Discovery aprobado y Framing propuesto

David aprueba Discovery; gate PASS verificado y avance a Framing. Contrato propone historia180, horizonte90, capacidad100, reconciliación entre hojas preservando multiplicidad y compras positivas con ID/código estándar. Preview:788.187 líneas/5.852 clientes; códigos excluidos4,06% del importe positivo preliminar posterior a reconciliación. Framing NEEDS_REVIEW, sin labels/modelos ni gasto API. Freeze Discovery corregido por dos planes mutables, preservando versiones con hashes originales; fuentes/snapshots intactos. [Revisión](../../pilots/retail-valor-90d-publico/reports/framing/review.md).

## 2026-10-09 — Tres mejoras y ensayo conjunto aceptado

Pautas/templates/manual incorporan freeze, reproducción con serialización y QA de cifras/etiquetas/períodos. Piloto forecasting independiente con Online Retail II reutilizado: media4 elegida por development; WAPE final13,15%, sin staffing ni eficacia causal. Tres checks conjuntos PASS; siete outputs idénticos en copia independiente, 153tests durante preparación y evidencia retail previa263archivos intacta. David acepta paquete con límites mediante «Aprobado seguimos». Cierre COMPLETED desde entrada validation; tres etapas, once gates PASS y trece comandos de cierre exit0; manifest70archivos intacto. API US$0, Foundry sin cambios.

[Informe](../../pilots/retail-capacidad-semanal-publico/PILOT_REPORT.md) · [Cierre](../../pilots/retail-capacidad-semanal-publico/reports/closure/closure.md).

## 2026-10-09 — Evaluación conjunta menos guiada preparada

Usuario autoriza preparar seis cases (dos freeze, dos reproducción, dos etiquetas), tres con defecto y tres coherentes. Doce payloads con baseline por ablación y treatment con las tres pautas nuevas, expected privados separados. Checks locales PASS, 48 archivos congelados; ningún call/modelo/budget de ejecución autorizado, US$0. Revisión del mismo autor, aislamiento de runtime y evaluación de outputs pendientes. Sin cambios al compiler, Foundry ni paquete aceptado del último piloto.

[Paquete y pendientes](validation/2026-10-09-os-workflow-evaluation-preparation-report.md).

## 2026-10-09 — Controles y configuración de evaluación preparados

Aceptación concreta del protocolo/expected registrada fuera del freeze. Checker de formato/estado/referencias y transporte nativo con controles de presupuesto preparados con TDD; Haiku5.5 explícito y defaults Windows conservados. Suite162tests y siete del piloto PASS; integridad48+70archivos PASS. Freeze adicional12archivos con configuración/runbook/snapshots/checks. Propuesta: un smoke y doce invocaciones, hastaUS$0.20total, sin retries; presupuesto todavía sin autorizar. Cero llamadas/APIUS$0. Aislamiento/compatibilidad real, outputs y revisión semántica pendientes; ninguna eficacia o promociónFoundry acreditada.

[Informe y siguientes pasos](validation/2026-10-09-os-workflow-execution-config-report.md).

## Evaluación menos guiada — gasto autorizado, credencial local pendiente

David aprueba hastaUS$0.20total, smoke+doceejecuciones sin retries. Autorización registrada contra manifest de configuración, fuera del freeze. Preflight integridad/snapshots PASS; CLI actualizado a2.1.296 activa parada por versión, flags revisados y amendment pendiente antes de smoke. API key Anthropic no está en el entorno ni en .env del proyecto; solicitada ruta/mecanismo seguro. Cero calls/APIUS$0; no sustituir por presupuesto adicional ni auth OAuth que evada el proxy.

## Evaluación menos guiada — smoke real PASS y ronda01 detenida

David proporciona clave local en .env; no expuesta, excluida de Git. CLIpatch2.1.296 revisado y amendment registrado. Smoke PASS con un request. E01baseline agota cap2048 (thinking590), CLI intenta continuación y proxy bloquea antes del proveedor; termina error. Dos requests HTTP200; no problema de credencial, 403 local. Coste estimadoUS$0.001540175; quedaUS$0.198459825 del total autorizado. Sin retries, cero pares comparables, semántica/eficacia no evaluables. Freeze15archivos del intento e integridad previa48+12+70PASS. Propuesta: configurar cap8192 y capturar stopreason upstream; nueva ronda manual requiere excepción explícita al sin-reintentos y presupuesto acumulado conservado.

[Resultado y diagnóstico](validation/2026-10-09-os-workflow-round-01-report.md).

## Evaluación menos guiada — ronda02 completada y revisada localmente

David autoriza cap8192 y nueva ronda manual dentro del total acumulado US$0.20. TDD cap/reserva y stopreason RED→GREEN; suite164PASS. Smoke+12respuestas nativas PASS,13end_turns,ningún retry/rechazo. Total ambas rondasUS$0.02065453 estimados. Revisión semántica del autor, no independiente: obligaciones completas baseline2/6,treatment4/6; estado5/6ambas; JSON purobaseline2/6,treatment0/6; falso bloqueoE02ambas; desviación adicional enE03treatment. Resultado MIXED, regla favorable no satisfecha, sin eficacia general ni promociónFoundry. Decisiones semánticas/quotes y errores adicionales conservados; freeze86archivos, integridad previaPASS. Siguiente: revisión humana y diseño acotado de formato, reproducción fiel y continuidad de planes vivos; no llamadas pendientes de la ronda.

[Informe completo](validation/2026-10-09-os-workflow-round-02-report.md).

## Pautas — formato, reproducción fiel y continuidad implementados

David aprueba diseño acotado. Workflow/templates/manual distinguen contrato específico de salida (JSON puro sin fences), reproducir/diagnosticar/corregir método y preparación de tarea frente a ejecución/gates. Template project-and-task añadido a composición básica para que el manual tenga recurso disponible; test missing-template RED→GREEN, hash inicial conforme al contrato del manifest. Suite165PASS; proyecto temporal status/next integrityOK y validateNEEDS_REVIEW esperado; wheel local con recursos actualizados. Revisión de pautas del autor no prueba eficacia de agentes. Integridad241archivos anterioresPASS, freeze12archivos del cambio. Cero calls/APIUS$0adicionales, Foundry sin cambios/promociones. Siguiente: diseño de casos inéditos de transferencia y criterios/configuración antes de evaluar eficacia.

[Informe y evidencia](validation/2026-10-09-os-workflow-refinement-report.md).

## 2026-10-09 — Transferencia de los tres ajustes preparada

David aprueba cobertura de seis casos: churn/API, pricing/Markdown, inventario/IDs, forecast/cambio autorizado, crédito/borrador y retención/lanzamiento. Doce payloads; baseline snapshot previo frente a workflow actual, sin templates/MANUAL. Checks de fixtures/ensamblaje PASS e integridad253archivos históricos PASS. Criterios privados y manifest congelados; autor no independiente, eficacia NOT_EVALUATED. Detectada incompatibilidad del system prompt JSON del runner anterior con caso Markdown; adaptación y checker pendientes antes de calls. Preparación APIUS$0; gasto previoUS$0.02065453. Ejecución/configuración/gasto nuevo no autorizados; Foundry intacto.

[Informe y pendientes](validation/2026-10-09-os-workflow-transfer-preparation-report.md).

## 2026-10-09 — Transferencia: runner/checker/configuración listos

David aprueba paquete y ajuste acotado. Transporte acepta prompt neutral explícito, default JSON preservado; nuevo checker de transferencia JSON/Markdown separa estructura/estado/rutas de contenido. TDD17fallos nuevos→GREEN,28tests focalizados; suite182PASS con proveedores simulados. Freeze13archivos de configuración; preparación50/históricos253 y snapshots intactos. Propuesta hastaUS$0.10 adicionales, smokeMarkdown+12celdas, Haiku5.5/effortlow/cap8192, sin retries. Cero calls; presupuesto pagado pendiente, compatibilidad real y eficacia NOT_EVALUATED. Foundry intacto.

[Informe y autorización pendiente](validation/2026-10-09-os-workflow-transfer-config-report.md).

## Transferencia — ronda01 pagada completada, resultado inconcluso

David autoriza hastaUS$0.10adicionales. Preflightpycache corregido antes de proveedor, cero calls iniciales. Smoke+12respuestas,13end_turn/HTTP200, sin retries/rechazos; US$0.02088035nuevo y US$0.04153488acumulado ambos estudios. T02excluido simétricamente por escenario pricing ambiguo y checkerEstado restrictivo; raw/expected intactos. Cinco pares comparables: contenido4/5ambas, formato4/5Bvs5/5T, mejora schemaT06; T05draft incompleto ambas. Sin señal favorable en dosfamilias ni cobertura completa; revisión del autor no independiente. Integridad316archivos PASS, freeze86archivos de run. Foundry sin cambios/promociones; nuevascalls no autorizadas por saldo.

[Informe y pendientes](validation/2026-10-09-os-workflow-transfer-round-01-report.md).

## Ajustes locales02 — checker, pricing y task concreto

David aprueba diseño. Checker0.2.0 acepta explicación tras primer estado y rechaza estados adicionales; TDD3fallos→GREEN,35tests focalizados y suite189PASS. PricingP02-v02 documenta cantidad1000/precio100→120/coste75, margen25→37,5%, diferencia12,5pp; corrección expuesta, no inédita. Workflow/template/manual piden task redactado con inputs/outputs/criterios/dependencias y desconocidos pendientes. Ejemplo del autor, no simulación. Proyecto temporal status/nextPASS, validateNEEDS_REVIEW esperado; copias canónicas/bundle/template generado coinciden. Integridad402archivos PASS; freeze19archivos. APIUS$0 adicional, previoUS$0.04153488; eficacia pendiente y nuevascalls no autorizadas. Foundry intacto.

[Informe y pendientes](validation/2026-10-09-os-workflow-local-refinement-02-report.md).

## Task concreto — nueva evaluación preparada

David aprueba cuatrocasos: forecastinventario, anomalíassinlabels, evaluaciónRAG y seguimientosintask. Ocho payloads, único contraste751bytes de pauta de borrador; sin template/MANUAL/ejemplo. Rúbrica de concreción y criterio exploratorio congelados; equivalencia semántica, outputs futuros distintos del borrador y acuerdos/propuestas separados. Checks de preparación PASS, integridad421archivos PASS, freeze39archivos. Cero calls/APIUS$0 adicional; previoUS$0.04153488. Review del autor no independiente y eficacia pendiente; paquete/configuración/gasto por revisar. Producto/Foundry intactos.

[Informe y pendientes](validation/2026-10-09-os-workflow-task-draft-preparation-report.md).

## Task concreto — configuración preparada para revisión/gasto

Usuario indica siguiente. Review local del autor y configuración nuevos: Claude2.1.296/Haiku5.5/effortlow/cap8192, checker0.2.0 y neutralprompt común, un smokeMarkdown+8celdas, sin retries. Runbook especifica guard9/schedule para no confundir ceiling13 del helper con autorización. Propuesta hastaUS$0.10adicionales; saldo no transferido. Checks y421históricos+39preparación intactos; freeze12archivos, código sin cambios. No API ni suite nueva, aceptación humana/configuración/gasto pendiente. Foundry intacto y eficacia NOT_EVALUATED.

[Informe y revisión pendiente](validation/2026-10-09-os-workflow-task-draft-config-report.md).

## 2026-10-10 — Task concreto: ronda01 detenida en smoke

David aprueba paquete/configuración y hastaUS$0.10adicionales. Preflightlocal sinAPI detenido por localhost restringido; ejecución escalada conforme. Una solicitud Haiku5.5 HTTP200/end_turn, runtimePASS, costeUS$0.000241; rawponeREADY antes de##Estado y falla contratoMarkdown. Detención sin retries, cero casosbenchmark enviados; eficaciaNOT_EVALUATED. Integridad421históricos+39preparación+12configPASS, freeze17archivos del intento/diagnóstico, secretoausente en evidencia. Producto/Foundry intactos. Propuesta de smoke con plantilla literal preparada, no ejecutada; configuración02 y aprobación vinculada pendientes. Recomendación límiteUS$0.10acumulado ambasrondas del estudio, no nuevo presupuesto adicional.

[Informe y siguiente propuesta](validation/2026-10-10-os-workflow-task-draft-round-01-report.md).

## 2026-10-10 — Task concreto: configuración02 preparada

David aprueba preparación de nueva configuración, único cambio smokeconplantillaliteral. Casos/expected/rúbrica/runtime/checker/promptneutral intactos; configuración01/ronda01 conservadas. CLI/version/flags/snapshots y smoke literal PASS local, no evidencia de salida modelo. Freeze12archivos, manifest02SHA76ce8d316d09bd679e4efeea012792092c71640a134e7de326f4cc1226fc5a7e. TechoUS$0.10acumulado estudio, previoUS$0.000241, nuevo máximoUS$0.099759. Sin calls/proxy/credencial ni testsuite nueva. Ejecución vinculada a nueva configuración pendiente de aprobación; Foundry intacto.

[Configuración02 y siguiente paso](validation/2026-10-10-os-workflow-task-draft-config02-report.md).

## 2026-10-10 — Task concreto: ronda02 completada, resultado mixto

David autoriza configuration02 ligada al manifest hastaUS$0.099759, manteniendo techo acumuladoUS$0.10. Smoke+8respuestas nativas,9HTTP200/end_turn/usageknown, sin retries/rechazos. Ronda02US$0.01455995; estudio ambasrondasUS$0.01480095; workflowacumuladoUS$0.05633583. Reviewautor no independiente/ciega: formatoB4/4vsT3/4, contenidoB1/4vsT2/4, conjunto1/4ambas; D03mejora,D02regresiónMarkdown,D01incompleto,D04estadoNOT_DETERMINABLEambas. Regla favorableFAIL, sin eficacia general ni promociónFoundry. Integridad501archivos anterioresPASS, freeze63archivos de ronda02, raw y criterios intactos. Cerrar pago; recomendar diseño local de outputs/criterios, headings y estado por acción solicitada antes de otra evaluación.

[Resultados, coste y pendientes](validation/2026-10-10-os-workflow-task-draft-round-02-report.md).

## 2026-10-10 — Ajustes locales03 y paquete detect-leakage

David aprueba diseño acotado. Outputs futuros con contenido/criterios, headings y estado por acción implementados en workflow/template/manual/bundle; checker/schema/tracker sin nueva lógica. Ejemplos del autor pasan formato; compilación status/next0integrityOK y validate4BLOCKED por framingvacío esperado. No suite nueva ni API. Integridad564históricosPASS, freeze17delcambio. detect-leakageexperimental0.1.0 snapshotexacto,3cases públicos(L01confirmado,L02válido,L03indeterminado), expectedprivados/templates canónicos, protocolo y checks preparados; freeze27archivos. Foundry canónico sin modificaciones/promociones; evaluación real/instalación/reviewer/budget pendientes. Coste adicionalUS$0.

[Informe y próximos pasos](validation/2026-10-10-workflow-and-foundry-preparation-report.md).

## 2026-10-10 — detect-leakage: discovery nativo y configuración propuesta

Usuario indica continua. Reviewautor del paquete27archivos intacto, sin fixturedefecto. Trespares SDKinitialize sinusermessage/key/generación: bare/proyecto no discover; pluginlocalexplícito descubreacos-eval:detect-leakage solo treatment con bytes canónicos exactos. DiscoveryPASS, invocación/tools/aislamientoNOT_VERIFIED. Transporteanterior safe/toolsoff y proxyHaiku55rechazatools incompatibles; diseño adaptaciónoptin/multipaso y configdocumental preparados, no implementados. PropuestaUS$0.10nuevo smoke+6runs,8requests/run56global, no retries; no gasto autorizado. Freeze12de review/probes/propuesta. Foundry/madurez sin cambios y APIUS$0. Próximo aprobación diseño+verificaciónlocal antes configurarpaidrun.

[Estado y diseño de transporte](validation/2026-10-10-detect-leakage-native-configuration-review-report.md).


## 2026-10-10 — transporte Foundry nativo verificado localmente

Adaptación opt-in aprobada implementada. Suite completa 214PASS, 0FAIL/ERROR/SKIP. Claude Code 2.1.296 real con proveedor HTTPS simulado: baseline Read/Write/end_turn y treatment Skill exacta/utility readonly/Write/end_turn; tres intentos prohibidos bloqueados. Inputs, utility y plugin protegidos por hashes; fallos detienen solicitudes. Cero API pagada, US$0; eficacia NOT_EVALUATED y Foundry canónico intacto. 620 archivos históricos conservados. Freeze de implementación 89 archivos, manifest SHA256 cafc12aa3183557d101e1db13df5b7797abebffd5c03841c0dfa88939a77c2e2. Pendiente coordinador/configuración congelada, aceptación del paquete y nueva autorización de presupuesto antes del estudio.

[Informe de verificación local](validation/2026-10-10-foundry-native-transport-report.md).


## 2026-10-11 — coordinador Foundry y configuración 01

Orden smoke+6runs, workflow común, autorización/hash antes de credenciales, límites56/8 y parada/persistencia. Suite223PASS; APIUS$0. Freeze29files, SHA25664a52f85b39eedcff77a7ca47f17c5b8664791db48aea0063971e3915480ede0. Pendiente aceptación del paquete/regla, reviewer y autorización hastaUS$0.10; eficaciaNOT_EVALUATED.

[Informe](validation/2026-10-11-foundry-coordinator-report.md).


## 2026-10-11 — smoke Foundry real round01 detenido

Paquete y hastaUS$0.10 aprobados contra manifest64a52f85b39eedcff77a7ca47f17c5b8664791db48aea0063971e3915480ede0. Una solicitudAnthropicHTTP200/tool_use, guardbloqueóBashfueraexactwhitelist, sin reporte ni cases; segundo requestsolo local rechazado, cero retry pagado. Usageknown; estimadoUS$0.000689075. EficaciaNOT_EVALUATED. Run13files SHA256d1c3bcb4e73ee647d29ab301ff5a51adbb60b09dff85c8860395b04917f543b0. Brecha comandoexactonoexplicadoprompt y rejectedinputno retenido; hipótesis no confirmada sobre elección modelo. Sin modificarFoundry/expected/config. Propuesta correcciónlocal común y observabilidad antes nueva config/autorización.

[Informe](validation/2026-10-11-foundry-smoke-round-01-report.md).


## 2026-10-11 — corrección local aprobada y config02

Prompt operativo común con comandoexacto/límites; rejectedtool preview acotado/redactado sin relajar permisos. DosRED→GREEN, suite226PASS. Cero nuevasAPI, eficaciaNOT_EVALUATED. Config02freeze29files SHA25666c77ceb0eccbc72ef6e8f7e65132d3023374077d5f380570391e57c8ee0f941; propuestaUS$0.099310925 restante, totalestudioUS$0.10, no autorizada. Cases/expected/skill/workflow idénticos; historia intacta. Correcciónfreeze SHA25695f7f4cefc89f5d3b29bcbcb1cf634f259941965b66d0ff27cd3737c92401011.

[Informe](validation/2026-10-11-foundry-local-correction-report.md).


## 2026-10-11 — evaluación inicial detect-leakage cerrada

Usuario autorizó rondas necesarias según recomendación manteniendo techoUS$0.10. Cinco rondas preservadas: comandos/8ktruncación/skillomitida/reserva/round05completa. Ajustes comunes de contexto/reportebreve/nativeobligatorio/reservaoptinportier+cota; 229pruebasPASS. Tresparesválidos round05nativeT3/B0. CosteAnthropicestimadoUS$0.07056525total,61requests; no furtherAPIpara este cierre. Contenido B2/T3, contrato/trazabilidad B3/T0, conjunto B2/T0: sin señal favorable; T+37.1%coste observedcases. Autorreview no independiente; mantenerexperimental y proponer cambios, Foundryintacto. No agrupar otroscohorts ni promoverautomáticamente.

[Evaluación final](validation/2026-10-11-foundry-detect-leakage-evaluation-report.md).

## 2026-10-12 — detect-leakage 0.2.0, cierre experimental

Usuario autoriza continuar rondas/correcciones, preservando techoUS$0.10. Revisión independiente de0.1 encuentra defectos adicionales; evidencia previa intacta. Borrador0.2compacto, metadata de runtime dinámica y capconfigurable verificados:233pruebasPASS con localhost/proveedor simulado. Microtextual15calls muestra brevedad0.2:5/5vs0.1:0/5, sin validar efficacyglobal. Tres nuevospares forward y dos regresiones correctos con reservas; baselines nuevos también aciertan. NativeL01completo pero contrato/longitudFAIL; L02max_tokenssinreporte,403localposterior; L03noejecutado. Reviewerindependiente recomienda usoexperimental supervisado. CanonicalFoundry0.2actualizado con hashc2a2440477d9985489b71f4d8c50380ccd7985635d02eab330cfee0f7e5856c4; statusexperimental, sinpromoción ni actualizarsnapshots/globalinstalls. CosteAnthropicestudioUS$0.09112648,83requests; pago detenido. Quick_validateCodexrechazametadataFoundryroot:compatibilidadformalpendiente. Contratonativo, nuevascomparaciones y revisió humana antesmadurezpendientes.

[Informe, límites y evidencia](validation/2026-10-12-foundry-detect-leakage-v02-report.md).

## 2026-10-12 — control mecánico del contrato nativo

Continuación autónoma autorizada: reproducido el avance del coordinador ante reportes inválidos. Check readonly separado de runtime y semántica, prompt/hash persistidos y parada de secuencia/presupuesto ante incumplimiento; reportes originales conservados. Revisión independiente detectó falso PASS de headings en fences; corregido y aprobado en seguimiento, con defensas de fechas/contexto/symlinks. Suite completa262PASS en17.43s, Claude real contra proveedor simulado: baseline/treatment válidos aceptados, reporte inválido rechazado sin reparación. Diagnóstico L01 histórico confirma528/500palabras y claveversion ausente sin alterar su hash. Los222archivos del cierre0.2 y canonicalexperimental intactos. APIadicionalUS$0; acumuladoestudioUS$0.09112648. Pendientes: nueva configuración congelada, L02/L03 y comparación reales con presupuesto suficiente, revisión semántica y compatibilidad formal del template.

[Informe y evidencia del contrato](validation/2026-10-12-native-report-contract-report.md).

## 2026-10-12 — regresión nativa preparada 02 y prueba de saldo

Continuación autorizada: paquete congelado23archivos paraL01–L03treatment0.2, cap8192 por truncación previa, reporte500/final80 y transporte con contrato mecánico. Verify-onlyPASS, manifestb8ef2799245a463cc3e33be88c25e94b1b26af13072862d9f6c613ac2e0da044; aprobación de pagoNOT_AUTHORIZED. Claude real/proveedor simulado:12requests completan3runsconruntime/contratoPASS bajo presupuesto ficticio; con saldoUS$0.00887352, dosrequests sintéticos y bloqueo de reservaUS$0.008994625 antes de escribirL01. Cero llamadas reales/costeAPIadicional; no eficaciaLLM demostrada. Integridad222+55archivos y canonical0.2PASS. Propuesta concretaUS$0.05adicionales, techoestudioUS$0.15, máximo nueva secuenciaUS$0.05887352; pendiente autorización expresa porque excede techo anterior.

[Paquete, simulaciones y propuesta](validation/2026-10-12-native-regression-preparation-02-report.md).

## 2026-10-12 — regresiones reales y cierre de contrato

Usuario aprueba US$0.05 adicionales, techo estudio US$0.15. Config02 real: L01runtime/contratoPASS; L02runtimePASS/frontmatterFAIL; parada sinL03 ni reparación. Esquema literal añadido al prompt común tras RED→GREEN, suite262PASS y revisión de alcance; cases/expected/skill/guards intactos. Config03 nueva: L01–L03runtime/contratoPASS, Skill nativa3/3. Revisión independiente: L01/L02 útiles con reservas, L03 semánticamente no aceptado íntegramente. Coste nuevoUS$0.023976565, acumuladoUS$0.115103045,103requests conocidos; saldoUS$0.034896955. Pago detenido; canonical0.2experimental intacto, sin promoción ni superioridad causal. Pendiente incertidumbre y acciones, comparación nueva y compatibilidad formal.

[Resultados reales, coste y pendientes](validation/2026-10-12-native-regression-real-report.md).

## 2026-10-13 — detect-leakage 0.2.2 y cierre sin costo

0.2.1/0.2.2 con micro textual (gate 5/5 tratamientos aceptables, sin superioridad causal). L03 nativo 0.2.2: runtime PASS, contrato FAIL (515/500 palabras), parada sin reparación; coste US$0.004567405, acumulado US$0.14019795 de 0.15, saldo US$0.00980205. Compilador acepta `status/version` bajo `metadata:` (264 PASS) y el borrador compatible pasa `quick_validate`; canonical 0.2.0 sin migrar. Pendientes humanos: revisión semántica del L03, comparación nueva con presupuesto, adjudicación humana.

[Informe de cierre](validation/2026-10-13-detect-leakage-v022-closure-report.md).

## 2026-10-13 — revisión independiente del L03 nativo 0.2.2

Agente distinto del autor/runner, no humano ni ciego, sin API ni modificación de evidencia. Contenido: ACEPTABLE CON RESERVAS; contrato sigue FAIL (515/500 palabras), sin dispensa. Skill real cargada y check_inputs.py ejecutado; 4 sha256 verificados; cero defectos prohibidos (sin falsa invalidez, sin disponibilidad presumida, sin ejecuciones inventadas); corrige el fallo semántico de 0.2.0. Reservas: «asociación con churn no es mecanismo» solo implícita; hallazgos 2/3 sin todos los campos. El exceso de palabras es redundancia (preguntas 2–5, resumen, hallazgo 3, línea de skill), sin impacto semántico. Una sola ejecución, solo treatment, sin baseline: no demuestra superioridad ni generalización. Madurez experimental, sin promoción. Pendientes: adjudicación humana, corrección de redundancia con prueba nueva y presupuesto (saldo US$0.00980205 insuficiente).

[Revisión completa](../../evaluations/foundry/2026-10-13-detect-leakage-v022/NATIVE_L03_REVIEW.md).

## 2026-10-13 — cierre del estudio detect-leakage

Estudio cerrado con el estado actual, sin API nueva. Canonical 0.2.0 experimental; 0.2.1/0.2.2 sin promoción. Gasto US$0.14019795 de 0.15, saldo US$0.00980205 sin uso. 264 PASS. Sin eficacia causal ni generalización demostradas; L03 nativo 0.2.2 con contrato FAIL (515/500). Pendientes abiertos: adjudicación humana, corrección de redundancia con corrida nueva y presupuesto, comparación menos guiada, decisión sobre migrar a `metadata:`.

[Informe de cierre](validation/2026-10-13-detect-leakage-study-closure.md).

## 2026-10-13 — canónico detect-leakage migrado a `metadata:`

Cambio solo de formato en `~/david-skill-foundry/experiments/skills/detect-leakage/SKILL.md`: `status/version/domain` pasan bajo `metadata:`. Versión 0.2.0 y estado experimental sin cambio; contenido idéntico. Hash previo `c2a2440477d9985489b71f4d8c50380ccd7985635d02eab330cfee0f7e5856c4`, hash nuevo `8bf268c477a56ec687c3b2a8b505c1cb75b625ef32d28a622892faa94e1dd9c9`. `quick_validate` PASS; `scan_foundry` inventaría las 9 skills sin hallazgos. Respaldo previo en `~/david-skill-foundry/SKILL.detect-leakage.0.2.0.pre-metadata.bak.md`. Snapshots, manifests y evidencia históricos conservan el hash anterior y no se tocaron. Foundry sin git: sin diff versionado.

## 2026-10-13 — detect-leakage 0.2.3: dos corridas nativas L03

Adjudicación humana del L03 0.2.2: aceptable con reservas; David autoriza +US$0.03 (techo 0.18). 0.2.3 (un dato por sección). Cap4096: runtimeFAIL por max_tokens (thinking 2709), sin reporte, US$0.004386. Cap8192: runtimePASS, contratoFAIL 532/500 (peor que 0.2.2, 515), US$0.003878. Redundancia no confirmada como causa; hipótesis sin probar: estructura fija (~100 palabras) vs límite 500. CLI 2.1.296→2.1.299 (desviación documentada). Acumulado US$0.14846196, saldo US$0.03153804, pago detenido. Experimental, sin promoción; micro y comparación no ejecutados.

[Informe](validation/2026-10-13-detect-leakage-v023-report.md).

## 2026-10-13 — opción A: límite 650 y L03 nativo 0.2.3 aceptable con reservas

David sube el límite de reporte a 650 (no retroactivo). Corrida única cap8192: runtimePASS, contratoPASS 485/650 (final52/80), US$0.00432061; acumulado US$0.15278257, saldo US$0.02721743. Revisión independiente: aceptable con reservas (mecanismo por hallazgo no etiquetado, churn solo implícito, redundancia leve); sin defectos prohibidos. 485 cabría en 500: varianza entre corridas, causa no demostrada; 515/532 con límite 500 siguen FAIL. Experimental sin promoción; sin baseline ni generalización. Pendientes: adjudicación humana de 0.2.3, subir a PyPI (artifacts 0.1.0 preparados en dist/, sin publicar), remoto git.

[Informe](validation/2026-10-13-detect-leakage-v023-report.md).

## 2026-10-13 — publicación en PyPI

David publicó `agentic-consulting-os` 0.1.0 con `uv publish` (artifacts construidos de HEAD `dist/`). Índice verificado: wheel `8d59637596ff7da15026c1d37c62db3f8a08ab897ac5cf8b5850cecba5ee8522` y sdist `9c64899d45371386b18e3c12cfa8a73320d05f51557355b9151be61a1b5b2e2a`, idénticos a los locales; instalación desde PyPI en venv limpio, `acos --version` 0.1.0. El token usado quedó expuesto en la conversación: debe revocarse. Versión inmutable; correcciones futuras exigen 0.1.1. README/installation/release actualizados. Las skills Foundry no forman parte del paquete.

## 2026-10-14 — Foundry reubicado y README reescrito

El Foundry pasó de `~/david-skill-foundry` a `~/Foundries/david-skill-foundry` (ahora repo git propio y reorganizado; skills enlazadas desde `~/.claude/skills/`). Efecto en ACOS: la autodetección por defecto (`./david-skill-foundry`, `~/david-skill-foundry`) ya no lo encuentra; hay que indicar la ruta en `acos init`, donde se guarda por dispositivo. `scan_foundry` sobre la ruta nueva: 8 skills, sin hallazgos; `detect-leakage` 0.2.0 experimental conserva el formato `metadata:`. Su hash actual es `9af69d09964952a9d12f65f26f7cc74466ce471fa417b238efd46ccb91b4d28a` (la description ahora lleva el prefijo `[EXPERIMENTAL]`), distinto del `8bf268c4…` registrado el 2026-10-13: cambio hecho fuera de esta sesión. Las rutas `~/david-skill-foundry/...` de entradas anteriores son históricas. README reescrito para consultores: requisitos, entregables, etapas y recorrido paso a paso.

## 2026-10-14 — video del flujo para el README

Video `docs/video/acos-flujo.mp4` (82 s, 1280×720, 24 fps, sin audio, subtítulos en pantalla), adaptado del brief «Follow the Record»: un mismo proyecto (`demo-fraude`) recorre perfil → `acos init` → estado central → `status`/`next` → agente → gate BLOCKED→revisión humana→PASS → 7 etapas → entregables. Fuente HTML con reloj determinista y render con Chrome+ffmpeg reproducible (`docs/video/README.md`). Salidas condensadas de las reales; conversación con el agente ilustrativa y señalada. Vista previa GIF en el README. Sin narración.

## 2026-10-14 — guía e2e completa

Nueva guía `docs/acos/ejemplo-e2e.md`: lectura guiada de las 7 etapas del piloto de churn (pregunta, rol de usuario y agente, archivo producido, extracto real y evidencia del gate), con el hallazgo crítico de leakage de diagnosis y los límites. Verificado en una copia del piloto: los 7 gates dan PASS y el estado es COMPLETED/integrity OK; enlaces, anclas y archivos citados comprobados. Enlazada desde README (sección 4, sección 5, contenido y documentación). No es un script reproducible: el trabajo de las etapas lo hizo un agente en sesiones anteriores.

## 2026-10-14 — publicación de 0.1.1 en PyPI

Versión 0.1.1 (`pyproject.toml` y `acos.__version__`; 264 PASS) publicada con `uv publish` a petición de David, usando el token que él proporcionó en la sesión (pasado por variable de entorno, no guardado en archivos). Índice verificado: wheel `3653ffcbb1809f49e05f52bcd82529b2eb49afbd4fdc2f14670a10250b7eecf3`, sdist `64b15c78bf93a97a88686b2558b8606dfe4f1308b30c326dd2cce95a87f985f1`, `license: MIT`; instalación desde PyPI en venv limpio, `acos --version` 0.1.1 y `acos init`/`status` correctos. Cambios frente a 0.1.0: licencia MIT, README reescrito y fallback `metadata:`. 0.1.0 permanece en el índice (inmutable). El token sigue activo por decisión de David; recomendación vigente: revocarlo o reemplazarlo por uno limitado a este proyecto.
