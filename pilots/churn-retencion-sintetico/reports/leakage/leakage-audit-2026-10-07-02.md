---
skill: detect-leakage
version: 0.1.0
fecha: '2026-10-07'
proyecto: churn-retencion-sintetico
modo: aplicación manual de pautas por asistente; sin invocación nativa ni review independiente
inputs:
- path: analysis/baseline.py
  sha256: 8c41489662880ce04a5b3b860f261987abfd860d1672f07459444503db352c2f
- path: analysis/test_baseline.py
  sha256: 92f02ac2ea00880e7120c4a11de6daf67b2d52b24acd515bb39765cb0a9e3746
- path: validation/validation_design.md
  sha256: 5addda286a3a07f392a5fc54c0353194abb74b3d0546b83d494758feacf9f0b2
- path: analysis/outputs/baseline-audit.json
  sha256: dc44c044b8726de4630c83fe2728b02e7ca01a3c4d2065272e1e06bd57c5f298
- path: analysis/outputs/baseline-development/policy.json
  sha256: 63d826c321117a8468c9bdd57e46f00750daadfa429086b253ac0b37edc507bb
- path: analysis/outputs/baseline-development/results.json
  sha256: 5af1bddc83c922eeee46a83562c1d2eb2e2e213ec3567f98f3b814f3717dc27c
estado: pipeline de desarrollo auditado; no se observaron infracciones en los checks;
  revisión humana pendiente
---

# Auditoría del pipeline de desarrollo

## Resumen

Alcance: baseline.py, transformaciones, ajuste por fold, selección y evaluación de desarrollo. Complementa, sin sobrescribir, la auditoría previa aprobada. Los checks no muestran uso de información futura en el pipeline inspeccionado. La auditoría se hizo después de entrenar; no se entrenó ni se diseñó otro modelo durante esta revisión.

## Hallazgos

### Alto — Riesgo: outcomes presentes en fuentes

Componente: CSV de labels. Familias: target/post-event leakage. Mecanismo potencial: pasar target, cancellation_at o label metadata como predictores. Evidencia: load_development usa allowlist de cuatro features y predict lee solo esas cuatro; cambios de target, MRR y cancellation_at no alteran los scores en los nueve folds. Impacto potencial: ranking artificial. Acción: conservar allowlist y repetir regresión si cambia el pipeline. No se confirmó uso indebido.

### Alto — Riesgo: maduración de labels

Componente: selección de train. Familia: temporal leakage. Mecanismo potencial: aprender outcomes que aún no se conocían en el cutoff. Evidencia: filtros por prediction_timestamp y label_available_at; fit rechaza labels futuras y filas de scoring. Checks pasan en nueve folds; septiembre inicia con febrero–julio, sin labels de agosto. Acción: conservar condiciones al evaluar o extender el pipeline. No se confirmó infracción.

### Medio — Riesgo: contaminación de transformaciones o codificación

Componente: mediana y frecuencias por grupo. Familias: preprocessing/target encoding/cross-validation. Mecanismo potencial: calcular mediana o tasas con validation/test. Evidencia: cada fold ajusta fit solo con train; modelo y mediana coinciden con recálculo desde train. Grupos usan targets de train, no de validation; no hay selección de features ni tuning. No hay resampling. Acción: ajustar nuevamente dentro de cada fold al cambiar método. No se confirmó infracción.

### Medio — Riesgo: ampliaciones de joins y agregaciones

Componente: carga. Familias: aggregation/join leakage. Mecanismo potencial: duplicar snapshots o agregar tickets posteriores. Evidencia: baseline consume conteos preexistentes auditados en diagnosis y unión 1:1 de snapshots/labels por customer_id y timestamp; claves sin duplicados. Los 26 checks de datos previos permanecen vigentes por hashes. Acción: volver a auditar si se incorporan tickets brutos u otras tablas.

### Informativo — Confirmado: historia de entidades repetidas

Componente: particiones temporales. Familias: entity/train-test contamination. Clientes pueden repetirse, pero las claves cliente-mes de train y validation no se solapan. La decisión aprobada es scoring futuro de clientes existentes, no desempeño en clientes nuevos. Usar historia previa es coherente con ese contrato; ID no modifica riesgo, solo desempata. No se marca esta repetición como leakage por sí sola.

### Informativo — Confirmado: holdout separado del cálculo

Componente: load_development y run. Se descartan fechas posteriores a mayo antes de interpretar targets para entrenamiento/evaluación. El archivo completo se lee y hashea para integridad; esto no equivale a aislamiento físico del test. Ninguna métrica individual de julio–diciembre intervino en tuning o elección de parámetros. Modelo final congelado; test sin puntuar. Acción: preservar política y hash al ejecutar la evaluación autorizada.

## Evidencia

analysis/outputs/baseline-audit.json: siete checks globales verdaderos; nueve folds con recálculo de modelos/medianas/métricas e invariancia a outcomes. Ocho tests unitarios pasan. Cinco outputs JSON idénticos en reproducción. Datos y protocolo conservan hashes. No hay hallazgos críticos confirmados en este alcance.

## Preguntas abiertas

No se dispone de fuentes reales para verificar semántica y disponibilidad operacional fuera del generador. No se ha ejecutado el runner de test ni se auditó producción. La review del autor no sustituye review independiente. Estos límites son No determinable en este piloto, sin extrapolación al cliente real.

## Recomendaciones

Revisar ejecución antes de evaluar holdout; comprobar código y hashes del runner de evaluación, mantener modelo fijo y excluir labels pendientes. Repetir auditoría si se modifican fuentes, ventanas, features, transformaciones o política. No promover la skill por esta aplicación manual.
