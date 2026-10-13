# Windows 11 ARM y runtimes nativos

Fecha local: 2026-10-08, America/Lima. Ejecución exitosa el 2026-10-09 04:02–04:04 UTC.

## Resultado por prioridad

**Prioridad 3: recorrido de ACOS completado en Windows 11 ARM64.** Se utilizó el runner real `windows-11-arm`, con Python ARM64 y dependencias nativas; no emulación desde macOS ni Docker.

**Prioridad 2: instalación, arranque y descubrimiento local completados para Claude Code y Codex en Windows x64 y ARM64.** La conversación autenticada, la invocación de una skill por el modelo y la continuidad con `continuemos` siguen pendientes. Descubrir una skill no demuestra que el modelo la aplique correctamente.

[Ejecución exitosa](https://github.com/davidrodriguez2712/agentic-consulting-os/actions/runs/37882006292), commit `5b52a83e196e304a8b4fb1663802c0cba6261aeb`. ACOS conserva versión 0.1.0.

| Comprobación | Windows Server 2022 x64 | Windows 11 ARM64 |
|---|---|---|
| Python nativo | 3.11.9 / AMD64 | 3.13.16 / ARM64 |
| Suite | 125 passed, sin failures/errors/skips | 125 passed, sin failures/errors/skips |
| Simulaciones del compiler | 24 casos / 164 checks | 24 casos / 164 checks |
| Wheel instalado en venv fuera del checkout | PASS | PASS |
| Smoke de ACOS | 12 comandos con exit codes esperados | 12 comandos con exit codes esperados |
| Codex 0.160.0 | Ejecutable PE x64; arranque PASS | Ejecutable PE ARM64; arranque PASS |
| Claude Code 2.1.294 | Ejecutable PE x64; arranque PASS | Ejecutable PE ARM64; arranque PASS |
| Skill local antes/después de traslado | Ambos runtimes PASS | Ambos runtimes PASS |
| Conversación y continuidad con modelos | Pendiente | Pendiente |

Cada job tardó 2 minutos 23 segundos. El smoke incluye creación, rutas con espacios, traslado, status/next/validate, conservación de archivos con `--here` y rechazo de colisiones. No cubre todos los recorridos del wizard.

## Cómo se comprobó el runtime

El probe genera un workspace mediante el compiler y añade una fixture desechable `acos-ci-probe` en `.agents/skills/` y `.claude/skills/`. La fixture no es una capacidad del Foundry ni se copia al producto.

- Codex: `app-server` recibe `initialize`, `initialized` y `skills/list`. Se verifica nombre y ruta de la skill dentro del workspace.
- Claude Code: la inicialización del protocolo SDK recibe únicamente un `control_request` de `initialize`. Se verifica la presencia de la skill en los comandos disponibles, sin enviar mensajes de usuario.
- Se termina cada proceso, se mueve el proyecto a una ruta con espacios y se repiten ambas comprobaciones.
- Se inspecciona el encabezado PE de los binarios y se ejecuta directamente el correspondiente a la arquitectura del runner.

Las comprobaciones usan mecanismos documentados en [Codex app-server](https://learn.chatgpt.com/docs/app-server), [skills de Claude Code](https://code.claude.com/docs/en/skills) y el [protocolo del SDK oficial de Anthropic](https://github.com/anthropics/claude-agent-sdk-python/blob/main/src/claude_agent_sdk/_internal/query.py). La instalación nativa por npm y sus plataformas están descritas en [Claude Code setup](https://code.claude.com/docs/en/setup). GitHub ofrece estos [runners ARM64 para repositorios privados](https://github.blog/changelog/2026-01-29-arm64-standard-runners-are-now-available-in-private-repositories/).

**Cero turns de modelo en esta ronda.** No se configuraron credenciales de modelos en GitHub ni se trasladaron sesiones de macOS. El estado sin autenticación se comprobó con los comandos locales de ambos runtimes. Las descargas de paquetes y GitHub Actions sí utilizan red; no se midió su coste.

## Fallo observado y corrección

El [primer intento](https://github.com/davidrodriguez2712/agentic-consulting-os/actions/runs/37881558139) pasó suite, simulaciones, build, instalación aislada y arranque de runtimes en ambas arquitecturas. Falló al trasladar el workspace: terminar `codex.cmd` dejó un proceso hijo abierto y Windows rechazó el movimiento con WinError 32.

Se corrigió el probe para lanzar directamente el ejecutable nativo de la arquitectura esperada y terminar ese proceso. También se añadió la comprobación de descubrimiento de Claude. El segundo intento pasó el traslado y el redescubrimiento en ambos runtimes. No se modificó el compiler para resolver este fallo.

## Reproducción y evidencia

Workflow manual: [windows-runtime-validation.yml](../../../.github/workflows/windows-runtime-validation.yml). Probe: [windows_runtime_probe.py](../../../scripts/ci/windows_runtime_probe.py).

```sh
gh workflow run windows-runtime-validation.yml --repo davidrodriguez2712/agentic-consulting-os --ref main
gh run watch <run-id> --repo davidrodriguez2712/agentic-consulting-os --exit-status
gh run download <run-id> --repo davidrodriguez2712/agentic-consulting-os --dir <carpeta-nueva>
```

Los artifacts remotos caducan a los 14 días. Ambos intentos se descargaron localmente:

- [Verificación de resultados](../../../artifacts/windows-arm-runtimes-2026-10-08/verification.json).
- [Metadatos del run exitoso](../../../artifacts/windows-arm-runtimes-2026-10-08/run-02-metadata.json).
- [Inventario SHA-256 de 53 archivos](../../../artifacts/windows-arm-runtimes-2026-10-08/evidence-manifest.json).
- Logs, JUnit, dependencias, wheels y resultados completos bajo `artifacts/windows-arm-runtimes-2026-10-08/run-01/` y `run-02/`.

Se verificó que la evidencia de la ronda Windows anterior y los dos manifests de Handoff de crédito permanecen intactos. No se modificó Foundry ni se promovieron capacidades.

## Pendiente concreto

Para completar la prioridad 2, configurar autenticación autorizada y un límite de consumo, y ejecutar una sesión breve por runtime que invoque una skill del proyecto y retome el estado con `continuemos`. Conservar transcript, outputs y checks de lectura/escritura del workspace. No iniciar esta prueba mientras la autorización de autenticación y consumo esté pendiente.

Esta ronda tampoco acredita un piloto real de consultoría en Windows, toda combinación de versiones de Python, ejecución de herramientas shell dentro del sandbox del modelo ni eficacia de las skills. La portabilidad del software y el descubrimiento local cuentan con evidencia específica por plataforma.

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
