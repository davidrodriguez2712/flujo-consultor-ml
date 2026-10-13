# Validación final — riesgo de crédito sintético

Fecha: 2026-10-08. Protocolo/código congelados antes del run final; configuración conservada de development. Resultado para revisión humana, no aprobación de uso real.

## Población y trazabilidad

Refit único al 2025-07-01: 2.140 solicitudes concedidas, 249 positivos, label disponible al cutoff; último scoring admisible 2025-03-25. Modelo/transformaciones fijos. Scoring julio–septiembre: 900 solicitudes, 447 concedidas con labels maduros, 60 positivos; 453 rechazadas sin outcome y cero pendientes dentro de este periodo.

Predicciones persistidas antes de leer labels del periodo de evaluación. La referencia final es 249/2.140=0.116355, fit sobre ese train, no la prevalencia vieja de development. El raw fue accesible y auditado previamente: no hubo evaluación ciega.

## Desempeño en concedidas maduras

| Métrica | Modelo | Referencia |
|---|---:|---:|
| Brier score | 0.102487 | 0.116530 |
| ROC-AUC | 0.752283 | 0.500000 |
| Media estimada | 0.126957 | 0.116355 |
| Tasa observada | 0.134228 | Misma población |

Mejora puntual de Brier: 0.014043. No prueba significancia, generalización real ni eficacia de skills. No se calcularon intervalos que supongan independencia entre solicitudes. Configuración no se cambió para favorecer estos resultados.

## Cortes mensuales — solo concedidas maduras

| Mes | N | Positivos | Brier modelo | Brier referencia | ROC-AUC | Precision@100 | Recall@100 | Lift@100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2025-07 | 152 | 19 | 0.093387 | 0.109450 | 0.762564 | 0.17 | 0.8947 | 1.3600 |
| 2025-08 | 131 | 22 | 0.138071 | 0.142396 | 0.707256 | 0.22 | 1.0000 | 1.3100 |
| 2025-09 | 164 | 19 | 0.082499 | 0.102432 | 0.780762 | 0.17 | 0.8947 | 1.4674 |

K=100 en cada población mensual; elegibles 152/131/164. Las tres métricas de selección corresponden a listas de concedidas maduras, no al ranking de todas las solicitudes.

## Clientes respecto del train

| Segmento | N | Positivos | Brier modelo | Brier referencia | ROC-AUC | Media score | Tasa observada |
|---|---:|---:|---:|---:|---:|---:|---:|
| known | 324 | 37 | 0.093217 | 0.101161 | 0.734344 | 0.117484 | 0.114198 |
| new | 123 | 23 | 0.126908 | 0.157015 | 0.774348 | 0.151913 | 0.186992 |

Known significa presente en train admisible; new no implica primera solicitud histórica. El Brier mejora puntualmente en ambos grupos. En nuevos, media score 0.151913 frente a tasa 0.186992; no declarar calibración suficiente ni aplicar una corrección aprendida del holdout.

## Calibración — bins prefijados

| Bin | N | Media score | Tasa observada |
|---|---:|---:|---:|
| 0.0–0.1 | 238 | 0.057517 | 0.058824 |
| 0.1–0.2 | 136 | 0.138584 | 0.125000 |
| 0.2–0.4 | 55 | 0.269492 | 0.345455 |
| 0.4–0.6 | 14 | 0.489800 | 0.571429 |
| 0.6–0.8 | 4 | 0.633602 | 0.500000 |
| 0.8–1.0 | 0 | — | — |

Bins [low,high), último incluye 1.0. Las filas y tasas sugieren desajustes en probabilidades intermedias; bins altos tienen muy pocas observaciones. Estas diferencias puntuales no prueban un problema poblacional específico. Conservar la evidencia y evitar certificar calibración a partir del promedio global.

## Top-100 sobre todas las solicitudes

| Mes | Elegibles | Seleccionados | Labels observados | Coverage | Precision / Recall / Lift |
|---|---:|---:|---:|---:|---|
| Julio | 300 | 100 | 26 | 26 % | No identificadas |
| Agosto | 300 | 100 | 22 | 22 % | No identificadas |
| Septiembre | 300 | 100 | 26 | 26 % | No identificadas |

Las listas están conservadas en results.json. Entre 74 % y 78 % de los seleccionados no tienen outcome observado porque fueron rechazados históricamente. No rellenar con negativo ni transferir el Precision@100 de concedidas a estas listas. Tampoco identificar los scores como PD calibradas para rechazadas.

El benchmark mensual dispone de todas las solicitudes al cerrar el mes; no representa una política online de revisión previa a concesión. El efecto de revisar y el ahorro no se identifican.

## Verificación y recomendación para revisión

Hashes, disponibilidad, filas, scores, referencia y métricas auditados; evidencia en `reports/final-validation/` y outputs en `analysis/outputs/baseline-final/`. Las pruebas de integración del runner usaron fixtures manuales antes del freeze, no resultados del holdout real para seleccionar parámetros.

Resultado técnico favorable en la población observada, con límites de calibración. Preparar un memo que recomiende conservar el prototipo como evidencia de laboratorio y obtener datos de originación/revisión/outcomes adecuados antes de una política real sobre todas las solicitudes. La decisión operacional global permanece parcialmente respondida. Revisión humana de Validation antes de Delivery.
