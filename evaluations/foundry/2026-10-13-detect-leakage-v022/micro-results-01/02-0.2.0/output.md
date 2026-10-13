---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-13
modo: guia_textual
estado: no_recomendado_para_scoring_hoy
inputs:
- context.md
- dictionary.json
- observations.csv
---

## Resumen

No recomendar usar `complaint_count` para scoring hoy. El expediente no prueba que el conteo estuviera disponible en `prediction_at` (2025-06-01). La exportación es posterior (2025-08-01) y el conteo podría reflejar estado posterior al scoring.

## Hallazgos

- **Riesgo de leakage temporal (no determinable):** falta fecha de disponibilidad, ventana de conteo y código de construcción. Mecanismo posible: conteo tomado al exportar.
- **Señal no concluyente:** tres filas no sustentan inferencia estadística.

## Evidencia

Lectura de `dictionary.json`: `feature_available_at` y `construction_code` son `null`. Lectura de `context.md`: no se conoce si el conteo refleja el estado al scoring o al exportar. Lectura de `observations.csv`: tres filas, todas con `exported_at` posterior a `prediction_at`. No se ejecutaron checks deterministas.

## Preguntas abiertas

- ¿Cuándo existía `complaint_count` en producción?
- ¿Qué ventana temporal cuenta?
- ¿Hay snapshot histórico al scoring?

## Recomendaciones

- Excluir `complaint_count` del scoring hasta confirmar disponibilidad.
- Evaluar retrospectivamente solo con snapshot verificable.
- Cambiaría la conclusión: fecha de disponibilidad ≤ 2025-06-01, ventana cerrada antes del corte, código que muestre conteo como de `prediction_at`, y snapshot histórico.