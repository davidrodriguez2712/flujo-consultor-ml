```json
{
  "rows": [
    {
      "id": "D1",
      "eligibility": "indeterminate",
      "label_state": "observed_negative",
      "reason": "prediction_timestamp 2025-05-01 es anterior al cutoff 2025-07-01, y window_end 2025-06-30 también, así que la ventana figura cerrada antes del cutoff. El target=0 se observa en la extracción de 2025-07-15, que es posterior al cutoff. No se proporciona label_available_at, delay ni regla de certificación. Por eso no se puede probar que la etiqueta estuviera disponible en o antes de 2025-07-01. El fin de ventana y la observación en una extracción posterior no equivalen a disponibilidad al entrenar. Si la etiqueta se certificó después del cutoff, la fila sería exclude; si se certificó en o antes del cutoff, sería eligible. No se asume ninguna de las dos fechas. Las features están disponibles antes del prediction_timestamp, así que el único punto sin resolver es la disponibilidad de la etiqueta."
    }
  ],
  "open_questions": [
    "¿Cuál es el label_available_at de D1, es decir, cuándo se conoció o certificó el target=0 en el proceso de negocio?",
    "¿Existe un delay o regla de certificación entre window_end (2025-06-30) y la disponibilidad de la etiqueta? Si existe, ¿de cuántos días es?",
    "¿Cuenta como negativo observado un target=0 en la extracción de 2025-07-15, o requiere certificación explícita de cierre de ventana?",
    "¿La regla de elegibilidad en el cutoff usa label_available_at <= cutoff (se permite igualdad con 2025-07-01T00:00:00Z) o una desigualdad estricta?"
  ],
  "gate_decision": "NEEDS_REVIEW"
}
```
