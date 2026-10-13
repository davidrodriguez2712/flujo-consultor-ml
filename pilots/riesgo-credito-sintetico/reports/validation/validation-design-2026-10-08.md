---
skill: design-validation
version: 0.1.0
fecha: '2026-10-08'
proyecto: riesgo-credito-sintetico
inputs:
- path: data/raw/applications.csv
  sha256: 512ed2cc0797ffec199cfa9bd3aad48ea1a5954a1be81bad60ff645b28f052f6
- path: data/raw/decisions.csv
  sha256: 1bac356ab25a8c3a6bcb9a76c8c6230ff9cf48e7085be0be2148d3ae0066ff29
- path: data/raw/history.csv
  sha256: 2a2da6b8dea82df9a4f2b8e066a0439219935f337e2af45970529a6359970ca5
- path: data/raw/outcomes.csv
  sha256: 3cdfdd1ce17e854a40d83dced1f331eee56aca95e7750ec782d2edc747d586f7
- path: data/raw/post_decision.csv
  sha256: 21662662dda0bdcf67f5a0c28060db8acb245d2070dce07913d929038e3812a5
- path: data/dictionaries/README.md
  sha256: 00cd77fffb84fd4337f9c669724097f3d2f427d8a3c9ba59d2ff60e4a82e5dc2
- path: framing/framing.yaml
  sha256: b4c3ca36f64eb3d823dc62a69240680be677d4d6fefeb0075a469085270b2fe4
- path: framing/metrics.yaml
  sha256: 9cc6288130578b8282efc7d59381c8fc33b9004b84967401034ee4772d083d4f
- path: analysis/generate_synthetic_data.py
  sha256: 63db985307b2c1a9e110599927154471a8a1ff1642438047134bd1a35695442c
estado: Diagnóstico propuesto para revisión; sin entrenamiento ni aprobación de readiness.
---

# Diseño de validación temporal

## Resumen

Recomendación: entrenar con labels disponibles en un cutoff histórico, evaluar solicitudes posteriores y reservar julio–septiembre de 2025 para evaluación final con modelo fijo desde 2025-07-01. Simula predicción sobre solicitudes futuras de clientes nuevos/recurrentes, condicionando la evaluación a créditos concedidos. No demuestra eficacia de una política de revisión de todos los solicitantes.

Las fechas/cadencia son una propuesta de laboratorio; revisión humana pendiente. La skill no ejecuta splits ni entrena modelos: el preflight comprobó viabilidad de las reglas sin persistir asignaciones ni métricas.

## Objetivo de validación

Medir calidad de probabilidades y ranking de riesgo usando información disponible al scoring. Separar desempeño offline en concedidas maduras de scores propuestos para solicitantes sin outcome. El escenario incluye solicitudes repetidas y permite puntuar clientes recurrentes.

## Estructura de datos relevante

Una fila por solicitud, customer_id recurrente, scoring diario y summaries mensuales. Target: 30DPD dentro de 90 días desde desembolso. La label completa está disponible 97 días tras desembolso, 98 días tras scoring en este fixture. Extract 2026-01-15. No derivar disponibilidad a partir del estado observed al extract.

## Estrategia recomendada y definición de splits

| Propósito | Regla propuesta | Preflight |
|---|---|---|
| Model development: train | scoring anterior a 2025-01-01, label disponible <= ese cutoff | 1.248 filas, 134 positivos |
| Model development: validation | scoring enero–febrero de 2025, label disponible al seleccionar el 2025-06-15 | 298 concedidas maduras, 40 positivos |
| Final fit | scoring anterior a 2025-07-01, label disponible <= ese cutoff | 2.140 filas, 249 positivos |
| Final / out-of-time | scoring julio–septiembre de 2025, modelo fijo al 2025-07-01, evaluación al 2026-01-15 | 900 solicitudes; 447 concedidas evaluables, 453 rechazadas |
| Operational benchmark | ranking por mes, hasta 100, empate por application_id | Métricas solo para población explícita con labels completos; coverage para todas |

Regla de train adicional: solo concedidas con target observado; la disponibilidad al cutoff manda. No aprovechar los 455 outcomes anteriores al cutoff que solo se hicieron observables después. La última solicitud admisible para final fit es 2025-03-25, pero no se impone esa fecha manualmente: resulta del filtro de disponibilidad individual.

