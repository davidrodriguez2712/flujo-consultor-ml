# Balance después de los pilotos de churn y crédito

Fecha: 2026-10-08. Análisis local para orientar la continuación. No cambia decisiones, fichas ni madurez del Foundry.

## Resultado del recorrido

Los dos laboratorios sintéticos están cerrados. El recorrido permitió producir contratos, análisis, baseline, validación, entregables y handoff, con aprobación humana por etapa y snapshots experimentales. Crédito se reprodujo en otra carpeta del mismo macOS/Python, conservando 19 archivos de resultados y metadata salvo timestamp.

Esto demuestra ejecución local de esos recorridos. No acredita eficacia general de las skills, uso crediticio real, efecto causal de retención/revisión ni validación nativa de Windows. Churn incluye una comparación exploratoria de design-validation; crédito aplicó manualmente las pautas existentes.

Fuentes: [feedback de churn](../../../pilots/churn-retencion-sintetico/handoff/capability_feedback.md), [feedback de crédito](../../../pilots/riesgo-credito-sintetico/handoff/capability_feedback.md), [cierre de crédito](../../../pilots/riesgo-credito-sintetico/handoff/closure.md) y [verificación del cierre](../../../pilots/riesgo-credito-sintetico/reports/handoff/closure-verification.json).

## Contraste con candidates canónicos

Se leyeron las fichas actuales directamente en David Skill Foundry. Los nombres de archivo de esta tabla son relativos a `candidates/` del Foundry; no se copiaron ni modificaron. Su metadata conserva `status: candidate`, mientras que sus decisiones humanas indican mantener como conocimiento. El cierre de los proyectos no revoca esas decisiones.

| Candidate existente | Evidencia adicional local | Qué permite concluir | Tratamiento recomendado |
|---|---|---|---|
| `2026-10-04-acos-validate-delayed-outcome-targets.md` | Disponibilidad temporal necesaria en ambos pilotos; crédito detectó 455 labels disponibles después del cutoff de fit | Hay necesidad metodológica en fixtures sintéticos. No se observó admisión indebida en el pipeline aprobado | Conservar contrato/checks y pautas actuales; no reabrir una extensión por mera recurrencia sintética |
| `2026-10-04-acos-evaluate-operational-selection.md` | Churn distingue riesgo de beneficio; crédito separa concedidas evaluables de Top-100 global con coverage 22–26% | Las métricas dependen de población y observabilidad. No se identifican métricas globales ni beneficio causal | Conservar playbook/contrato; contrastar con evaluate-ranking antes de cualquier nueva ficha |
| `2026-10-04-acos-synthesize-evidence-to-recommendation.md` | Memos con límites y trazabilidad; crédito documenta ocho claims y comprueba 65 campos JSON | El proceso produjo un memo verificable en este laboratorio. No hay comparación que atribuya mejora a una skill de delivery | Mantener playbook/template y comprobaciones de claims; reabrir solo con fallo respaldado |
| `2026-10-04-acos-evaluate-probability-calibration.md` | Crédito reporta bins y desajustes; no certifica calibración aunque Brier mejora | Discriminación/Brier favorables no bastan para certificar probabilidades o decisiones económicas | Mantener conocimiento y diagnóstico explícito; no crear calibrador ni nueva skill automáticamente |
| `2026-10-04-acos-design-human-review-policy.md` | Capacidad de 100 revisiones/mes, benchmark retrospectivo; falta definir política de llegada online | Una capacidad nominal no completa política, latencia, revisión ni efecto de acción | Definir contrato operacional cuando exista engagement; no se observó subdimensionamiento que reabra el candidate |

Los candidates temporales y de calibración contienen decisiones posteriores de mantener como conocimiento, además de secciones anteriores que proponen experimentar. La decisión humana posterior manda para este análisis. Una futura revisión canónica debe aclarar la vigencia sin borrar historia; no se interpreta la sección antigua como autorización actual.

## Evidencia comparativa ya disponible

- [Ronda temporal 03](2026-10-08-temporal-contract-round-03-report.md): empate en campos y decisiones evaluados; diferencias exploratorias de preguntas no demuestran eficacia. No repetir rondas automáticamente buscando ventaja.
- [Selección operacional 02](2026-10-08-operational-selection-round-02-report.md): ambas condiciones aciertan los checks estructurados; existen defectos de texto en ambas. El suplemento no mostró ventaja estructurada en estos cases.
- Los pilotos añaden aplicación E2E, no una comparación controlada del efecto de cada capacidad. Métricas de los modelos no son métricas de eficacia de las skills.

## Prioridades para continuar

| Orden | Trabajo | Qué falta / criterio de entrada |
|---|---|---|
| 1 | Completar la evidencia de portabilidad en Windows nativo | Host Windows disponible y ejecución del recorrido documentado; conservar logs y checks. No sustituirlo por simulación de rutas o macOS |
| 2 | Intake de un engagement con contexto/datos independientes | Decisión, owner, datos accesibles y permisos; también puede comenzar por Discovery sin datos, declarando bloqueos de análisis |
| 3 | Revisar un fallo observado antes de cambiar capacidades | Expediente concreto, output incorrecto, expected verificable y contraste con cobertura existente; decidir conocimiento, template/playbook, extensión, skill o agent |
| 4 | Mejoras de cobertura del código de laboratorio si va a reutilizarse | Nueva versión y pruebas, preservando fuentes y freezes aprobados; los Minor documentados no son fallos observados |

## Recomendación inmediata

Completar Windows nativo como siguiente hito del producto portable, si hay un host disponible. El recorrido existe en [windows-check.md](windows-check.md); se requiere evidencia de ejecución, no otra plantilla.

Si no hay host, avanzar con la definición del próximo engagement y sus inputs, manteniendo Windows pendiente. No hace falta generar otro laboratorio sintético para declarar más madurez ni crear nuevas capacidades por defecto.

Para el Foundry, preparar la transferencia de referencias/feedback únicamente cuando se decida una revisión concreta y con autoridad para escribir en su fuente canónica. Este balance ya identifica las fichas pertinentes y evita duplicarlas; no abre una evaluación ni autoriza gasto API.

## Actualización posterior — Windows mediante GitHub Actions

La prioridad de ejecución nativa de CLI se completó para Windows Server2022x64/Python3.11.9:125tests,24simulaciones/164checks y12comandos del smoke aislado. [Resultado y alcance](2026-10-08-github-actions-windows-report.md). Windows11/ARM y harnesses no verificados. La siguiente iniciativa recomendada es intake de un engagement independiente; no más rondas sintéticas para buscar mejora de skills.

## Actualización posterior — Windows 11 ARM y runtimes

Por elección de David, se priorizaron Windows 11 ARM y los runtimes nativos. La matriz pasó en Windows x64 y Windows 11 ARM64: 125 tests, 24 simulaciones y 12 comandos de smoke por plataforma. Codex y Claude Code descubren una fixture de skill local antes y después de mover el workspace. [Evidencia](2026-10-08-windows-arm-runtimes-report.md). Conversación real, invocación y continuidad con modelos en Windows siguen pendientes de autenticación y autorización de consumo. No se abre otra evaluación del Foundry por estos resultados.

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
de capacidades ante fallos observados. [Evidencia y límites](2026-10-09-windows-authenticated-report.md).
