# Validation — revisión humana pendiente

## Decisión resultante

Mantener baseline `historical_sales`: ninguno de los dos modelos fijos fue elegible en development. La selección se congeló antes del holdout, con hashes y timestamp. Se evaluó únicamente baseline final; no se seleccionó otro modelo con sus outcomes.

## Resultado final histórico

Cutoff **2011-09-01**, horizonte [2011-09-01,2011-11-30). Población elegible: **2.768 clientes**. Capacidad simulada100, Top-K efectivo100.

| Métrica baseline | Valor |
|---|---:|
| Ventas válidas futuras en Top-100 | GBP 993.347,93 |
| Ventas válidas futuras de todos los elegibles | GBP 2.408.052,35 |
| Fracción de ventas elegibles en Top-100 | 41,25% |
| MAE del score monetario | GBP 633,47 por cliente |
| Concentración Top-1 dentro del Top-100, según ventas futuras | 11,84% |
| Concentración Top-10 dentro del Top-100, según ventas futuras | 54,57% |

Concentración se calcula sobre el outcome para diagnóstico; no se usa para cambiar el ranking. Estos importes son ventas observadas en el subconjunto de compras definido, no ventas incrementales inducidas, margen, CLV completo o ROI.

## Development y aceptación

Baseline Top-100 agregado4 períodos: GBP2.606.803,55. RidgeGBP2.217.514,29 (-14,93%); HistGradientGBP2.487.103,96 (-4,59%). Ambos pierden4/4; no cumplen aceptación. No tuning ni cambio de features tras observar resultados. Baseline final no demuestra ganancia comparativa: modelos descartados no se evaluaron en holdout.

## Estabilidad y cancelaciones

Última transición baseline (2011-06-01→2011-09-01): **60** clientes siguen en Top-100, permanencia de miembros del ranking **60%**, Jaccard **0.429**. Comparación retrospectiva de conjuntos, no churn causal ni promesa de estabilidad operacional.

En Top-100 final: 522 líneas de cancelación en el horizonte, correspondientes a51 clientes, importe firmadoGBP -47.363,08. No enlazadas a compra original; no restar para inventar ventas netas ni usar para reseleccionar.

## Verificación

50 tests pasan. Tests explícitos de K, empates lexicográficos, keys, outcomes completos, cero ventas, aceptación y prohibición de seleccionar otro modelo por holdout. Runner rechaza segunda apertura y cambios en selección. `holdout-attempt.json` registra una única ejecución COMPLETED; hashes de resultado/predicciones y congelación previa verificables. Checks estructurales del OS no sustituyen esta revisión metodológica.

Una comprobación posterior recalcula métricas desde los mismos scores/outcomes para verificar artefactos; no reentrena, no genera nueva selección y no vuelve a ejecutar el comando holdout.

## Límites

- Una fuente retail antigua, encargo/capacidad simulados y un único final histórico.
- Distribución global conocida en Diagnosis; holdout reservado a desempeño, no ceguera completa a distribución.
- Disponibilidad inmediata/as-of de revisiones supuesta; ingestion real no determinable.
- Snapshots train con clientes/horizontes compartidos; cuatro development no acreditan superioridad estadística universal. Sin intervalos de confianza IID.
- Clientes identificables activos180d, todos los países y códigos estándar; anónimos/nuevos/códigos no estándar fuera del ranking y cobertura explícita.
- Cero outcome no es churn; primera compra observada no es adquisición real. Cancelaciones no restadas retroactivamente.
- Ranking de clientes de mayor venta esperada no identifica quién se beneficia del contacto. Para decidir campaña efectiva se requiere prueba causal distinta.

## Gates solicitados

Validation, data_analysis-review, supervised_model-review, selection-review y executive_delivery-review pendientes de David. Último gate también seleccionado por el catálogo aunque el plan enumeró solo los primeros cuatro: revisar storyline coherente antes de Delivery. No preparar aprobación automática ni declarar proyecto completo.

Gasto API US$0. Siguiente etapa tras aprobación: recomendación/memo/reporte y claims trazables, luego reproducción y handoff.
