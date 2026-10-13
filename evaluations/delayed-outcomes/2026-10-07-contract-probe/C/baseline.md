```json
{
  "rows": [
    {
      "id": "C1",
      "eligibility": "exclude",
      "label_state": "pending",
      "reason": "prediction_timestamp 2025-06-01; la ventana de junio [2025-06-01, 2025-07-01) seguía abierta en el cutoff/train 2025-06-15, y label_available_at 2025-07-08 es posterior a ese cutoff. El target es null y no hay label certificada. El partial_event_report del 2025-06-10 no está certificado: las reglas indican que no se certifican positivos antes de cerrar ventana + 7 días. No se usa como positivo ni se trata como negativo observado. La fila queda fuera de este entrenamiento y podría reevaluarse desde 2025-07-08."
    },
    {
      "id": "C2",
      "eligibility": "exclude",
      "label_state": "pending",
      "reason": "prediction_timestamp 2025-06-01; misma ventana de junio, abierta en el cutoff 2025-06-15. label_available_at 2025-07-08 es posterior al cutoff y target es null. La ausencia de label no equivale a negativo observado, porque la certificación aún no existía. Queda fuera de este entrenamiento y podría reevaluarse desde 2025-07-08."
    },
    {
      "id": "C3",
      "eligibility": "eligible",
      "label_state": "observed_negative",
      "reason": "prediction_timestamp 2025-05-01; label_available_at 2025-06-08 es anterior al cutoff 2025-06-15, es decir, la label estaba certificada antes de la extracción/train. target = 0 está observado. La disponibilidad 2025-06-08 es coherente con la regla (cierre de ventana mensual 2025-06-01 + 7 días), aunque la ventana de mayo no se da explícitamente en el contexto."
    }
  ],
  "open_questions": [
    "¿La ventana de mayo para C3 es [2025-05-01, 2025-06-01)? El contexto solo define explícitamente la de junio; aquí se infiere por la regla mensual y por label_available_at 2025-06-08.",
    "¿Cuál es el horizonte de predicción y la definición operativa del positivo (cancelación) y de su fecha de evento? El partial_event_report de C1 (2025-06-10) no incluye detalle del evento, y no se pudo verificar si cae dentro de la ventana.",
    "¿Se reevaluarán C1 y C2 en un reentrenamiento posterior a 2025-07-08, cuando exista label certificada?",
    "¿La label certificada vacía (target null) de C1 y C2 significa 'aún no certificada' o 'certificada sin evento'? Se asumió lo primero, porque la certificación no estaba disponible al cutoff.",
    "¿Con solo una fila elegible (C3, negativa) hay suficientes positivos y períodos para entrenar o validar? Con este input no hay positivos observados."
  ],
  "gate_decision": "NEEDS_REVIEW"
}
```
