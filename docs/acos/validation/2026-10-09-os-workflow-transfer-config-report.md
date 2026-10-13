# Transferencia — controles y configuración preparados

## Estado

David aprueba paquete de seis casos y diseño acotado mediante «aprobado». Aprobación registrada contra manifest de preparación fuera del freeze. Ajuste de transporte/checker implementado y verificado localmente. **Presupuesto y ejecución pagada siguen sin autorizar.**

## Cambios

- `workflow_native_transport.py`: `invoke(..., system_prompt=...)` permite prompt neutral explícito; default JSON anterior conservado. Para transferencia se usa el mismo prompt neutral en smoke y doce celdas. Envelope CLI sigue JSON; texto de modelo puede ser JSON o Markdown sin reparar.
- Nuevo `workflow_transfer_checker.py`: delega JSON al checker existente; Markdown valida los cinco H2, estado, ausencia de prefacio/fences envolventes y referencias locales. Acepta énfasis en estado y fences internos con cierre; no convierte estructura/citas existentes en aceptación semántica.
- Extracción de rutas limitada a `.md`/`.json` locales en Hallazgos; existencia y soporte se separan. Ausencia de referencias se registra y exige revisión del contenido. No parser universal ni independencia acreditada.

## Verificación

TDD: 17 tests nuevos fallan por funciones ausentes; después 28 tests de transporte/checkers PASS. Suite completa **182 passed**, 5,79s; sin failures ni skips, proveedores simulados y HTTP localhost. Tests ejecutan checker real, su CLI y preservación de raw; proceso nativo se simula para evitar gasto. No prueban eficacia de pautas ni compatibilidad real del proveedor.

Checks finales PASS: 50 archivos de preparación, 13 archivos de configuración, 253 históricos y snapshots actuales intactos. Checker congelado funciona con siblings congelados. Cero calls API y US$0 adicionales. Foundry sin cambios ni promociones.

## Configuración propuesta y consumo

Claude Code2.1.296, `claude-haiku-5-5`, effort low, cap8192 incluyendo thinking, un request por invocación, trece máximo: smoke Markdown + doce celdas. Sin tools/MCP/skills, proceso/cwd nuevos y settings deshabilitados conforme al runner revisado. Aislamiento/compatibilidad reales pendientes de smoke; no sandbox OS nuevo.

Tarifas verificadas el2026-10-09: Haiku5.5 hasta100kinput US$0.10/MTok entrada, US$0.50/MTok salida; cachewrite5m US$0.125/MTok y cacheread US$0.01/MTok. Tier mayor: entradaUS$0.50 y salidaUS$2.50. [Pricing oficial](https://platform.claude.com/docs/en/about-claude/pricing), [migración y thinking](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide).

Propuesta: **hastaUS$0.10 adicionales para este estudio**, no saldo transferido. Estudio anterior US$0.02065453 estimados se registra separado. El coste anterior sirve solo de referencia (~US$0.02), no predicción garantizada. Proxy reserva antes de enviar con tier conservador y cap; probes públicos por request US$0.04159–0.04472, y request real se recalcula con wrappers CLI. La reserva se libera parcialmente al liquidar usage conocido. Si el saldo no cubre la siguiente reserva, se detiene; el límite puede dejar pares incompletos. No garantizar completar todo a consumo máximo, ni factura/impuestos.

Freeze configuración SHA-256: `69529a3f59f7eb3c214a5ebfaa64b8a0e50610f1a366efdd6493443b0b6601a4`.

[Configuración](../../../evaluations/os-workflow/2026-10-09-transfer-01/execution-config-01/config.json) · [Runbook](../../../evaluations/os-workflow/2026-10-09-transfer-01/execution-config-01/RUNBOOK.md) · [Checks finales](../../../evaluations/os-workflow/2026-10-09-transfer-01/configuration-final-checks-01.json).

## Pendientes

Autorización de gasto contra este freeze; preflight final y smoke real; doce respuestas; revisión semántica/matriz exploratoria. Un formato incorrecto se conserva y puntúa, sin retries ni reparaciones. Fallos de transporte/usage/modelo/stopreason/integridad detienen calls. Expected históricos quedan intactos. No eficacia general ni promoción Foundry por estos controles.
