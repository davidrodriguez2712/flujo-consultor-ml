---
skill: understand-dataset
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

# Comprensión del dataset

## Resumen

Cinco tablas sintéticas. Una fila por solicitud en cada tabla: claves application_id únicas y mismas 7.200 solicitudes. La entidad customer_id puede repetirse; el grain es solicitud, no cliente ni cliente-mes. Se observan 1.766 clientes en enero 2024–diciembre 2025, con 300 solicitudes cada mes. Dos solicitudes del mismo cliente en un mes pueden ser legítimas; no deduplicar por cliente-mes.

Target contractual confirmado por Framing: 30 días de mora dentro de 90 días desde desembolso. Disponibilidad completa al día 97; relación con scoring: desembolso al día siguiente, por lo que se publica 98 días después del scoring. El contrato permite diseñar validación temporal condicionada a la población concedida.

## Hallazgos

### Crítico

- [Hecho] max_dpd_90d contiene el target: comparación `(max_dpd_90d >= 30)` coincide con todos los 3.084 outcomes observados. Esa información llega después del scoring. Es una trampa deliberada del fixture, no evidencia de que un modelo existente la haya usado.
- [Hecho] labels de rechazadas y pendientes vacíos. Rellenarlos con cero alteraría el target y la población. Evidencia: 3.726 rechazadas y 390 pendientes.

### Alto

- [Hecho] un join applications–history por customer_id produciría 35.914 filas frente a 7.200 por application_id. La relación correcta es 1:1 por solicitud; el join por cliente relaciona solicitudes diferentes.
- [Hecho] decisiones y funded_amount se generan al día siguiente del scoring. No son predictors disponibles al solicitar revisión.
- [Hecho] 455 labels observados al extract pertenecen a solicitudes anteriores al cutoff final pero no estaban disponibles el 2025-07-01. No incluirlos en el entrenamiento histórico.
- [Hecho del generator] la política de concesión depende de bureau_score y debt_to_income; hay selección de la población con labels. La magnitud de un sesgo de calibración hacia rechazadas es desconocida.

### Medio

- [Hecho] clientes recurrentes; no asumir independencia entre solicitudes. Compartir clientes entre periodos es permitido en el escenario propuesto, sin utilizar el ID como feature; reportar desempeño de nuevos/recurrentes.
- [Hecho del contrato] antecedentes ficticios disponibles dos días antes del scoring. No existe un ledger para reconstruirlos desde eventos; su validez temporal se comprueba contra el contrato del generator, no contra un sistema de crédito real.

### Informativo

- [Hecho] no hay claves application_id duplicadas ni filas exactas duplicadas; todas las tablas contienen las mismas solicitudes.
- [Hecho] extract_at es constante, por diseño. application_id tiene cardinalidad máxima y no es predictor. Las columnas de outcome/decisión tienen missing condicionado a estado, no errores aleatorios.
- [Hipótesis] la validación temporal mostrará desempeño distinto de un split aleatorio. No se midió ni se necesita probar entrenando en esta etapa.

## Evidencia

Inventario:

| Tabla | Filas | Columnas | Claves duplicadas | Filas exactas duplicadas |
|---|---:|---:|---:|---:|
| applications.csv | 7200 | 7 | 0 | 0 |
| decisions.csv | 7200 | 5 | 0 | 0 |
| history.csv | 7200 | 5 | 0 | 0 |
| outcomes.csv | 7200 | 7 | 0 | 0 |
| post_decision.csv | 7200 | 3 | 0 | 0 |

Tipos inferidos del CSV, no schema de origen; missing representa cadena vacía. El JSON incluye muestras sintéticas, cardinalidades y constantes por columna.

| Columna | Tipo inferido | Missing | Cardinalidad no vacía | Rango de fecha |
|---|---|---:|---:|---|
| applications.application_id | string | 0 | 7200 | — |
| applications.customer_id | string | 0 | 1766 | — |
| applications.scoring_at | date | 0 | 672 | 2024-01-01 a 2025-12-28 |
| applications.monthly_income | integer | 0 | 3732 | — |
| applications.debt_to_income | number | 0 | 4440 | — |
| applications.requested_amount | integer | 0 | 191 | — |
| applications.bureau_score | integer | 0 | 358 | — |
| decisions.application_id | string | 0 | 7200 | — |
| decisions.decision_at | date | 0 | 672 | 2024-01-02 a 2025-12-29 |
| decisions.decision | string | 0 | 2 | — |
| decisions.funded_amount | integer | 3726 | 191 | — |
| decisions.disbursed_at | date | 3726 | 672 | 2024-01-02 a 2025-12-29 |
| history.application_id | string | 0 | 7200 | — |
| history.customer_id | string | 0 | 1766 | — |
| history.snapshot_at | date | 0 | 672 | 2023-12-22 a 2025-12-18 |
| history.available_at | date | 0 | 672 | 2023-12-30 a 2025-12-26 |
| history.prior_late_count | integer | 0 | 6 | — |
| outcomes.application_id | string | 0 | 7200 | — |
| outcomes.extract_at | date | 0 | 1 | 2026-01-15 a 2026-01-15 |
| outcomes.disbursed_at | date | 3726 | 672 | 2024-01-02 a 2025-12-29 |
| outcomes.window_end | date | 3726 | 672 | 2024-04-01 a 2026-03-29 |
| outcomes.label_available_at | date | 3726 | 672 | 2024-04-08 a 2026-04-05 |
| outcomes.label_status | string | 0 | 3 | — |
| outcomes.target_30dpd_90d | integer | 4116 | 2 | — |
| post_decision.application_id | string | 0 | 7200 | — |
| post_decision.available_at | date | 4116 | 597 | 2024-04-08 a 2026-01-15 |
| post_decision.max_dpd_90d | integer | 4116 | 91 | — |

Fuente de todos los checks: `analysis/outputs/diagnosis-checks.json`. Reproducción: desde la raíz del checkout, ejecutar `python <ruta_a_una_copia_de_reports/diagnosis/audit-command.py.txt>`; el comando escribe el JSON de checks dentro del piloto. No modifica fuentes ni entrena modelos. El path del proyecto está explícito en el comando archivado.

## Preguntas abiertas

Aprobar rangos/cutoffs del diseño temporal y la distinción entre ranking retrospectivo mensual y una futura revisión al llegar la solicitud. Los outcomes de rechazadas y el efecto de revisar no existen en este fixture; son límites conocidos, no datos que deban inventarse.

## Recomendaciones

Mantener joins por application_id, IDs para trazabilidad, missing según estados y target separado de predictors. Revisar `reports/validation/validation-design-2026-10-08.md` y `reports/leakage/leakage-audit-2026-10-08.md` antes de aprobar Diagnosis. Este reporte no declara readiness de modelado ni recomienda algoritmos.
