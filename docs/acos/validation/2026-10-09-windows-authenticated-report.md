# Validación autenticada de runtimes Windows — 2026-10-09

## Alcance

Se valida la integración de ACOS con Codex 0.160.0 y Claude Code 2.1.294 en
Windows Server 2022 x64 y Windows 11 ARM64 nativos mediante GitHub Actions.
Se usa un proyecto sintético de churn, sin dataset ni entrenamiento, con estado
canónico validation/BLOCKED y vistas iniciales obsoletas. El identificador del
objetivo es aleatorio y debe obtenerse leyendo el estado, no desde el prompt.

La primera ejecución es guiada. La segunda recibe únicamente `continuemos` en
una sesión nueva. No es resume de una conversación persistida. Se exige que el
workspace permanezca idéntico byte por byte y que el bloqueo por disponibilidad
de labels siga presente. No se autorizan cambios de etapa ni gates.

La skill design-validation 0.1.0 es experimental, con SHA256
`70883c3b75b07334fc95bad1b5c6749fd7b5e623b648f6b48fb6c14b2d32b8f9`.
Se copia el snapshot real al fixture en ambas rutas nativas; esta preparación
manual no evalúa la selección automática del Module Resolver. Codex debe leer
el archivo mediante un comando exitoso y Claude debe invocar Skill con resultado
exitoso. Una afirmación textual del agente no basta.

## Resultados

Las cuatro combinaciones pasan ambas ejecuciones, ocho ejecuciones aceptadas
con exit 0 y workspace sin cambios:

| Runtime | Plataforma | GitHub Actions | Estimación API del intento aprobado |
|---|---|---|---|
| Codex / Luna | Windows x64 | [37889843366](https://github.com/davidrodriguez2712/agentic-consulting-os/actions/runs/37889843366) | US$0.00772443 |
| Codex / Luna | Windows 11 ARM64 | [37890429413](https://github.com/davidrodriguez2712/agentic-consulting-os/actions/runs/37890429413) | US$0.007780755 |
| Claude Code / Haiku | Windows x64 | [37891756918](https://github.com/davidrodriguez2712/agentic-consulting-os/actions/runs/37891756918) | US$0.05479895 |
| Claude Code / Haiku | Windows 11 ARM64 | [37891953156](https://github.com/davidrodriguez2712/agentic-consulting-os/actions/runs/37891953156) | US$0.0667421 |

Suite local final: 144 tests pasan. El intento final de Claude en cada
arquitectura ejecutó además 19 tests del probe/presupuesto, sin errores ni skips.
Codex pasó los 16 tests existentes en sus commits respectivos. No se volvió a
llamar a Codex después de su PASS. Commit final del harness: db8e82d.

Se preservan los 14 intentos de Actions; algunos fallaron antes de llamar al
modelo. El intento 12 de Claude recuperó correctamente el estado pero terminó
por max_turns=6; se amplió a 10 sin relajar el criterio de éxito ni permisos.
La verificación final consta en [final-verification.json](../../../artifacts/windows-authenticated-2026-10-09/final-verification.json).


## Consumo y límites

David autorizó hasta US$1 total para APIs. El proxy local retiene las claves en
memoria, usa credenciales ficticias en los procesos y reserva consumo antes de
cada request. No realiza reintentos propios; ante un rechazo del proveedor
cierra el circuito. Se usan Luna y Haiku, salida máxima de 1024 tokens y cache
Claude de cinco minutos.

Total estimado de APIs **US$0.346215125**, incluidos los intentos fallidos con
usage. Total comprometido conservador **US$0.565150375**, contando también
US$0.21893525 de reservas de requests Claude rechazados sin usage. Ambos están
bajo el dólar autorizado. No habrá llamadas adicionales en este cierre.

Las estimaciones proceden del usage de cada proveedor y las tarifas registradas
en el [protocolo](2026-10-09-windows-authenticated-protocol.md). Las reservas sin
usage se cuentan conservadoramente, pero no acreditan un cargo. El mecanismo no
es un límite de facturación del proveedor y excluye los minutos de Actions.
El [ledger](../../../artifacts/windows-authenticated-2026-10-09/cost-ledger.json)
conserva todos los intentos, incluidos los fallidos.

## Interpretación

Esta prueba acredita integración bajo el fixture y las versiones indicadas.
No acredita eficacia de la skill, calidad de recomendaciones con datos reales,
autoorientación general sin guía, ni promoción de madurez en Foundry.
Los fallos de Claude en los intentos 10 y 11 se conservan: lectura sin invocación
nativa, y posterior invocación sin lectura del estado con objetivo/etapa inventados.
El prompt guiado se hizo explícito sin relajar los criterios de aceptación.

No se modifican capacidades canónicas, pilotos cerrados ni código del producto.
No se publica ACOS en PyPI.

## Siguiente paso

La integración autenticada Windows queda cerrada para estas versiones y este
fixture. La prioridad recomendada es intake de un engagement independiente:
definir decisión, owner, datos disponibles, permisos y entregables. Si no hay
datos, comenzar Discovery y mantener explícitos los bloqueos. Revisar capacidades
solo ante un fallo concreto respaldado; no abrir más rondas sintéticas por defecto.
