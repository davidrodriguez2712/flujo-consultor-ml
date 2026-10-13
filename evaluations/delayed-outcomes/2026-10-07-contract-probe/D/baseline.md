```json
{
  "rows": [
    {
      "id": "D1",
      "eligibility": "indeterminate",
      "label_state": "unknown",
      "reason": "Las features están disponibles antes de prediction_timestamp (2025-05-01), así que no hay problema del lado de las features. El problema está en la etiqueta. window_end (2025-06-30) es anterior al cutoff (2025-07-01), pero la fecha de fin de ventana no equivale a disponibilidad del label. El target=0 solo consta como observado en la extracción de 2025-07-15, posterior al cutoff. No hay label_available_at, delay ni regla de certificación, por lo que no se puede verificar que el 0 estuviera disponible y fuera definitivo al cutoff. Tampoco se puede descartar que sea un 0 provisional o por falta de reporte aún. La disponibilidad de la etiqueta queda entre 2025-06-30 (fin de ventana) y 2025-07-15 (extracción), con el cutoff dentro de ese intervalo. No se inventa una fecha de disponibilidad. No se puede clasificar como eligible ni como exclude con la evidencia actual."
    }
  ],
  "open_questions": [
    "¿Cuál es el label_available_at de D1, o el delay entre window_end (2025-06-30) y la disponibilidad del target?",
    "¿Existe una regla de certificación o cierre del target? ¿Un 0 en la extracción de 2025-07-15 es definitivo o puede cambiar por reportes tardíos?",
    "¿El 0 significa 'sin evento confirmado' o 'sin evento registrado aún'? Es decir, ¿se distingue un negativo observado de un pendiente?",
    "¿El cutoff 2025-07-01 se aplica a la disponibilidad del label, al fin de la ventana o a ambos?",
    "¿Se dispone de una extracción previa o de un historial de versiones del target para verificar su estado al cutoff?"
  ],
  "gate_decision": "NEEDS_REVIEW"
}
```
