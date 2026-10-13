# Adaptación acotada propuesta para runner existente

## Necesidad comprobada

workflow_native_transport.py usa safe-mode, desactiva skills/tools y fuerza una solicitud por invoke. runtime_budget.prepare rechaza herramientas para Haiku5.5. No ejecutar casos Foundry con esos defaults: impedirían inspección/persistencia y native skill. Windowsauthenticatedprobe ya tiene flujo de runtime con herramientas/múltiples solicitudes; reutilizar controles que correspondan, sin cambiar sus resultados históricos.

## Cambios propuestos antes de configuración ejecutable

Agregar opción opt-in de tools locales al proxy, con whitelist estricta y validación de schemas/nombres; defaults text-only intactos. Agregar transporte local de evaluación para skill, reutilizando reserva/usage del proxy y soporte multipaso del probe, sin modificar snapshots previos. Permitir tool_use intermedio y exigir respuesta terminalend_turn con usage conocido y cada request reservado. No considerar cada paso normal de herramientas un retry; ningún intento fallido se repite automáticamente. Herramientas remotas/subagents fuera del whitelist.

Runtime propone restricted/dontAsk, settings explícitos y configdir aislado; sin safe/bare por los descubrimientos locales. Plugin explícito conserva bytes del snapshot. Baseline y treatment reciben la misma tarea, tools y permisos; solo treatment dispone del plugin. Baseline no debe afirmar skill cargada. Para treatment exigir evento real Skill con nombreacos-eval:detect-leakage. Descubrimiento no sustituye invocación ni uso efectivo.

Utility local fija con stdlib devuelve hechos genéricos de inputs (hashes/conteos/timestamps), sin expected ni conclusiones de leakage. Bash solo tiene permiso para ese comando exacto. Read limita inputs/case/skill, Write limita reporte nuevo. Denegar reviewer y escrituras a inputs/config. No permitir Bash arbitrario ni depender de prompt para aislamiento; validar permisos con intentos negativos y revisar que los paths fuera del workspace no estén accesibles. Si políticas efectivas no se pueden demostrar, parar y diseñar un control verificable antes de paidcall. No afirmar sandboxOS a partir de restricted.

## Comprobación local propuesta

Verificar defaults anteriores rechazan tools; opt-in acepta solo el conjunto local y rechaza remote/MCP/subagents/modelo distinto. Proveedor simulado de dospasos comprueba request→tooluse→resultado→end_turn, límites y reserva/usage. Probar lectura/escritura restringidas, persistencia/no sobrescritura, ausencia de expected/credenciales en cwd/contexto, hash del snapshot y diferenciación de discovery/invocation. Estos checks validan infraestructura, no eficacia de skill.

## Límites de coste

Propuesta nueva hastaUS$0.10total, todavía no autorizada. Siete invocacionesmáximo: smoke+seis cases, hasta8solicitudes cadauna y56globales; no retries. Timeout y stop antes de proveedor por presupuesto/reserva/requestcount. Uso desconocido retiene reserva y detiene; modelo distinto/salida truncada/permissionfailure/runtimefailure detienen. Si presupuesto no permite completar, conservar pares incompletos, sin señal favorable sobre plan entero. Congelar implementación/config antes de solicitar ejecución pagada contrahash.

## Alcance y revisiones

Este diseño es documental, no código implementado. Requiere aprobación según superpowers:brainstorming antes de cambiar comportamiento del runner. La autorización de preparación recibida no aprueba gasto. No modificar Foundry/madurez, expected ni evidencia histórica. Regla del paquete concreta requiere aceptación humana antes de evaluación. Reviewer diferente del autor pendiente; sin él, reviewautor explícita no acredita independencia.

## Referencias oficiales verificadas

- Skills y permisos Skill(name): https://code.claude.com/docs/en/skills
- CLI, max-turns y flags: https://code.claude.com/docs/en/cli-reference
- Permisos y alcance: https://code.claude.com/docs/en/permissions
- Tarifas Haiku5.5: https://platform.claude.com/docs/en/about-claude/pricing

Los probes locales son evidencia de descubrimiento en CLI2.1.296. No atribuir a documentación una garantía de aislamiento, coste o compatibilidad no comprobada.
