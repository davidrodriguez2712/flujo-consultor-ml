---
skill: detect-leakage
version: "0.2.2"
fecha: 2026-10-13
condicion: treatment
estado: leakage_confirmado
modo: textual_guide_not_native
inputs:
  - path: case.md
    sha256: 4c41de990caa164c5749c2660a47dee3daa0dbd9b91c70018b5d5e59f3bae8e2
  - path: inputs/context.md
    sha256: 620e9e3f209b9c12361deb7147b318c6d3f6f346a24805348b55a9855c6d857e
  - path: inputs/observations.csv
    sha256: 8ec83a7f81b47dc4c80ab9097443af95f7feaccdaaf87e68c6157cbc018a111b
  - path: inputs/pipeline.py
    sha256: ca6985dbac6928444de93626f8e49cc18227e0c466c8fc6705b4910309f89483
---

## Resumen

El expediente demuestra leakage temporal por disponibilidad: la única feature seleccionada llega al motor después de la decisión declarada. Sus hechos corresponden al día previo, pero eso no la hace accesible a las 08:00. El backtest propuesto no sustenta el uso histórico de estos valores. Auditoría del expediente sintético mediante guía textual 0.2.2; no se verificó ejecución de Skill/plugin nativo.

## Hallazgos

- **Componente:** `payment_sum_previous_day`. **Conclusión:** leakage confirmado en el uso propuesto. **Mecanismo:** `pipeline.py` selecciona esta columna; en las tres observaciones, `prediction_at` es 2025-11-01T08:00:00Z y `available_at` es 2025-11-02T03:00:00Z. El contexto define esta última como el primer acceso efectivo del motor: el valor llega después del scoring, aunque `period_end` sea anterior. **Fuentes:** `inputs/context.md`, `inputs/observations.csv`, `inputs/pipeline.py`. **Confianza:** alta dentro del expediente; no demuestra una ejecución real. **Severidad:** impacto potencial sobre la validez del backtest; magnitud no estimable sin resultados ni decisiones observadas. **Acción:** retirar esos valores del backtest de las 08:00 y solicitar una fuente histórica accesible al corte, bajo decisión del owner.

## Evidencia

La utilidad fija autorizada se ejecutó y devolvió los hashes anteriores y tres filas CSV. No evalúa leakage. La comparación de timestamps y selección de columnas se realizó por inspección; el pipeline no se ejecutó, no se entrenó ni se calculó performance.

`period_end` es 2025-10-31T23:59:00Z: documenta hechos previos. La exportación del 20 de noviembre documenta extracción, no disponibilidad histórica. `missed_next_7d` es un outcome retrospectivo legítimo para evaluación según el contexto y no figura en `FEATURE_COLUMNS`. Cuenta y fechas son metadata, no features declaradas.

## Preguntas abiertas

¿Existe una fuente histórica alternativa disponible antes de las 08:00, con linaje y accesos corroborables? ¿Quién acepta la corrección del backtest? Faltan construcción completa, particiones, ajustes de preprocessing y momentos de entrenamiento para evaluar otras familias y disponibilidad de labels al entrenar.

## Recomendaciones

Reconstruir features mediante cortes de disponibilidad efectiva y conservar evidencia de acceso. Una alternativa válida requiere conjuntamente hechos previos y acceso efectivo al scoring, con linaje aplicable; no basta adelantar el timestamp del mismo valor posterior. Revisar después las familias pendientes sin interpretar esta auditoría como certificación universal. El owner debe aceptar la fuente y el corte antes de reutilizar la feature; no se aprueban gates ni uso productivo.
