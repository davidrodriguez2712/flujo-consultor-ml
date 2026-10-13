# Task concreto — configuración preparada para aprobación

## Estado

**READY_FOR_PACKAGE_CONFIGURATION_BUDGET_REVIEW**. Usuario indica «siguiente»; se completa revisión local del paquete y preparación de configuración sin inferir aceptación humana ni permiso de calls. Revisión del autor, no independiente ni ciega.

Cuatro casos/eightpayloads sin cambios. No inconsistencias materiales detectadas en review del autor. Claims del forecast se limitan a metadata, sensores no tienen labels, RAG no permite tickets/APIs y el control exige tres acciones sin task. Rúbrica requiere contenido concreto y acepta propuestas explícitas, sin permisos/thresholds inventados.

## Ejecución propuesta

- Claude Code2.1.296, `claude-haiku-5-5`, effortlow, cap8192incluyendothinking.
- Un smoke técnico Markdown con explicación bajo Estado, separado de benchmark; después ocho invocaciones en orden alternado, una repetición.
- Prompt neutral igual, sesiones/cwd nuevos, no tools/MCP/skills/settings ni contextos privados. No sandbox OS nuevo; compatibilidad real en este estudio pendiente de smoke.
- Checker0.2.0 común, outputs/raw sin reparar; contenido manual con citas y expected congelados, no independiente.
- Sin retries. Stop por infraestructura, usage/modelo/stopreason inesperado, integridad/versiones o budget; error de formato/content se conserva y puntúa.

El helper existente tiene ceiling13, no un límite independiente9. Por eso el runbook exige schedule exacto smoke+ocho celdas únicas y guard `len(entries)<9` antes de cada invoke. Proxy limita un request adicional por invoke. Solicitudes10–13 no autorizadas; no confundir ceiling del helper con alcance permitido.

## Budget propuesto

**Hasta US$0.10 adicionales**, solo este estudio. No transferir saldo de otro. Histórico acumuladoUS$0.04153488 estimados se registra aparte.

Tarifas Haiku5.5 reconsultadas: hasta100kinput US$0.10/MTok entrada y US$0.50/MTok salida; cachewrite5m US$0.125/MTok, read US$0.01/MTok. Tier largoUS$0.50entrada/US$2.50salida. [Pricing oficial](https://platform.claude.com/docs/en/about-claude/pricing).

Quote conservador para bodies públicos US$0.04434–0.04511por request; request real puede incluir wrappers y proxy recalcula antes de proveedor. Esto es reserva, no coste cobrado. Se liquida usage conocido antes de continuar; si siguiente reserva no cabe, detener, pudiendo dejar pares incompletos. No garantía de completar todo a consumo máximo ni factura/impuestos. Aprobación debe referenciar freeze de configuración antes de credencial/proxy.

## Checks y freeze

Checks locales PASS: paquetes, contratos, ocho celdas únicas/schedule, flags/versionCLI, checker con texto sintético y estado con prosa. No API ni suite nueva del producto: código reutilizado coincide con snapshots verificados con189tests en ajuste previo. Checks actuales no prueban eficacia de agentes ni aislamiento real de runtime.

Integridad421archivos históricos y39preparación PASS;12archivos configuración congelados, activos igual a snapshots. SHA256config:

`b8c904441ae6c3e35c15d6a839a10892f8a7142e944d77267c95908382e608b8`

[Configuración](../../../evaluations/os-workflow/2026-10-09-task-draft-01/execution-config-01/config.json) · [Runbook](../../../evaluations/os-workflow/2026-10-09-task-draft-01/execution-config-01/RUNBOOK.md) · [Checks](../../../evaluations/os-workflow/2026-10-09-task-draft-01/configuration-final-checks-01.json) · [Rúbrica](../../../evaluations/os-workflow/2026-10-09-task-draft-01/reviewer/rubric.md).

## Pendientes

Aceptar paquete/expected/configuración y autorizar nuevo budget. Después preflight final, smoke y ocho respuestas con revisión según regla congelada. No ejecutar modelos ni promover Foundry por esta preparación. Producto y Foundry sin cambios; cero calls/APIUS$0 adicional.
