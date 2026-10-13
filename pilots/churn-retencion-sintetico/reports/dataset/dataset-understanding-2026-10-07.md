---
skill: understand-dataset
version: 0.1.0
fecha: '2026-10-07'
proyecto: churn-retencion-sintetico
modo: aplicación de pautas por asistente; no evaluación comparativa ni review independiente
inputs:
- path: data/raw/churn_labels.csv
  sha256: ed1898cfdabddee88711ff50efff0c99129b0fda253ab62b69f596c3a356820a
- path: data/raw/customers.csv
  sha256: 53fbf9495621829ddb1accb36cd6335d8a35f0a28f869f0ad5e373ed8d53afc3
- path: data/raw/monthly_snapshots.csv
  sha256: 64cf0c93c4c02fdc5a42d4ed578c32135fa22efef2349cc6d362da7c46f0a8e9
- path: data/raw/support_tickets.csv
  sha256: c425d1997f9a5b0a72e122da4fb84c879afcf4472c27ff25f3d6eda5e6eaee50
- path: analysis/generate_synthetic_data.py
  sha256: f195409ee5a05960e28466b71dcddc7405bc73860651fc8c5fab3b46de290dfc
- path: validation/validation_design.md
  sha256: 5addda286a3a07f392a5fc54c0353194abb74b3d0546b83d494758feacf9f0b2
estado: checks deterministas sin infracciones; revisión humana pendiente
---

# Comprensión del dataset — v2

## Resumen

Datos sintéticos: 2.400 clientes, 35.990 snapshots cliente/mes, 35.990 labels y 11.804 tickets. 24 períodos de scoring (febrero de 2024–enero de 2026). El target aprobado es cancelación en [inicio del mes de scoring, inicio del mes siguiente), con delay de label de 7 días después del cierre. Se pueden diseñar particiones temporales para la tarea del laboratorio.

## Hallazgos

### Crítico

- [Hecho, corregido] V1 exportó una cancelación de 2026-01-15 12:00 UTC con extracción a las 00:00. Comparaba fechas sin hora. V2 no exporta ese evento; la label permanece pendiente. No se entrenó sobre esa fuente. Evidencia: generator-v2-regression.json y diagnosis-checks-v1.json.

### Alto

- [Hecho] 972 labels de enero de 2026 no han madurado en la extracción; no convertirlas en negativos ni evaluar ese mes.
- [Hecho] Tickets tienen relación 1:N con snapshots. Un join directo multiplica filas (36.853 en vez de 35.990); agregar antes de unir o utilizar el conteo existente sin doble suma.
- [Hecho] Outcomes/metadata de labels son posteriores al scoring; un join para obtener y no debe incorporarlos como predictors.

### Medio

- [Hecho] 730 valores missing de actividad; no representan cero. Imputación y cualquier transformación ajustada deben aprenderse solo con train.
- [Hecho] Cohorte sin nuevas altas después de junio de 2024 y universo decreciente. La validación no demuestra performance de nuevos clientes ni de una empresa real.
- [Hecho] Historia inicial de actividad simulada por el generador, sin logs de actividad para reconstruir el agregado. Revisar código da trazabilidad en este laboratorio, no una garantía para futuros datos reales.

### Informativo

- [Hecho] Clave customers: customer_id; snapshots/labels: customer_id+prediction_timestamp; tickets: ticket_id. Sin duplicados exactos/lógicos ni huérfanos en checks.
- [Hecho] 35.018 labels observadas, 1.428 positivos (4,08%). Es una tasa sintética, no un KPI comercial estimado.
- [Hecho] market/is_synthetic/extracted_at son constantes; IDs no son predictors. mrr_usd deriva del plan en la simulación, pero alta correlación no lo convierte en leakage.

## Evidencia

26 comprobaciones de claves, eventos, ventanas, alta, disponibilidad y consistencia de conteos sin infracciones en `analysis/outputs/diagnosis-checks.json`. Cada input tiene SHA-256 en este frontmatter. El generador v2 se reprodujo con CSV idénticos byte a byte. No se entrenaron modelos ni se ejecutó EDA extensivo.

## Preguntas abiertas

- Aceptación humana de este diagnóstico y contrato de datos.
- Semántica, fuentes y disponibilidad de un cliente real, si se sustituye el dataset sintético.
- El código de entrenamiento todavía no existe: su ajuste y validación deben auditarse cuando se implemente.

## Recomendaciones

Usar solo data/raw v2; mantener borradores excluidos. Aplicar el contrato y protocolo aprobado a un baseline reproducible después de revisar diagnosis/data-quality. Registrar una auditoría posterior del código de entrenamiento antes de usar métricas finales.
