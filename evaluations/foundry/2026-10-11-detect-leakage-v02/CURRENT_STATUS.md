# Estado actual — detect-leakage 0.2.0

2026-10-12: ronda cerrada, revisión independiente completada y canonical actualizado a **0.2.0 experimental supervisada**. No implica validated/stable ni superioridad demostrada.

- Microprueba: 15 salidas, cinco por condición. 0.2.0 respeta 180 palabras en5/5;0.1.0 en0/5. Ambas guías atienden la tarea con reservas; sin guía falla el contenido en5/5. Prueba textual, no instalación nativa.
- Tres pares nuevos: disponibilidad tardía, identidad legítima y fit global. Contenido observable correcto tanto baseline como treatment; no mejora incremental demostrada. Dos regresiones suplementarias correctas con reservas; revisadas por agente distinto del autor/runner.
- Native: L01 completo con Skill, pero contrato y longitud FAIL; L02 truncado sin reporte; L03 no ejecutado. Error403final es local después de la truncación, no credencial del proveedor inválida.
- Verificación local:233PASS, inputs intactos y36hashes de9reportes válidos. Metadata root canónica Foundry no pasa quick_validate estricto de Codex; compatibilidad formal pendiente.
- Coste estimado acumulado Anthropic:US$0.09112648,83solicitudes; saldoUS$0.00887352 de techoUS$0.10. API detenida; no reintentos de pago automáticos. Consumo de subagents de Codex no medido por este ledger.
- `canonical-update-01.json` registra before/afterSHA y límites. Canonical0.2.0SHA:c2a2440477d9985489b71f4d8c50380ccd7985635d02eab330cfee0f7e5856c4. Snapshot0.1preservado. No se actualizan automáticamente proyectos históricos ni runtimes globales.

## Pendiente

1. Contrato nativo: claves exactas, campos completos por hallazgo y longitud; el runner debe rechazar incumplimientos sin reparar outputs originales.
2. Completar L02/L03 nativos y comparación nueva con condiciones iguales. Requiere presupuesto adicional explícito; no gastar por encima del techo actual.
3. Escenarios menos guiados y juicio humano antes de cambiar madurez. Experimental requiere revisión de cada reporte y supervisión de acciones.

Informe: `docs/acos/validation/2026-10-12-foundry-detect-leakage-v02-report.md` en ACOS. Evidencia detallada: `MICRO-REVIEW.md`, `independent-review-02.md`, `checks-final-01.json`, `verification/`, configs, ledgers y reportes originales.
