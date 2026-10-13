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
estado: "auditoría parcial con límites; no aprueba gates"
condicion: treatment

## Resumen

No se confirma leakage en el expediente de muestra. La feature `usage_previous_30d` está disponible antes de `prediction_at` en las 6 filas, el target no entra en las features y el scaler se ajusta solo con train. Las entidades recurrentes (C01–C03) son parte del escenario declarado y no prueban contaminación. Quedan riesgos por evidencia incompleta: el código de entrenamiento no está y la muestra es de 6 filas sin métricas.

## Hallazgos

1. **Recurrencia de entidad entre train y evaluation.** Componente: partición/entidad. Mecanismo: mismo `customer_id` en historia y scoring; esperado por el escenario. Fuente: context.md; CSV filas 2–7. Confianza: alta. Severidad: baja. Acción: reportar métricas separadas para clientes conocidos y nuevos.
2. **Disponibilidad de feature y target solo declarada.** Componente: features/labels. Mecanismo: `feature_available_at` y `label_available_at` son metadatos; no hay evidencia de proceso. Fuente: CSV; context.md. Confianza: media. Severidad: media. Acción: aportar la ventana de cálculo de `usage_previous_30d` y el corte de certificación del target.
3. **Código de split/entrenamiento incompleto.** Componente: entrenamiento/particiones. Mecanismo: pipeline.py solo cubre preparación; no muestra filtro de labels disponibles al 2025-06-01 ni folds. Fuente: pipeline.py; context.md. Confianza: media. Severidad: media. Acción: aportar el código de entrenamiento y verificar el filtro `label_available_at ≤ 2025-06-01`.

## Evidencia

- Timestamps (inspección manual de 6 filas, no ejecución): train `feature_available_at` 2025-04-30T23:00Z ≤ `prediction_at` 2025-05-01; `label_available_at` 2025-05-09 < corte de entrenamiento 2025-06-01. Evaluation `feature_available_at` 2025-06-01T23:00Z ≤ 2025-06-02; `label_available_at` 2025-06-10 usado solo retrospectivamente, según context.md.
- pipeline.py: `scaler.fit_transform` sobre train y `scaler.transform` sobre evaluation; `feature_columns = ["usage_previous_30d"]`.
- Utility check_inputs.py: hashes de 4 archivos; observations.csv con 6 filas y 7 columnas esperadas.
- No se ejecutó pipeline.py ni se entrenó modelo. No hay AUC ni resultados.

## Preguntas abiertas

- ¿Cómo se construye `usage_previous_30d` y cuál es su ventana real?
- ¿Qué código entrena el modelo y aplica el filtro de labels?
- ¿El código de producción coincide con pipeline.py?
- ¿Cuántos clientes evaluados son nuevos frente a conocidos?

## Recomendaciones

- Mantener la recurrencia como escenario válido; no retirarla por sí sola.
- Obtener evidencia de proceso para disponibilidad de feature y target antes de cerrar la auditoría.
- Revisar código de entrenamiento y folds; ejecutar checks en un entorno autorizado si se requiere.
- Separar métricas de clientes conocidos y nuevos.
- Esta auditoría no certifica producción ni aprueba gates; la revisión humana de proceso sigue siendo necesaria.
