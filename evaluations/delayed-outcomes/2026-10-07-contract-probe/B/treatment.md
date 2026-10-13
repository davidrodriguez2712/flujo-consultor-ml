```json
{
  "rows": [
    {
      "id": "B1",
      "eligibility": "eligible",
      "label_state": "observed_negative",
      "reason": "prediction_timestamp 2025-01-01T00:00:00Z es anterior al cutoff 2025-07-01T00:00:00Z. label_available_at 2025-07-01T00:00:00Z es igual al cutoff, y la regla contractual del caso es label_available_at <= training_timestamp, por lo que la igualdad está permitida. target=0 es un negativo observado según el contexto (negativos observados, target certificado tras cerrar el horizonte). No se añade embargo, ya que no hay fundamento autorizado."
    },
    {
      "id": "B2",
      "eligibility": "exclude",
      "label_state": "pending",
      "reason": "prediction_timestamp 2025-01-01T00:00:00Z es anterior al cutoff, pero label_available_at 2025-07-01T00:00:01Z es 1 segundo posterior al cutoff 2025-07-01T00:00:00Z, por lo que incumple label_available_at <= training_timestamp. Al cutoff la etiqueta aún no estaba disponible; que target=0 figure en la extracción del 2025-07-10 no prueba disponibilidad al entrenar. Se trata como pendiente al cutoff, no como negativo utilizable. No se inventa ninguna fecha ni se aplica tolerancia."
    }
  ],
  "open_questions": [
    "¿El training_timestamp coincide exactamente con el cutoff 2025-07-01T00:00:00Z? La decisión de B1 y B2 depende de esa equivalencia, que se asume a partir del contexto pero no se declara de forma explícita.",
    "¿La precisión de label_available_at es de segundos y está en UTC homogéneo? La exclusión de B2 depende de una diferencia de 1 segundo y no se ha verificado la fuente del timestamp.",
    "¿Se confirma que no hay tolerancia ni embargo autorizados? El contexto indica 'sin embargo adicional autorizado' y así se ha aplicado.",
    "Faltan end-of-window y la duración del horizonte por fila; no se ha podido verificar el cierre de ventana más allá de lo que declara label_available_at y el contexto."
  ],
  "gate_decision": "NEEDS_REVIEW"
}
```
