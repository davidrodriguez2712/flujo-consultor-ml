---
skill: detect-leakage
version: 0.1.0
fecha: '2026-10-08'
proyecto: riesgo-credito-sintetico
inputs:
- path: analysis/credit_baseline.py
  sha256: b1ffc72b9b58a698bc020389ef8582ceb24e14856b529ed6ed2e2f6392d455b1
- path: analysis/credit_final.py
  sha256: 33a00517b0f3ba69ac764a0bdb53431cab793b0d950680b8888e7643a6056e6e
- path: reports/final-validation/final-freeze.json
  sha256: 13d03d735e9eaa3a695a5109aef1777c7d68fffa279995231ad9ca4d693e1cad
- path: analysis/outputs/baseline-final/model.json
  sha256: 5e65969197ea144f806ad3bf0fff278b6f28363ffbaacbc8df985e90dfef2c87
- path: analysis/outputs/baseline-final/metadata.json
  sha256: f1fe59fdca6e34cac46f793c3ec318d9eefdeae32396dc93291397ba3f19c931
estado: Auditoría del pipeline ejecutado; sin leakage observado en controles disponibles,
  uso real no validado.
---

# Auditoría del pipeline ejecutado

## Resumen

Controles inspeccionados de disponibilidad, join y fit/predict respetan el diseño. No se detecta uso de columnas posteriores o labels de scoring durante entrenamiento. Esta es una auditoría del código/output, no prueba absoluta de ausencia de todos los riesgos ni validación real del negocio.

## Hallazgos

### Crítico / Alto

Sin leakage confirmado en el pipeline ejecutado. El baseline lee únicamente las cinco features; target, IDs y decisiones no entran como predictors. Las trampas posteriores siguen en raw y no se usaron.

### Medio

Riesgo de interpretación: métricas en concedidas no identifican desempeño en rechazadas. Confirmada cobertura de labels del Top-100 global de22–26%; no convertir un score en PD calibrada de esa población. No es por sí mismo leakage.

La evaluación no es ciega: raw/generator disponibles y outcomes usados en QA previa. Riesgo de futura contaminación si se modificase configuración basándose en estos resultados; no ocurrió tuning en el código revisado. No seguir reusando este holdout para seleccionar mejoras.

### Bajo / Informativo

Clientes recurrentes son compatibles con escenario aprobado; se reportan grupos. No llamar contaminación al overlap por sí solo. No se usaron target encoding, resampling, selección de features global, cross-validation o agregaciones temporales nuevas; esos componentes no aplican en este pipeline y requieren nueva auditoría si se introducen.

## Evidencia

Train2140, cutoff2025-07-01, labels<=cutoff, última solicitud2025-03-25; IDs disjuntos respecto de scoring900. Referencia249/2140. Model/transformaciones fit solo train, codigo600iteraciones sin tuning/refit mensual. Join application_id1:1, history.available_at<=scoring. Scoring usa applications/history; predicciones persistidas antes de load_labels. Auditoría aritmética coincide; hashes del freeze intactos.

## Preguntas abiertas

Disponibilidad y políticas reales de una entidad financiera no determinables: fixture ficticio. Implementación de revisión online y efecto causal tampoco están evaluados. Cambios posteriores requerirán nuevo case/protocolo y datos de evaluación independientes.

## Recomendaciones

Mantener código/configuración/output congelados. No recalibrar con holdout ni inventar labels de rechazadas. Llevar límites de población, calibración y acción al memo; conseguir evidencia apropiada antes de una política real. No entrenar con columnas posteriores para demostrar cuán altas podrían ser las métricas.
