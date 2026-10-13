# Datos sintéticos — diccionario y reglas

Seed: 20261007. Versión corregida del generador: v1. Extracción simulada: 2026-01-15 00:00 UTC. Sin personas, cuentas ni empresa reales. USD representa importes ficticios, no márgenes ni recupero real.

## customers.csv

Una fila por cliente ficticio, clave `customer_id`. `signup_date`: fecha de alta a las 00:00 UTC; `plan`: basic/standard/premium, fijo en esta simulación; `channel`: canal de alta; `market`: constante synthetic; `is_synthetic`: constante 1. No existe una historia de cambios de plan.

## monthly_snapshots.csv

Una fila por cliente activo × comienzo de mes calendario, clave `(customer_id, prediction_timestamp)`. El cliente deja de generar snapshots tras cancelar. El universo disminuye y no hay altas nuevas después de 2024-06; esta limitación afecta la generalización.

- `prediction_timestamp`: instante de scoring, primer día a las 00:00 UTC.
- `features_available_at`: corte simulado del agregado, a las 23:00 UTC del día anterior; anterior al scoring.
- `tenure_months`: diferencia entre meses calendario del alta y el scoring; no meses completos transcurridos.
- `active_days_prev_month`: días de actividad en el mes anterior, limitados por alta y longitud del mes. Vacío representa missing simulado (~2%); no significa actividad cero.
- `active_days_prev2_month`: actividad agregada del mes previo al anterior. Cero si el cliente no existía en esa ventana. Para historias anteriores al primer snapshot el generador simula el agregado; no hay un log de actividad para reconstruirlo.
- `failed_payments_prev_month`, `support_tickets_prev_month`: conteos en el mes anterior, disponibles antes del scoring.
- `mrr_usd`: precio mensual del plan, 29/59/99 USD ficticios; no mide margen incremental ni efecto de una campaña.
- `discount_active`: indicador ficticio conocido al scoring. No es una asignación aleatoria de retención ni permite evaluar uplift.
- `is_synthetic`: constante 1; excluir de predictors.

## churn_labels.csv

Una fila por el mismo cliente y scoring; join 1:1 con snapshots por ambas columnas.

- `window_end_exclusive`: comienzo del mes siguiente; el horizonte es un mes calendario, NO 30 días fijos.
- `churn_next_month`: 1 si hay cancelación en `[prediction_timestamp, window_end_exclusive)`, 0 si no; vacío si no ha madurado la label.
- `label_available_at`: `window_end_exclusive + 7 días`, por el delay simulado de cierre. Una label se usa en entrenamiento solo si ya estaba disponible en la fecha de entrenamiento.
- `label_status`: observed o pending según disponibilidad al corte de extracción. Pending nunca equivale a 0.
- `cancellation_at`: dato del outcome; posterior al scoring. Se conserva para trazabilidad, pero no puede ser predictor. Puede constar una cancelación antes de que la ventana completa haya madurado; aun así no se adelanta la label.
- `extracted_at`: corte de extracción constante; no es la fecha del scoring.
- `is_synthetic`: constante 1.

No usar churn_next_month, cancellation_at ni label_status como features. Los otros campos de labels son metadata de ventanas/disponibilidad, no predictors de clientes.

## support_tickets.csv

Una fila por ticket, clave `ticket_id`. customer_id relaciona el cliente; `snapshot_prediction_timestamp` identifica a qué agregado del mes anterior contribuye. `opened_at` está después del alta y antes del scoring; `category` indica billing/technical/account. Un join directo multiplica snapshots cuando hay varios tickets: agregar primero por cliente y scoring o usar el conteo ya disponible. No sumar simultáneamente ambas fuentes del mismo conteo.

## Calidad y reproducibilidad

Consultar `analysis/outputs/data-checks.json` para conteos, missing, claves, fan-out y tiempos. Los CSV y sus SHA-256 están en `data/raw/manifest.json`. Regenerar en una carpeta nueva:

```bash
python analysis/generate_synthetic_data.py --output /ruta/a/carpeta-vacia
```

El script usa únicamente la biblioteca estándar de Python; no necesita Foundry ni ACOS. No sobrescribe destinos con contenido. La primera versión defectuosa se conserva en `data/interim/generator-draft-v0/` para trazabilidad; está excluida del piloto.
