# Revisión de Framing

Status: NEEDS_REVIEW. Discovery aprobado por David; Framing no aprobado.

## Decisión y población

Hasta 100 clientes por mes para revisión comercial, ordenados por ventas positivas esperadas a 90 días. Elegibles: cliente con ID y una compra válida en los 180 días anteriores. Todos los países; no afirmar que todos sean consumidores finales. Capacidad/horizonte son supuestos del encargo simulado.

## Reglas propuestas

1. Reconciliar copias entre hojas por las ocho columnas completas, conservando la mayor multiplicidad por patrón observada en una hoja. Mantener las repeticiones internas y el mapa de provenance; no hacer deduplicación general de factura/producto.
2. Compra válida: cantidad/precio positivos y finitos, fecha/IDs presentes, factura no c/C y StockCode con cinco dígitos iniciales seguido únicamente de letras opcionales.
3. Excluir códigos no estándar sin llamarlos inválidos: la regla delimita el target operacional. Incluye cargos de envío y ajustes, pero también líneas ambiguas o potencialmente comerciales. Su relevancia debe quedar visible.
4. Target: quantity × unit_price en [cutoff, cutoff+90 días), solo con horizonte completo. Cero no equivale a churn definitivo.
5. Timestamps originales, sin conversión de zona no documentada. Observabilidad al momento de factura es un supuesto retrospectivo; no certificar disponibilidad real.
6. Ranking y baseline sobre la misma población; score descendente y desempate lexicográfico por ID. Top-K es un benchmark, no política de campaña óptima.

## Impacto preliminar de la propuesta

| Paso | Filas |
|---|---:|
| Fuente original | 1.067.371 |
| Copias coincidentes entre hojas | 22.523 |
| Después de reconciliación propuesta | 1.044.848 |
| Cancelaciones excluidas | 19.165 |
| Cantidad/precio no positivos, después del filtro anterior | 6.029 |
| Código no estándar, después de filtros anteriores | 4.709 |
| Sin ID, después de filtros anteriores | 226.758 |
| Compras propuestas restantes | 788.187 |

Son buckets secuenciales sin doble conteo. Las compras propuestas contienen **5.852 clientes distintos y 41 países** en toda la historia; no significa que todos sean elegibles en cada cutoff. No se guardó un dataset limpio ni se generaron labels.

Los códigos no estándar equivalen a **4.06%** del importe positivo preliminar posterior a reconciliación. Destacan M/Manual (GBP339.614,89), DOT/Postage (GBP309.854,11) y POST/Postage (GBP125.682,42). La exclusión tiene coste de cobertura visible y limita la recomendación a la población definida. No llamar mercancía inválida a una línea solo por su código.

## Lo que esta decisión permite concluir

El KPI medirá calidad retrospectiva de un ranking por ventas positivas de esta definición. No mide ingresos netos, margen, retorno de contacto o CLV completo. La selección no demuestra que una intervención sea beneficiosa.

## Qué requiere aprobación

Aprobar este contrato de población/compra/target/métricas y el supuesto de reconciliación. Después se realizará Diagnosis para revisar calidad, suficiencia temporal y sensibilidad a repeticiones, y congelar cutoffs/aceptación antes de generar snapshots y entrenar. Aprobar Framing no aprueba automáticamente Diagnosis ni modelos.

## Evidencia

- `framing/retail_contract.yaml`
- `framing/framing.yaml`
- `reports/framing/coverage-preview.json`
- `reports/discovery/sheet_overlap.json`
- `reports/discovery/human-approval.json`

## Trazabilidad

Fuentes, auditoría y snapshots intactos. El freeze de Discovery incluía dos planes humanos mutables; al actualizarlos se detectó la discrepancia. Se conservan manifest inicial y planes actuales, se archivan versiones iniciales con SHA256 exacto y se versiona manifest02. Incidente y resolución en reports/framing/freeze-incident.json. Los contratos de Framing se congelarán como copias históricas, separadas de los paths vivos.
