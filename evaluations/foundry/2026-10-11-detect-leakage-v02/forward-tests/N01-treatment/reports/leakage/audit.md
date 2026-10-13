---
skill: detect-leakage
version: "0.2.0"
fecha: 2026-10-11
condicion: treatment
estado: auditado_con_leakage_confirmado
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

El expediente no sustenta usar `payment_sum_previous_day` en la decisión diaria de las 08:00. Sus hechos preceden a la predicción, pero el motor accede a ellos después. Un backtest que utilice esos valores como disponibles al decidir incorporaría información ilegítima. El target posterior es legítimo para evaluación retrospectiva según el contexto. No se calculó performance ni se ejecutó el pipeline.

## Hallazgos

**Confirmado — disponibilidad temporal.** Componente: `payment_sum_previous_day`. Mecanismo: `features()` selecciona esa columna sin filtrar su disponibilidad; las tres cuentas tienen `prediction_at=2025-11-01T08:00:00Z` y `available_at=2025-11-02T03:00:00Z`, 19 horas después. Aunque `period_end=2025-10-31T23:59:00Z` representa hechos pasados, no habilita acceso a las 08:00. Fuente: `inputs/context.md`, `inputs/observations.csv`, `inputs/pipeline.py`. Confianza: alta dentro del expediente sintético; severidad: alta, por invalidar la representación del scoring declarado. Acción: excluir esos valores de la reconstrucción de esta decisión y reconstruir features con fuentes y cortes de disponibilidad verificables. La ejecución real del backtest no está demostrada.

## Evidencia

La utility fija `.runtime/check_inputs.py`, ejecutada con el Python autorizado, produjo los hashes del frontmatter y contó tres filas CSV. No evalúa leakage.

La comparación de timestamps y la selección de columnas proceden de lectura directa, no de checks automatizados del pipeline. El fragmento define únicamente `FEATURE_COLUMNS = ["payment_sum_previous_day"]`; `account`, fechas y `missed_next_7d` no son features declaradas. La exportación del 20 de noviembre con outcomes conocidos no prueba contaminación por sí misma. No hay evidencia de uso del target para construir features, ni de un mecanismo de leakage por identidad.

El fragmento no contiene entrenamiento, particiones, cross-validation ni transformaciones aprendidas; su validez no puede determinarse con este expediente. Los resultados del sistema desplegado tampoco fueron comprobados.

## Preguntas abiertas

¿Existe una fuente accesible antes de las 08:00 con ventana de hechos y disponibilidad histórica documentadas? ¿Cómo aplica el pipeline completo el corte temporal y resuelve datos aún no disponibles? ¿Cuándo se entrena y qué labels estaban disponibles entonces? ¿Qué población, particiones y transformaciones utiliza el backtest?

## Recomendaciones

Preparar una reconstrucción histórica que imponga `available_at <= prediction_at` y documente también la ventana de hechos. Usar información más antigua solo si su acceso anterior al scoring puede verificarse; aumentar filas no resuelve esta brecha. Cualquier cambio de horario o definición requiere decisión del responsable del proceso.

Mantener los outcomes posteriores exclusivamente para evaluar una vez observado el horizonte. Revisar después el código completo de joins, fit y splits y la disponibilidad de labels al entrenamiento. Este reporte recomienda acciones; no acepta decisiones de negocio, gates ni promociones del Foundry. Se aplicó la guía suministrada, sin instalar ni invocar un plugin o una herramienta Skill.
