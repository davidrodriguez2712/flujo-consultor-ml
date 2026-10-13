# Analytical report — piloto retail con datos públicos

## Contexto y fuente

Encargo y cliente simulados: priorización comercial periódica, sin cliente contratante ni campaña real [LIM002]. Fuente: Chen, D. (2012), [Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii), DOI 10.24432/C5CG6D, CC BY 4.0. Original preservado y provenance en `data/source_manifest.json`.

## Alcance y calidad

1.067.371 [OBS021] líneas originales → reconciliación de 22.523 [OBS023] copias entre hojas → 788.187 [OBS022] compras válidas y 256.661 [OBS024] exclusiones. Se conservan razones y source_sheet/source_row; máxima multiplicidad por patrón entre hojas, sin deduplicar internamente por mera igualdad.

Compras válidas: campos requeridos presentes, cantidad/precio finitos y positivos, factura sin prefijo c/C, ID identificable y código estándar conforme a regex del contrato. Código estándar es convención operacional, no certificación de mercancía. Descripción ausente no excluye por sí sola. Se excluyen 226.758 [OBS025] líneas por ID ausente y 4.709 [OBS026] por código no estándar; no imputar clientes artificiales ni declarar todos los códigos excluidos inválidos. Todas las geografías de la población aprobada, sin asumir B2C.

## Unidad, temporalidad y features

Cliente × cutoff mensual. Elegibilidad con historia 180 [ASM001] días; baseline ventas pasadas 90 [ASM003] días; target suma positiva válida durante 90 [ASM002] días siguientes. Ventanas semiabiertas; timestamps naive originales, zona no documentada. ID textual estable y desempate lexicográfico ascendente después de score descendente.

Features: recency_days, orders_90d, orders_180d, sales_90d, sales_180d, units_180d, distinct_products_180d y tenure_observed_days. Solo historia pasada; frecuencia por factura, tenure observado anterior al cutoff. ID, target, fechas absolutas y label_end fuera del modelo. Metadata temporal separada para auditoría. Supuesto de disponibilidad: [ASM005].

## Diseño y modelos

Walk-forward con snapshots train maduros (label_end ≤ fit_at), expanding window; entidades compartidas corresponden a repriorizar clientes conocidos. 4 [OBS010] períodos development, calendarios congelados en `validation/evaluation_contract.yaml`. Snapshots mensuales train pueden compartir horizontes: no independencia IID.

Dos modelos de configuración fija: Ridge sobre log1p(target), StandardScaler ajustado solo en train; HistGradient sobre log1p(target), sin early stopping ni búsqueda. Predicción expm1 con piso cero. Configuración exacta/seed en contrato y model_runs.json. Baseline principal ventas históricas; RFM comparador ordinal informativo, sin MAE monetario ni selección por final.

Aceptación: superar ventas Top-K agregadas baseline y no perder en mayoría de períodos; si ambos elegibles preferir simple salvo complejo mejor en todos. En final solo elegido contra baseline, mejora estricta; empate/pérdida mantiene baseline, sin cambiar a otro candidato por su outcome. Tests cubren estas reglas.

## Resultados

| Método development | Top-K agregado | Diferencia relativa | Períodos perdidos |
|---|---:|---:|---:|
| Baseline | GBP 2.606.803,55 [OBS014] | Referencia | Referencia |
| Ridge | GBP 2.217.514,29 [OBS015] | -14,93% [OBS017] | 4 [OBS019] |
| HistGradient | GBP 2.487.103,96 [OBS016] | -4,59% [OBS018] | 4 [OBS020] |

Ningún modelo elegible. Selección: historical_sales [OBS001], congelada antes de apertura final única [OBS034]. Final evalúa únicamente baseline [OBS033][LIM003].

| Métrica final | Valor |
|---|---:|
| Cutoff | 2011-09-01 [OBS011] |
| Fin exclusivo horizonte | 2011-11-30 [OBS012] |
| Clientes elegibles | 2.768 [OBS002] |
| Top-K efectivo | 100 [OBS003] |
| Ventas válidas futuras seleccionados | GBP 993.347,93 [OBS004] |
| Ventas válidas futuras todos los elegibles | GBP 2.408.052,35 [OBS005] |
| Fracción capturada | 41,25% [OBS006] |
| MAE por cliente | GBP 633,47 [OBS007] |
| Top-1 por outcome dentro seleccionados | 11,84% [OBS008] |
| Top-10 por outcome dentro seleccionados | 54,57% [OBS009] |

MAE mide error monetario del baseline, sin acreditar calibración prospectiva. La fracción capturada divide ventas seleccionadas por ventas de toda la población elegible del mismo horizonte; no por ventas de todo el retailer ni todo el histórico.

## Diagnósticos separados

Último ranking baseline frente al anterior: permanecen 60 [OBS030] miembros, Jaccard 0,429 [OBS031]. Es estabilidad de selección, no retención/churn del negocio. Conjunto final: 522 [OBS027] líneas de cancelación, 51 [OBS028] clientes e importe firmado GBP -47.363,08 [OBS029]; vínculo con compra original no determinado. Concentración ordena outcomes para diagnóstico y no cambia ranking/aceptación.

## Límites e interpretación

Una sola fuente histórica y un solo final; distribución global vista en Diagnosis. No ceguera completa a distribución ni superioridad universal del baseline. Disponibilidad real, latencia y revisiones históricas no determinables [ASM005]. Clientes conocidos identificables con historia; generalización a nuevos clientes no evaluada. Primera compra observada no es adquisición, cero outcome no churn definitivo.

El target no mide ventas netas, margen, CLV completo, uplift o ROI [LIM001]. Los importes seleccionados son ventas observadas, no incrementales causadas por una acción. Sin intervalos de confianza IID: pocos períodos y snapshots dependientes. Si se modifica estrategia tras ver final, se requiere nueva versión/evaluación, sin llamarlo holdout intacto.

## Artefactos y reproducción

Scores: `data/processed/development_predictions.csv`, `data/processed/holdout_predictions.csv`. Ranking: `delivery/prioritization_retrospective.csv`. Métricas/elección: `reports/validation/holdout-results.json`, `development-selection.json`. Checks/hash/timestamp: manifests y holdout-attempt.json. 50 [OBS032] tests pasan; no reentrenar ni repetir final para ajustar narrativa. Reproducción aislada y runbook se preparan en Handoff, todavía pendiente; no afirmar portabilidad analítica Windows por esta ejecución local.

Gasto API US$0 [OBS013]; tiempo humano/infraestructura no cuantificados. Skills experimental usadas como apoyo metodológico, sin evidencia de eficacia general ni promoción Foundry. Próximo paso comercial distinto: datos as-of actuales y diseño causal [PROP001].
