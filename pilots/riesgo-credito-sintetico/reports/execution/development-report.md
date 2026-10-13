# Resultado del baseline de development

Fecha: 2026-10-08. Datos sintéticos, código/configuración congelados antes del run principal. No evaluación final. Los tests de integración previos usaron copias temporales del mismo generator, sin usar métricas para tuning.

## Población y protocolo

Train: 1.248 solicitudes concedidas,134 positivos; scoring anterior al 2025-01-01 y label disponible<=ese cutoff. Validation: 298 solicitudes concedidas/maduras,40 positivos, scoring enero–febrero 2025 y labels disponibles al 2025-06-15. No se presentan resultados para rechazadas.

Regresión logística L2 de cinco features, mediana/escalas solo train,600 iteraciones,learning_rate 0.05,L2=0.01. Referencia constante134/1248 = 0.107372. Sin tuning, resampling,IDs,outcomes ni columnas posteriores como predictors.

## Métricas agregadas

| Métrica | Modelo | Referencia |
|---|---:|---:|
| Brier score | 0.104092 | 0.116932 |
| ROC-AUC | 0.708430 | 0.500000 |
| Media de probabilidad | 0.121702 | 0.107372 |
| Tasa observada | 0.134228 | misma población |

Mejora puntual de Brier: 0.012841. La comparación es sobre las mismas filas; no se calculó inferencia de significancia ni incertidumbre que asuma independencia entre solicitudes.

## Meses — concedidas maduras

| Mes | N | Positivos | Brier modelo | Brier referencia | ROC-AUC | Precision@100 |
|---|---:|---:|---:|---:|---:|---:|
| 2025-01 | 163 | 26 | 0.128077 | 0.136784 | 0.656654 | 0.200 |
| 2025-02 | 135 | 14 | 0.075132 | 0.092963 | 0.776269 | 0.120 |

El ranking mensual es retrospectivo, población concedida evaluable. No representa lista de todas las solicitudes ni revisión online previa al desembolso. Enero tiene 163 elegibles y febrero 135; K 100 en ambos. Recall/Lift y IDs seleccionados constan en results.json.

## Clientes respecto del train

| Segmento | N solicitudes | Positivos | Brier modelo | Brier referencia | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| known | 152 | 18 | 0.096776 | 0.104520 | 0.730514 |
| new | 146 | 22 | 0.111708 | 0.129855 | 0.692449 |

Cliente known: apareció en train admisible; new: no apareció allí. No significa que fuera su primera solicitud en toda la historia. No inferir generalización poblacional de este corte sintético. Hay dependencia entre solicitudes del mismo cliente.

## Calibración

Resultados completos de bins prefijados en results.json. Media estimada 0.121702 frente a tasa 0.134228; no basta esa cercanía para certificar calibración. Los bins[.4,.6) y[.6,.8) tienen 4 y 2 filas, y[.8,1] está vacío: evidencia muy limitada. Conservar tamaños junto a tasas; no modificar bins para favorecer resultados.

## Auditoría y límites

Brier y AUC recalculados independientemente por aritmética/pairs: `development-output-audit.json`. Tests y review técnica se conservaron en esta carpeta; freeze/live code e inputs verificados. No se alteraron fuentes ni contracts aprobados.

No demuestra eficacia de skills, calibración para rechazadas, impacto de revisar, aprobación crediticia real ni ahorro. Los resultados de julio–septiembre no se calcularon. Execution requiere revisión humana; no se avanza por una métrica favorable.

## Siguiente paso propuesto

Tras aprobar Execution, conservar esta configuración, refit final con labels disponibles al 2025-07-01 y evaluar una vez julio–septiembre según diseño aprobado. El wrapper de evaluación final aún debe implementarse, probarse y congelarse sin usar resultados finales para cambiar decisiones.
