---
skill: build-features
version: 0.1.0
fecha: 2026-10-09
proyecto: retail-valor-90d-publico
inputs:
  - "framing/retail_contract.yaml sha256:0e537ce003ac0c125d89f5a0aa301f3c29a09316f3e90d985a4b82cc642c6ab4"
  - "validation/evaluation_contract.yaml sha256:7c006d5440b88e07e3b04cad040d57775714510695c51ae6a30874c52ab8f83b"
  - "reports/diagnosis/diagnostic-summary.json sha256:609673207620b1a65f233fd27993dcfe2fb028456b0096743976a3e6da773829"
estado: Plan conforme al alcance aprobado; construcción posterior por tarea3.
---
# Plan de features

## Resumen

Recencia, frecuencia, importe, diversidad y antigüedad observada. Viables para benchmark bajo supuesto de observación inmediata; disponibilidad operacional real no determinable. Este plan no construye features ni selecciona por desempeño.

## Contexto de features

Unidad cliente × cutoff mensual; priorizar100 clientes por ventas válidas siguientes90d. Historia180d; validación walk-forward de clientes conocidos. Target, cancelaciones futuras, ID, label_end y fecha absoluta no son features.

## Feature strategy

Raw: no copiar líneas al nivel cliente ni IDs. Numéricas: agregados monetarios/unidades, sin clipping aprendido. Categóricas: país/producto no se codifican, cambios y sparsity sin hipótesis adicional. Temporales/comportamiento/eventos: recencia, frecuencia y ventanas90/180. Relativas: no peers ni ratios adicionales, no cambiar set aprobado. Geoespaciales: país no sustituye coordenadas. Grafo: sin aristas fiables. Domain-specific: importe histórico positivo según códigos estándar, sin margen ni CLV. Sin EWMA/estacionalidad/trends extras: alcance acotado y cobertura limitada.

## Feature inventory

| Feature | Familia | Hipótesis | Inputs | Ventana | Viabilidad | Riesgo leakage | Prioridad | Coste |
|---|---|---|---|---|---|---|---|---|
| recency_days | temporal | Compra reciente indica actividad | invoice_at | 180d | Válida con condiciones | Fecha futura | P0 | Bajo |
| orders_90d | frecuencia | Recurrencia reciente | invoice_id, invoice_at | 90d | Válida con condiciones | Conteo global | P0 | Bajo |
| orders_180d | frecuencia | Persistencia en semestre | invoice_id, invoice_at | 180d | Válida con condiciones | Conteo global | P0 | Bajo |
| sales_90d | importe | Gasto reciente como referencia | quantity, unit_price, invoice_at | 90d | Válida con condiciones | Futuro/target | P0 | Bajo |
| sales_180d | importe | Actividad semestral | mismos | 180d | Válida con condiciones | Futuro/target | P0 | Bajo |
| units_180d | intensidad | Volumen de compras | quantity, invoice_at | 180d | Válida con condiciones | Futuro | P0 | Bajo |
| distinct_products_180d | diversidad | Amplitud de compra | stock_code, invoice_at | 180d | Válida con condiciones | Futuro | P0 | Bajo |
| tenure_observed_days | historial | Tiempo de relación observado | primera invoice_at pasada | Toda historia pasada | Válida con condiciones | Primera compra global futura | P0 | Bajo |

## Contrato temporal

Agregaciones90/180 en [t-ventana,t). Recencia desde última compra pasada. Tenure desde primera compra observada anterior a t, no antigüedad real y no limitada a180d. Outcome separado [t,t+90d). Una línea en t nunca feature; en t+90d nunca target. Al fit solo targets con label_end <= fit_at. Disponibilidad transaccional y delay0 supuestos explícitos.

## Priorización

P0: ocho señales del contrato; bajo coste y semántica auditable. P1/P2: ninguna feature adicional en este piloto. Correlación de ventanas no implica identidad; conservadas por horizontes distintos definidos en plan, sin selección guiada por target.

## Leakage notes

ID conserva asociación/desempate, no predictor. No primera compra/total por cliente calculados con futuro. Reconciliación de copias usa fuente completa: riesgo retrospectivo de disponibilidad de la representación, supuesto documentado; multiplicidad preservada. Preprocessing se ajusta por fit posteriormente. Excluir outcome de inputs explícitos.

## Plan de implementación

Columnas fuente → reglas de compras/reconciliación aprobadas → historial por cliente → agregaciones por ventana y facturas únicas → unión uno-a-uno cliente; target separado. Conservar motivos/provenance de exclusiones y copias entre hojas. No implementar nuevas transformaciones aprendidas en construcción.

## Esquema del dataset modelable

customer_id, cutoff, label_end, target_sales_90d y ocho features. Añadir history_min_at/history_max_at y target_min_at/target_max_at para auditoría, sin alimentar modelo. Key cliente × cutoff.

## Plan de verificación

Tests de límites y perturbación del futuro, frame inmutable, exclusiones, duplicados, horizonte completo, madurez y key única. Checks globales: finitud, cardinalidad, fechas feature<t, target dentro horizonte. Revisar correlaciones solo development/train antes del holdout. Auditoría detallada posterior por detect-leakage.

## Riesgos, descartes y preguntas abiertas

Información de ingestion/correcciones desconocida; todos inputs válidos con condiciones retrospectivas. Cohorte/tenure censurados izquierda, país no acredita B2C. No inferir mejora de modelo por plausibilidad. Siguiente paso: construir ocho P0 y comprobar límites antes de entrenar. Reglas fijadas en contrato, no requiere elegir nuevas features por resultados.
