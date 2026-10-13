# Regresión nativa real — detect-leakage 0.2.0

Fecha: 2026-10-12. Usuario aprobó hasta US$0.05 adicionales, elevando el techo acumulado del estudio a US$0.15. Se ejecutaron dos configuraciones distintas, conservadas por separado.

## Qué ocurrió

La configuración02 ejecutó L01 y L02 con Claude Code real y API Anthropic. L01 pasó runtime y contrato. L02 terminó y persistió su reporte, pero omitió las líneas `---` del frontmatter. El checker lo rechazó y el coordinador se detuvo; L03 no se ejecutó en esa ronda. No se reparó el archivo.

Se reprodujo la ausencia de un ejemplo literal en el prompt transmitido. La corrección acotada añade ese esquema al prompt común, sin modificar skill, cases, expected, workflow, permisos, guards o caps. Test de transmisión RED→GREEN y suite completa: **262 PASS, cero fallos, 18.00 segundos**, con proveedor simulado. La revisión de configuración confirmó el alcance del cambio.

La configuración03 repitió L01–L03 con ese prompt. Las tres ejecuciones completaron runtime, invocaron la skill nativamente, persistieron el reporte y pasaron el contrato mecánico. No hubo reintentos pagados automáticos; la segunda ronda fue una ejecución nueva tras diagnosticar y verificar una corrección.

## Resultados separados

| Configuración/caso | Runtime | Contrato mecánico | Palabras reporte/final | Revisión semántica independiente |
|---|---|---|---:|---|
| 02 / L01 | PASS | PASS | 444 / 58 | Esencial correcto, reservas de cobertura y campos |
| 02 / L02 | PASS | FAIL: frontmatter ausente | 425 / 73 | Esencial correcto, reservas; entrega bloqueada |
| 02 / L03 | No ejecutado | No evaluable | — | No evaluable |
| 03 / L01 | PASS | PASS | 381 / 43 | Útil con reservas |
| 03 / L02 | PASS | PASS | 455 / 60 | Útil con reservas |
| 03 / L03 | PASS | PASS | 422 / 65 | No aceptado íntegramente |

Límites: reporte≤500 palabras completas por whitespace y final≤80 incluida ruta. La revisión es de un agente distinto del autor/runner, no humana ni ciega. El reviewer de03 conoce la ronda02. Los juicios detallados y sus reservas se conservan en cada `REVIEW-REAL-01.md`.

## Fallo semántico pendiente

L03 declara incertidumbre, pero también sobreafirma que la feature no es válida y propone que un conteo «con fecha de exportación» confirmaría leakage. Una fecha de exportación no demuestra por sí sola la ventana de los hechos ni la disponibilidad efectiva. También comprime un hallazgo secundario sin todos sus campos. La revisión no convierte estos puntos en PASS porque el wrapper sea válido.

L01/L02 conservan reservas: cobertura y campos de hallazgos secundarios, precisión de evidencia, acciones de reconstrucción y severidades atribuidas a limitaciones. Las preguntas no deben negar lo ya declarado en el expediente ni exigir escenarios diferentes como condición de validez del actual.

La siguiente mejora debe expresar para una conclusión no determinable qué evidencia permitiría confirmar o descartar el mecanismo y qué acción provisional corresponde. Eso requiere una hipótesis y prueba nuevas antes de modificar la skill canónica. No se añadieron soluciones a los expected ni se alteró retrospectivamente el criterio.

## Coste

| Etapa | Requests reales | USD estimados |
|---|---:|---:|
| Acumulado previo | 83 | 0.091126480 |
| Configuración02 real | 8 | 0.010226740 |
| Configuración03 real | 12 | 0.013749825 |
| **Acumulado** | **103** | **0.115103045** |

Saldo del techo aprobado US$0.15: **US$0.034896955**. Gasto nuevo de estas dos rondas: US$0.023976565. Todos los usages conocidos; HTTP200 y sin truncación en estas dos rondas. Cifras estimadas por ledger, no factura; corresponden al proveedor Anthropic. No incluyen consumo de Codex del coordinador/reviewer.

La clave real se carga únicamente tras verificar manifest, approval, CLI, output nuevo y saldo; el CLI recibe un placeholder local. No se guarda ni imprime la clave. Cada proxy usa el saldo explícito de su aprobación y cierra solicitudes ante fallo.

Reserva de nomenclatura: `config.json` conserva `budget_ceiling_usd: 0.1`, cota fija que acepta el verificador por paquete. El proxy usa `approved.total_budget_usd`, no esa constante como autorización de gasto. El launcher comprobó prior+saldo=US$0.15 antes de cargar la clave. No existe un tracker global concurrente del estudio; esta ejecución es secuencial y sus saldos se calculan desde ledgers. La ambigüedad del nombre se registra sin modificar paquetes ya ejecutados.

## Decisión

Regresión técnica y de contrato completada en03. **Calidad semántica todavía incompleta.** Mantener `detect-leakage 0.2.0 experimental` y supervisión. No promover a evaluated, validated o stable. Esta es una regresión treatment-only; no demuestra superioridad causal frente al baseline ni generalización.

Se detienen las llamadas de pago tras03. El saldo no es una obligación de consumirlo ni convierte un fallo en motivo para repetir la misma configuración hasta obtener PASS.

## Integridad y evidencia

Se verificaron hashes de prompts/reportes, manifests históricos y skill canónica. Canonical sigue con SHA-256 `c2a2440477d9985489b71f4d8c50380ccd7985635d02eab330cfee0f7e5856c4` y sin cambio de madurez. Los datos, expected y reportes anteriores permanecen intactos.

- Config02: `evaluations/foundry/2026-10-12-native-regression-preparation-02/`, approval nuevo y `runs/real-01/`; preparación/simulación histórica preservada.
- Config03: `evaluations/foundry/2026-10-12-native-regression-config03/`, manifest de ejecución `6ea839f67965ae100c51daedabb66376b4dfd7e082789ba72d2160bc4e0bedae`, approval, prompts, contratos, reportes, raw stdout, ledgers, reviews y `CLOSURE_CHECKS.json`.

## Pendientes

1. Refinar y evaluar incertidumbre, criterios de confirmación/descarte y acciones proporcionales, sin adaptar expected a los outputs.
2. Comparación nueva con baseline y escenarios menos guiados antes de atribuir mejora a la skill.
3. Compatibilidad formal del template Foundry y adjudicación humana antes de cambiar madurez.
