---
skill: detect-leakage
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

# Auditoría de leakage previa al baseline — v2

## Resumen

Alcance: CSV sintéticos, generador, joins posibles y diseño de validación aprobado. No existe todavía un pipeline de entrenamiento que pueda certificarse. Se confirmó y corrigió una exportación fuera del corte en v1. Los checks ejecutados sobre v2 no encontraron infracciones. Esta conclusión no equivale a ausencia garantizada de leakage en un modelo futuro.

## Hallazgos

### Crítico — Confirmado y corregido

**Componente:** exportación de cancellation_at. **Mecanismo:** comparar solo fecha permitía incluir un evento a las 12:00 del mismo día cuyo corte era 00:00. **Evidencia:** una fila en v1, cero en v2; label pending inalterada. **Impacto:** fuente incumplía el corte de extracción; no se usó para entrenar. **Acción:** comparación estricta de fechas acorde al timestamp fijo; si las horas dejan de ser fijas, usar timestamps completos. Borrador y regresión conservados.

### Alto — Riesgo condicionado al uso

- **Target/post-event:** churn_next_month deriva del evento; cancellation_at y label_status incorporan outcomes posteriores. Su naturaleza está confirmada por datos/generador, pero no hay prueba de incorporación a un modelo. Mantenerlos fuera de X; usar metadata solo para y/disponibilidad.
- **Disponibilidad de labels:** elegir todas las observed de la extracción para cualquier fold incluiría outcomes no disponibles en esa fecha histórica. Filtrar siempre label_available_at <= training_timestamp. Los 9 folds comprobados cumplen la regla.
- **Join/aggregation:** tickets multiplican filas si se unen sin agregar. Conteos del agregado existente concuerdan exactamente con los eventos. Usar agregado por cliente/scoring y comprobar que la clave no cambia.

### Medio — No determinable aún

- **Preprocessing, feature selection, target encoding, resampling y CV:** no existe código de fit/tuning para inspeccionar. No declarar auditado un Pipeline inexistente. El protocolo exige aprender transformaciones solo en train; confirmar su implementación posteriormente.
- **Selección del modelo/test:** el protocolo fija test julio–diciembre con modelo congelado. No se calcularon sus métricas. Implementar controles de acceso lógico al test y congelar configuración antes de evaluarlo.

### Informativo — Dependencia válida

- Los mismos clientes aparecen entre train y meses futuros (1.878 compartidos en el primer fold), pero no hay claves cliente/mes compartidas. El escenario aprobado vuelve a puntuar clientes; este solape no es por sí solo contaminación. No utilizar customer_id como predictor.
- Eventos de tickets anteriores al corte de features y ventanas limitadas por alta; cero infracciones en v2.
- MRR ligado al plan y actividad histórica son señales disponibles. No se marcan como leakage por ser predictivas. No se computó AUC univariante ni se entrenó un modelo.

## Evidencia

`analysis/outputs/diagnosis-checks.json`: 26 checks, cero infracciones; incluye fechas, labels, joins, actividad, tenure, cancelaciones y solape por fold. `generator-v2-regression.json`: un único cancellation_at pendiente corregido; otros CSV idénticos. `proposed-split-checks.json`: calendario de desarrollo y entrenamiento final aprobado.

## Preguntas abiertas

Código de entrenamiento, transformaciones aprendidas, selección y evaluación final aún no implementados. Su auditoría será necesaria para afirmar que las métricas futuras son válidas. No hay datos reales para comprobar disponibilidad operacional fuera del laboratorio.

## Recomendaciones

Aceptar/revisar diagnóstico y contrato de datos; conservar las reglas de labels, exclusión de outcomes y joins del diseño aprobado. Implementar un baseline con allowlist de predictors, ajuste solo en train y trazabilidad de splits. Reauditar el código antes de abrir el test. No hay justificación para promover la skill ni crear una capacidad nueva a partir de esta aplicación manual.
