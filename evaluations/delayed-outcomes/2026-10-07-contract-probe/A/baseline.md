```json
{
  "rows": [
    {
      "id": "A1",
      "eligibility": "eligible",
      "label_state": "observed_negative",
      "reason": "label_available_at 2025-06-08T00:00:00Z <= cutoff 2025-07-01T00:00:00Z, así que el label ya era conocido al corte. prediction_timestamp 2025-05-01 es anterior al corte. target=0. Es coherente con la regla del contexto: fin del mes de scoring (mayo) + 7 días del mes siguiente = 2025-06-08."
    },
    {
      "id": "A2",
      "eligibility": "exclude",
      "label_state": "pending",
      "reason": "label_available_at 2025-07-08T00:00:00Z > cutoff 2025-07-01T00:00:00Z, así que el label no estaba disponible al corte de train. Aunque la fila trae target=0 (extraído el 2025-08-15), ese valor no era observable el 2025-07-01. Usarlo sería leakage temporal. El mes de scoring (junio) termina el 2025-06-30, y la ventana de outcome apenas había cerrado al corte. Es coherente con la regla: 2025-07-01 + 7 días = 2025-07-08."
    },
    {
      "id": "A3",
      "eligibility": "eligible",
      "label_state": "observed_positive",
      "reason": "label_available_at 2025-05-08T00:00:00Z <= cutoff 2025-07-01T00:00:00Z, así que el label ya era conocido al corte. prediction_timestamp 2025-04-01 es anterior al corte. target=1 (cancelación observada). Es coherente con la regla: fin de abril + 7 días = 2025-05-08."
    }
  ],
  "open_questions": [
    "¿El target=0 de A2 se materializó después del corte (hasta 2025-08-15) o es un valor provisional? Solo se confirma que no estaba disponible al corte; no se infiere su estado previo.",
    "¿Se confirma que label_available_at es el momento real de disponibilidad del label y no un valor teórico calculado con la regla de +7 días? Aquí coincide con la regla en las tres filas.",
    "¿Se confirma que el timestamp de corte (2025-07-01T00:00:00Z) y los label_available_at usan la misma zona horaria, UTC? La igualdad <= está permitida, pero ninguna fila cae exactamente en el borde.",
    "Con solo 2 filas elegibles (1 positiva, 1 negativa), ¿hay más filas fuera de este input? No se puede evaluar volumen ni prevalencia de positivos para entrenamiento con esta muestra.",
    "No se informa la entidad (suscriptor) de cada fila, ni si puede repetirse entre períodos. Se asume sin duplicados, según lo indicado."
  ],
  "gate_decision": "NEEDS_REVIEW"
}
```
