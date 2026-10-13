---
skill: detect-leakage
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

# Auditoría de leakage previa al baseline

## Resumen

Confirmada la presencia de información posterior y target explícito en fuentes del fixture. No hay modelo ni pipeline entrenado: estos hallazgos describen columnas incompatibles con scoring y controles requeridos, no un uso indebido ya observado. Diseño temporal viable en concedidas con disponibilidad individual; implementación futura pendiente de auditar.

## Hallazgos

### Crítico

**L01 — Target/post-event leakage en post_decision.max_dpd_90d.** Confianza: Confirmado. El campo está disponible después del scoring y `(valor >=30)` reproduce el target en 3.084 observaciones completas. Entraría directamente el outcome si se incorporase como feature. Evidencia: checks leakage_feature_available_late y leakage_feature_encodes_target. Acción: mantenerlo fuera de la tabla predictora al scoring; conservarlo solo para auditar el fixture. No se prueba entrenando con leakage.

**L02 — Target en outcomes.** Confianza: Confirmado como campo posterior, no como uso en un pipeline. Target, ventanas y disponibilidad futura no son predictors; sirven como label/metadatos para filtros. La label completa llega 98 días tras scoring. Acción: separar inputs/labels y aplicar cutoff.

### Alto

**L03 — Decisión y desembolso posteriores.** Confianza: Confirmado. decision_at = scoring+1 día. decision, funded_amount y disbursed_at no existían al scoring. Acción: usar la decisión histórica únicamente para definir población evaluable, no como feature de solicitudes nuevas.

**L04 — Disponibilidad temporal del target.** Confianza: Riesgo para el fit futuro, confirmado que 455 labels pertenecen a solicitudes anteriores a 2025-07-01 pero se publicaron después. Un filtro solo por scoring_at permitiría leakage de labels. Acción: exigir label_available_at <= training_cutoff, sin considerar observed al extract como evidencia histórica.

**L05 — Join por customer_id.** Confianza: Confirmado fan-out hipotético; no ejecutado en el pipeline. Vincularía solicitudes diferentes del mismo cliente, incluyendo historia potencialmente futura: 35.914 filas en lugar de 7.200. Acción: join 1:1 por application_id y comparar fechas disponibles. No eliminar antecedentes legítimos.

### Medio

**L06 — Preprocessing, tuning, target encoding, resampling y selección de features.** Confianza: Riesgo; no hay código de esas operaciones todavía. No se declara un fallo confirmado. Acción: fit solo en train, sin resampling/global encoding en el scope propuesto; auditar la implementación antes del holdout.

**L07 — Clientes compartidos.** Confianza: Confirmado overlap de 289 clientes en rangos propuestos; NO confirmado leakage. El uso permite recurrentes y no utiliza IDs. Peligro si se incorporara una agregación que incluye eventos futuros o se presentara el resultado como generalización exclusiva a clientes nuevos. Acción: controles de ventana y reporting separado; no exigir GroupKFold automáticamente.

### Bajo

No hay hallazgos adicionales de severidad baja con evidencia que cambie la decisión.

### Informativo

Alta capacidad predictiva de una variable no demuestra leakage. Bureau, ingreso, deuda e historia están documentados como disponibles al scoring; no se marcaron por su correlación con el target. La regla probabilística latente del generator no se exporta como predictor. Selección histórica de concedidas limita generalización, pero no equivale por sí sola a leakage.

## Evidencia

`analysis/outputs/diagnosis-checks.json`: 10 checks temporales/labels true, cinco tablas con claves únicas, mismo universo de solicitudes y hashes coincidentes; relación determinista de la columna posterior con target; cardinalidad y overlap de rangos propuestos. Reporte de validación define reglas; no se ejecutó split productivo ni pipeline.

## Preguntas abiertas

Orden de fit/transform, código de asignación de particiones y uso real de features: pendientes de implementación. No determinable si ese pipeline futuro cumple los controles hasta inspeccionarlo. Acción real online y efecto de revisión: tampoco identificados por el benchmark mensual.

## Recomendaciones

Aprobar diseño; después revisar código y schema de features, labels disponibles al cutoff, fit de transformaciones y equivalencia de filas evaluadas frente a referencia. Mantener fuentes intactas y repetir auditoría si cambian joins/features. No se eliminaron columnas del raw ni se entrenó o recomendó un algoritmo.
