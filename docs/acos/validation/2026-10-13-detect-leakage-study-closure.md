# Cierre del estudio detect-leakage — estado al 2026-10-13

Cierre administrativo con el estado actual. Cero llamadas API nuevas. No es una promoción ni una validación de eficacia.

## Estado final
- **Skill:** `detect-leakage` canónica 0.2.0 sigue **experimental**, para uso supervisado. Los borradores 0.2.1/0.2.2 no se promovieron. El hash canónico `c2a2440477d9985489b71f4d8c50380ccd7985635d02eab330cfee0f7e5856c4` (hasta la migración a `metadata:`, ver implementation-record) está registrado en informes previos; no se re-verificó en este cierre porque el Foundry canónico queda fuera de este repositorio.
- **Presupuesto:** US$0.14019795 de US$0.15 (estimados por ledger, no factura; solo Anthropic, sin Codex del coordinador/reviewer). Saldo US$0.00980205, sin uso previsto. Pago detenido.
- **Tests:** 264 PASS.

## Resultados que sostienen el cierre
| Evidencia | Resultado |
|---|---|
| Regresión nativa 0.2.0, config03 (L01–L03) | runtime/contrato PASS; L01/L02 útiles con reservas; L03 no aceptado íntegramente |
| Micro textual 0.2.0 vs 0.2.2 (5 vs 5) | 5/5 tratamientos aceptables; ambos brazos 5/5 en contrato y ausencia de defectos prohibidos; sin mejora de tasa; cobertura de condiciones más completa en treatment, descriptiva |
| L03 nativo 0.2.2 | runtime PASS; **contrato FAIL (515/500 palabras)**; contenido ACEPTABLE CON RESERVAS según revisión independiente |

## Límites vigentes
- No hay evidencia causal ni generalización: escenarios sintéticos, una ejecución nativa de 0.2.2, solo treatment, un modelo.
- Revisiones hechas por agentes que conocían el propósito; ninguna humana ni ciega.
- La compatibilidad con `quick_validate` se verificó solo con el validador de Codex.

## Cambios de código del estudio
Compilador acepta `status/version` bajo `metadata:` (raíz con precedencia). Canonical, snapshots y pilotos no migrados; borrador compatible en `evaluations/foundry/2026-10-13-detect-leakage-v022/compat-template/`.

## Pendientes abiertos (no bloquean el cierre)
1. Adjudicación humana de David sobre el L03 nativo 0.2.2.
2. Corregir la redundancia que causó 515/500 y probarlo con una corrida nueva (requiere ampliar presupuesto).
3. Comparación baseline vs. treatment con escenarios menos guiados.
4. Decidir si se migra el canónico al formato `metadata:`.
5. Cualquier cambio de madurez exige evidencia nueva y adjudicación humana.

Reabrir el estudio requiere autorización de presupuesto explícita, un manifest congelado nuevo y no reutilizar aprobaciones previas.
