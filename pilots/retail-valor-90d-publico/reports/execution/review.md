# Execution — paquete para revisión

Diagnosis y data-quality aprobados por David. Contratos y representación JSON aprobada fijados mediante hashes. Fuente original conservada y sin cambios en Foundry/snapshots de skills.

## Dataset temporal

14 cutoffs en total: 13 snapshots train/development (39.677 filas) y un holdout reservado (2.768 clientes). 788.187 compras válidas. 22.523 copias entre hojas y 256.661 líneas excluidas conservadas con motivo/provenance. Snapshot no altera fuente y mantiene repeticiones internas.

Checks: límites semiabiertos, historia180d/horizonte90d completos, key cliente×cutoff, features finitas, madurez label_end<=fit. Clientes compartidos intencionales, no nuevos clientes. Ventanas/motivos/resultados en snapshot_checks.json. Outcomes holdout construidos y sometidos a checks de integridad/ventanas, sin métricas ni inspección de importes de desempeño.

## Development

Métrica: suma de ventas válidas futuras observadas entre Top-100; cuatro horizontes no solapados, misma población por período.

| Método | Ventas Top-100 agregadas GBP | Frente al baseline | Períodos por debajo |
|---|---:|---:|---:|
| Ventas históricas90 (baseline) | 2.606.803,55 | — | — |
| Ridge log | 2.217.514,29 | -14,93% | 4/4 |
| HistGradient log | 2.487.103,96 | -4,59% | 4/4 |
| RFM (informativo) | 2.160.776,71 | -17,11% | 4/4 |

16 ejecuciones locales (cuatro métodos × cuatro períodos), 49.132 scores. Dos modelos fijos, sin tuning ni selección de features. Ninguno cumple aceptación development; implicación preliminar: baseline. No entrenar nuevas variantes para intentar ganar ni seleccionar por holdout. No afirmar superioridad universal del baseline o efecto causal de contacto.

## Auditoría y pruebas

35 tests pasan: source9, temporal11, modelos11, runner4. RED→GREEN observado por módulo ausente y check adicional de manipulación de representación del contrato. Se corrigieron fixtures que carecían del nuevo hash obligatorio, sin relajar control. Logs históricos conservados.

build-features produjo plan de señales; implementación posterior por tarea3. detect-leakage inspeccionó pipeline antes de entrenar. No leakage confirmado en código revisado; disponibilidad/latencia real permanece no determinable. Scaler fit solo train, target/ID/fechas fuera de features; test alterar target scoring no cambia score.

## Pendiente de aprobación

Gate Execution requiere revisión humana del dataset, auditoría y development. Tras aprobación: congelar selección baseline según contrato y evaluar holdout histórico una sola vez; después revisión de Validation y gates técnicos. El holdout permanece bloqueado en el runner hasta implementar paso autorizado.

Gasto API US$0. La suma monetaria representa ventas observadas de clientes seleccionados, no ventas incrementales, beneficio ni ROI.
