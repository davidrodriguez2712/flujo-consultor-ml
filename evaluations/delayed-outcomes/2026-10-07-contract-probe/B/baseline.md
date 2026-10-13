```json
{
  "rows": [
    {
      "id": "B1",
      "eligibility": "eligible",
      "label_state": "observed_negative",
      "reason": "Suponiendo que training_timestamp = cutoff (2025-07-01T00:00:00Z), label_available_at (2025-07-01T00:00:00Z) <= training_timestamp se cumple por igualdad exacta, y la regla contractual es no estricta (<=). prediction_timestamp 2025-01-01T00:00:00Z es anterior al cutoff y el target 0 está certificado como negativo observado. No hay embargo adicional autorizado, así que la igualdad no se penaliza."
    },
    {
      "id": "B2",
      "eligibility": "exclude",
      "label_state": "pending",
      "reason": "Suponiendo que training_timestamp = cutoff (2025-07-01T00:00:00Z), label_available_at (2025-07-01T00:00:01Z) excede el cutoff por 1 segundo, por lo que label_available_at <= training_timestamp no se cumple. En ese momento el target no estaba certificado: aunque la extracción del 2025-07-10 muestra target 0, usarlo introduciría información posterior al cutoff. Su estado respecto al cutoff es pending, no negativo observado."
    }
  ],
  "open_questions": [
    "¿Cuál es el training_timestamp real? Los inputs no lo definen. Se asumió que coincide con el cutoff (2025-07-01T00:00:00Z). Si fuera la fecha de extracción (2025-07-10), B2 pasaría a eligible/observed_negative.",
    "¿Se confirma que no se aplica tolerancia ni embargo adicional? El contexto dice 'sin embargo adicional autorizado'. Con la regla <= estricta, la diferencia de 1 segundo entre B1 y B2 decide la elegibilidad.",
    "¿Cuál es la longitud del horizonte de predicción y la fecha de cierre por fila? Solo se dispone de label_available_at; no se verificó que el horizonte se haya cerrado antes de esa fecha.",
    "¿Está sincronizada la precisión de timestamps (segundos, zona horaria UTC) entre el sistema que certifica el target y el que define el cutoff? Un desfase de 1 segundo podría cambiar la decisión de B2.",
    "¿Cómo se debe tratar B2 si el cutoff queda fijado como límite de entrenamiento: se descarta definitivamente o se reincorpora en un reentrenamiento posterior con un training_timestamp mayor?"
  ],
  "gate_decision": "NEEDS_REVIEW"
}
```