Los positivos/prevalencia del periodo final no se agregaron en este preflight ni se calcularon métricas predictivas. Los checks globales de calidad sí leyeron outcomes para validar estados, fechas y relación de la columna deliberadamente posterior con el target. No afirmar que los labels finales son inaccesibles o que hubo evaluación ciega: el autor tiene acceso al raw y al generator.

## Diseño de cross-validation

Un holdout temporal de development es suficiente para este baseline acotado; no se propone tuning masivo ni múltiples folds/nested CV por defecto. La configuración/modelo candidato se fijará en un contrato de ejecución antes de evaluar final. Si se necesitase tuning extensivo, diseñar folds temporales dentro de development y revisar el protocolo antes de correrlos.

No hay embargo fijo añadido: se usa disponibilidad real por fila. No hay features con rolling windows compartidas en el scope actual. Un cambio que introduzca agregaciones futuras o dependencia de eventos requiere auditar ventanas y revisar si necesita purging.

## Manejo de entidades

Compartir clientes entre train y test representa solicitudes futuras de clientes recurrentes; no es automáticamente leakage. Preflight: 289 clientes aparecen tanto en train final como en concedidas maduras finales. Se prohíbe customer_id como predictor. Clasificar filas futuras como cliente conocido/desconocido respecto del train para reportar ambos, sin asumir independencia de solicitudes.

## Salvaguardas de leakage

Orden posterior: aprobar diseño; congelar protocolo/código; materializar particiones por las reglas; ajustar imputación, escalas y predictor constante únicamente con train; predecir validation; fijar configuración y refit final; evaluar el periodo final una vez. No modificar reglas/features para favorecer el holdout.

Join applications–history por application_id con validación 1:1 y history.available_at <= scoring. Features admisibles: income, debt_to_income, requested_amount, bureau_score y prior_late_count. Outcome, decisiones históricas, IDs y columnas posteriores quedan fuera de predictors. Auditoría en el reporte de leakage; no existe aún código de entrenamiento que certificar.

## Métricas

Brier score agregado por solicitud, con referencia constante fit en train, sobre idénticas filas. ROC-AUC cuando haya ambas clases; calibración en bins prefijados `[0,.1,.2,.4,.6,.8,1]`, incluyendo 1 en el último bin. Conteos/tasas por mes y por clientes conocidos/desconocidos, evitando concluir a partir de segmentos pequeños.

Precision@K/Recall@K/Lift@K mensuales en concedidas maduras con K efectivo propio; no confundir esa lista con Top-K de todas las solicitudes. En lista de todas las solicitudes, reportar cobertura de labels: si hay ausencias, las métricas globales no están identificadas. Sin positivos/K=0 se aplican estados de indefinición aprobados en Framing.

El benchmark Top-K usa todas las solicitudes del mes una vez llegadas. No es una simulación de revisión online previa a concesión: para eso habría que definir ventanas de llegada, presupuesto restante y decisiones antes del desembolso. No se cuantifica impacto causal. Mejor Brier es mejora puntual del fixture, no gate automático de negocio.

## Riesgos, alternativas descartadas y preguntas abiertas

- Random/stratified holdout descartado como primario: mezcla solicitudes pasadas/futuras y no representa entrenar con labels disponibles en un momento histórico.
- Group holdout como único esquema descartado: mediría solo clientes nuevos; el scope incluye recurrentes. Reportar nuevos por separado.
- Temporal split sin cutoff de label descartado: usaría outcomes que no existían al fit.
- Walk-forward mensual/nested CV descartados en este baseline: agregan decisiones y ejecuciones que no exige el alcance. El modelo fijo requiere declarar su cadencia; no simula reentrenar mensualmente.
- Reject inference, impacto causal y desempeño de revisiones reales: no determinables con estos datos.
- Pregunta de gate: aprobar rangos, disponibilidad, features, bins y cadencia propuestos. La etapa de ejecución debe congelar también algoritmo/configuración antes de métricas finales.

Contrato canónico del diseño propuesto: `validation/validation_design.yaml`. No hay feature engineering ni entrenamiento realizados por esta skill.
