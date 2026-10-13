---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-12
inputs:
  - path: case.md
    sha256: 71613379fe4387f19de862020de6bcdedec00623aeb452bbdff9491690b61d39
  - path: inputs/context.md
    sha256: 2d20272658305e9620515452c404e52d7b2015db0d0a30412287c4aa02a0c1b0
  - path: inputs/observations.csv
    sha256: cbcae4e4f891739ea487feda3f7e1eac58cf9fbe3303b774b5563770f7127462
  - path: inputs/pipeline.py
    sha256: 8fc757e4a3209efdedd3e1b8de6f0b77109557fb6335ac263cd3cea9b3788011
estado: auditoría con límites declarados; sin aprobación de gates
condicion: treatment
---

## Resumen
En el expediente sintético L02 no se confirma leakage. La feature usage_previous_30d tiene disponibilidad anterior a prediction_at, las etiquetas de train están disponibles antes del corte de entrenamiento y el escalado se ajusta solo con train. La recurrencia de clientes es un escenario declarado, no contaminación. Quedan brechas: origen de particiones, código de entrenamiento y una muestra de 6 filas.

## Hallazgos
1. **Recurrencia de customer_id** (partición/entidad). Mecanismo: C01–C03 aparecen en train y evaluation, como declara context.md. Fuente: observations.csv filas 2–7; context.md. Confianza: alta. Severidad: baja. Acción: informar que la evaluación mide clientes conocidos, no nuevos.
2. **Disponibilidad temporal** (usage_previous_30d, labels). Mecanismo: feature_available_at (2025-04-30T23 / 2025-06-01T23) ≤ prediction_at en las 6 filas; label_available_at de train (2025-05-09) < corte 2025-06-01; labels de evaluation (2025-06-10) solo para evaluación retrospectiva. Fuente: observations.csv; context.md. Confianza: media, limitada a timestamps declarados. Severidad: baja. Acción: verificar en el código real.
3. **Orden fit/transform** (pipeline.py líneas 6–7). Mecanismo: scaler ajustado solo con train; evaluation solo transform. Fuente: pipeline.py. Confianza: alta para el código mostrado. Severidad: baja. Acción: ninguna en el código mostrado.
4. **Construcción de particiones y entrenamiento no inspeccionadas** (partition, modelo, CV). Mecanismo: ningún código asigna particiones ni entrena; el orden es declarativo (pipeline.py línea 1). Fuente: pipeline.py; context.md. Confianza: no determinable. Severidad: riesgo medio. Acción: solicitar el código real.

## Evidencia
- Ejecutado: check_inputs.py (hashes, bytes, 6 filas, columnas).
- Conteo de particiones (3 train, 3 evaluation) y comparación de timestamps: lectura manual de observations.csv, no script.
- Lectura de context.md y pipeline.py; pipeline.py no se ejecutó.
- Skill detect-leakage 0.2.0 cargada (report-context.json, skill_sha256 c2a2440477d9985489b71f4d8c50380ccd7985635d02eab330cfee0f7e5856c4).
- No realizados: entrenamiento, CV, métricas, búsqueda en repositorio.

## Preguntas abiertas
- ¿Cómo se generan partition y prediction_at en producción? ¿Hay gap entre train y evaluation?
- ¿Cuál es la ventana exacta de usage_previous_30d y su corte de disponibilidad?
- ¿Cuál es el código real de entrenamiento y validación? ¿CV con folds por cliente?
- Sin AUC ni resultados: no se evalúa si la señal es perfecta o igual al target.
- La muestra de 6 filas no acredita distribución ni generalización.
- No se pudo verificar si existía un reporte previo en reports/leakage/; Read estaba restringido.

## Recomendaciones
- Mantener usage_previous_30d con disponibilidad documentada hasta revisar su construcción.
- Declarar que la evaluación es sobre clientes conocidos.
- Solicitar código real de split y entrenamiento, y verificar con datos completos antes de conclusiones de producción.
- Esta auditoría no certifica ausencia de leakage; la revisión humana de proceso sigue siendo necesaria.
