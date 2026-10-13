# Configuración de ejecución de la evaluación menos guiada

## Estado

**PREPARED_NOT_EXECUTED**. David aprobó protocolo y expected concretos mediante «apruebo»; la aprobación está ligada al manifest de preparación. No autoriza gasto. Cero llamadas de modelos y US$0 de API en esta preparación.

## Cambios

- Checker local de JSON estricto, contrato, estado esperado y referencias existentes. No repara outputs ni certifica contenido: revisión semántica NOT_RUN.
- Control de presupuesto existente ampliado con selección explícita de `claude-haiku-5-5`, tarifas de ambos tiers, reserva conservadora previa y rechazo de herramientas/recargos. Defaults históricos de Windows conservados.
- Transporte nativo con proceso/cwd nuevos, herramientas y MCP vacíos, safe mode y bare, sin persistencia; uso de un request por invocación y preservación de outputs. API key real únicamente en el proxy. El coordinador verifica autorización antes de credenciales y no continúa tras fallos.
- Configuración propone Claude Code **2.1.295**, Haiku 5.5, effort low, 2.048 tokens incluyendo thinking, un smoke independiente y doce invocaciones en orden alternado. **Hasta US$0.20 total propuesto, sin autorización todavía**; sin reintentos ni fallback.

[Configuración](../../../evaluations/os-workflow/2026-10-09-less-guided-01/execution-config-01/config.json) · [Runbook](../../../evaluations/os-workflow/2026-10-09-less-guided-01/execution-config-01/RUNBOOK.md).

Tarifas verificadas el 9 de octubre de 2026 en [pricing oficial](https://platform.claude.com/docs/en/about-claude/pricing). Thinking adaptativo y compatibilidad según [migration guide](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide). La reserva de bytes más margen es heurística; no se presenta como garantía de factura.

## Verificación local

Tests nuevos observados en RED y después GREEN. La primera invocación con Python del sistema no tenía pytest; se utilizó `.venv/bin/python`. La corrida sandbox encontró tres fallos por sockets localhost no permitidos; repetida con permiso para sockets locales y proveedores simulados:

- Suite completa: **162 passed**, 4,73 s, sin failures ni skips.
- Piloto forecasting: **7 passed**, 0,02 s.
- Verificador de preparación: PASS; seis cases, doce payloads, 24 permutaciones por case de etiquetas.
- Integridad: 48 archivos de evaluación y 70 del paquete de forecasting PASS; hashes de manifests aceptados conservados.
- Snapshots del código/tests coinciden con archivos de trabajo.

[Checks](../../../evaluations/os-workflow/2026-10-09-less-guided-01/execution-config-01/local-checks.json) · [Suite](../../../evaluations/os-workflow/2026-10-09-less-guided-01/execution-config-01/test-suite.txt).

## Freeze adicional

Doce archivos de configuración/control/pruebas congelados por separado. Manifest SHA-256:

`2e8dc56a6c95c15e61189fd59a8b944316b3dc8d88d275ce531e28c8775a85d4`

[Manifest](../../../evaluations/os-workflow/2026-10-09-less-guided-01/execution-config-01/execution-manifest-01.json). La futura autorización de gasto y los runs se registran fuera de este freeze.

## Pendientes y límites

1. Autorización explícita hasta US$0.20 ligada al manifest de ejecución; no reutilizar presupuesto Windows.
2. Disponibilidad segura de API key local, sin asumir que los secrets de GitHub están disponibles en la laptop.
3. Smoke real para comprobar compatibilidad y aislamiento observable del CLI. Tests mocked no acreditan integración con Anthropic; no hay sandbox OS nuevo y políticas administradas aún pueden aplicar.
4. Doce respuestas reales, checker determinista, revisión semántica y comparación de baseline/treatment bajo la regla ya congelada.

Una repetición aporta señal exploratoria; todavía no hay evidencia de eficacia. No se han modificado ni promovido capacidades del Foundry.

## Actualización — presupuesto autorizado y preflight detenido

David respondió «Aprobado» a la propuesta de hasta US$0.20 total para smoke y doce ejecuciones, sin reintentos. Autorización ligada al manifest registrado en [budget-approval.json](../../../evaluations/os-workflow/2026-10-09-less-guided-01/budget-approval.json), fuera del freeze.

Integridad y snapshots PASS. Claude Code instalado ahora es 2.1.296 frente a 2.1.295 del freeze. Los flags requeridos permanecen disponibles; se activó la parada por versión y debe registrarse amendment antes de ejecutar el smoke. No se modificó la configuración congelada.

`ANTHROPIC_API_KEY` no está disponible en el entorno y el proyecto no tiene `.env`. El secret de GitHub no puede recuperarse en texto plano. Se solicitó al usuario un mecanismo local seguro o una ruta a un archivo existente, sin pegar la clave en chat. Pendiente de esa información; no se han hecho llamadas ni gasto. [Preflight](../../../evaluations/os-workflow/2026-10-09-less-guided-01/execution-preflight-01.json).
