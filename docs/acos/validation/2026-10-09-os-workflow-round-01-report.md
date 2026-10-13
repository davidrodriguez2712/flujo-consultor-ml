# Primera ronda real: smoke PASS, benchmark detenido

## Resultado

Presupuesto aprobado: hasta US$0.20 acumulados. Clave Anthropic proporcionada por David en `.env`, leída exclusivamente para el proxy, sin mostrarla ni persistirla en evidencia. `.env` excluido mediante `.gitignore`.

Claude Code se actualizó a 2.1.296; los flags fueron revisados y el cambio patch registrado como amendment local fuera del freeze original. Smoke técnico PASS: un request, modelo exacto, usage conocido y JSON conforme. No hubo tools ni MCP en la configuración utilizada. Esto verifica transporte observable; no constituye sandbox OS ni evaluación de eficacia.

La primera celda E01-baseline no produjo resultado utilizable. Consumió **2.048 tokens de salida**, incluyendo 590 de thinking. El CLI intentó otra solicitud y el proxy la bloqueó **antes de enviarla**, conforme al único request permitido por invocación. El CLI terminó con error y se detuvo la ronda sin reintentos.

Ambas solicitudes enviadas recibieron HTTP200. El mensaje «Failed to authenticate» del CLI corresponde al 403 local de bloqueo de continuación, **no a una clave inválida**. La hipótesis principal es truncación por salida insuficiente; el stop reason upstream no se registró, por lo que no se afirma que se haya demostrado su valor exacto.

## Coste y evidencia

- Smoke: US$0.0000529 estimados.
- Primer intento: US$0.001487275 estimados.
- **Total API estimado: US$0.001540175**; usage completo para ambas solicitudes.
- Una continuación bloqueada sin llamada al proveedor.
- Restante del presupuesto acumulado: **US$0.198459825**.
- Cero parejas comparables; ninguna conclusión sobre mejora de treatment.

[Ledger de gasto](../../../evaluations/os-workflow/2026-10-09-less-guided-01/runs/round-01/budget-ledger.json) · [Diagnóstico](../../../evaluations/os-workflow/2026-10-09-less-guided-01/runs/round-01/diagnostic-review.json) · [Estado](../../../evaluations/os-workflow/2026-10-09-less-guided-01/runs/round-01/round-status.json).

Quince archivos de este intento congelados. Manifest SHA-256: `7cbc09d54baea334f4d712edbd1502089aebeaea1c33e72a85ca407d98ad10b4`. Preparación48, configuración12 y paquete del piloto70 permanecen intactos. No cambios en Foundry ni promoción de capacidades.

## Propuesta siguiente

Preparar un control/configuración nuevos con **8.192 tokens máximos incluyendo thinking**, idénticos para baseline y treatment, manteniendo un request por invocación, salida textual JSON, sin herramientas ni reintentos automáticos. Registrar el stop reason upstream para distinguir truncación de otros fallos del CLI.

Una nueva ronda manual requiere aprobación explícita porque esta ronda se autorizó sin reintentos. Mantener el total acumulado bajo US$0.20, descontando este intento; no reiniciar ledger como si el gasto previo fuese cero. Conservar este fallo y no considerar E01 completamente inédito en otra ejecución. No cambiar expected ni criterios semánticos después del fallo de infraestructura.
