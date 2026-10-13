```json
{
  "rows": [
    {
      "id": "C1",
      "eligibility": "exclude",
      "label_state": "pending",
      "reason": "prediction_timestamp 2025-06-01 < cutoff 2025-06-15, pero label_available_at 2025-07-08 > cutoff (2025-06-15). La ventana de junio [2025-06-01, 2025-07-01) sigue abierta en el cutoff y la label se certifica solo tras cerrar ventana + 7 días. El target es null (label certificada vacía). El reporte parcial de cancelación del 2025-06-10 no está certificado y no se certifican positivos antes de la disponibilidad, por lo que no se trata como positivo observado ni como negativo."
    },
    {
      "id": "C2",
      "eligibility": "exclude",
      "label_state": "pending",
      "reason": "prediction_timestamp 2025-06-01 < cutoff 2025-06-15, pero label_available_at 2025-07-08 > cutoff 2025-06-15. La ventana de junio no estaba cerrada en el cutoff y el target es null, que significa pendiente, no negativo. No cumple label_available_at <= cutoff."
    },
    {
      "id": "C3",
      "eligibility": "eligible",
      "label_state": "observed_negative",
      "reason": "prediction_timestamp 2025-05-01 < cutoff 2025-06-15; label_available_at 2025-06-08 <= cutoff 2025-06-15 (7 días antes del cutoff); target = 0 observado y certificado. Cumple la regla de ventana cerrada + 7 días para mayo (la ventana termina el 2025-06-01 y la disponibilidad es el 2025-06-08, coherente con esa regla)."
    }
  ],
  "open_questions": [
    "¿Existe una regla formal sobre el tratamiento de filas con label pendiente en el entrenamiento (exclusión, reetiquetado posterior en un reentrenamiento futuro)? Este análisis las excluye sin imputar outcome.",
    "¿El reporte parcial de cancelación de C1 (2025-06-10) puede usarse para algún fin operativo o de monitoreo? No se usa como label de entrenamiento porque no está certificado y el contrato no certifica positivos antes de la disponibilidad.",
    "¿La ventana de mayo es [2025-05-01, 2025-06-01)? No viene explícita en los inputs; se infiere por analogía con la regla de junio y es coherente con label_available_at 2025-06-08, pero conviene confirmarlo.",
    "¿Qué población de filas (más allá de C1-C3) compone el conjunto real de entrenamiento? Con solo una fila elegible no hay base para validación ni para evaluar prevalencia de positivos."
  ],
  "gate_decision": "NEEDS_REVIEW"
}
```
