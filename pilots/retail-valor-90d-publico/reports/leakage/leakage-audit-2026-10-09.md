---
skill: detect-leakage
version: 0.1.0
fecha: 2026-10-09
proyecto: retail-valor-90d-publico
inputs:
  - "analysis/retail_temporal.py sha256:0b4bc6e72647dff21f16ca3bbd2abc245e84eca1e1963a72f95ef08ea1616825"
  - "analysis/retail_models.py sha256:f102399877c4928edc580c42e3d61c01fcb90da42aac4aabcaf30a3e6b59f9d0"
  - "analysis/run_retail.py sha256:b20573a9aea3b74b450119a8d69771ead962ff0d6783513685851f8457b80cf5"
  - "reports/execution/snapshot_checks.json sha256:a764ecb9a0f21c78fbc2f2e1c2a5984c99e47de5ab33f23087500dfe33c6c939"
  - "validation/evaluation_contract.yaml sha256:7c006d5440b88e07e3b04cad040d57775714510695c51ae6a30874c52ab8f83b"
estado: Sin leakage confirmado en construcciones inspeccionadas; disponibilidad real no determinable.
---
# Auditoría de leakage antes de entrenar

## Resumen

Ventanas semiabiertas, elegibilidad pasada, labels maduras y lista explícita de ocho features. No leakage confirmado en código/tests inspeccionados; no constituye garantía sobre información histórica que UCI no conserva (ingestion/revisiones). Shared customers es válido para repriorizar clientes conocidos.

## Hallazgos

### Alto — disponibilidad histórica no acreditada

Componente: fuente y reconciliación entre hojas. Familia: post-event/temporal. Mecanismo potencial: una transacción/corrección podría publicarse después de su invoice_at; comparar patrones entre hojas usa el archivo histórico completo. Confianza: No determinable; no existe fecha de ingestion ni versionado operacional. Evidencia: contrato timestamp_policy, ausencia de campos. Impacto: simulación puede sobrestimar información disponible en producción. Prueba necesaria: snapshots reales as-of e ingestion. Acción: mantener como supuesto explícito del benchmark, no acreditar readiness comercial.

### Medio — dependencia entre snapshots

Componente: entrenamiento mensual. Familia: diseño de validación, no contaminación confirmada. Mecanismo: mismos clientes/horizontes aparecen en varios snapshots maduros. Confianza: Confirmado para dependencia; no leakage demostrado. Evidencia: snapshot_checks fit_checks. Impacto: filas no independientes, tamaño efectivo menor. Acción: no intervalos IID, considerar comparación por período; no imponer GroupKFold a un objetivo de clientes conocidos.

### Informativo — separación de futuros y transformaciones

Target/post-event/temporal/entity: target y label_end fuera de FEATURES; recencia/tenure desde historial anterior, sumas por ventanas. Train-test/CV/preprocessing: label_end <= fit, StandardScaler dentro Pipeline.fit(train); HistGradient sin early stopping oculto. Target encoding/resampling/feature selection/tuning: no usados. Join: aggregate cliente luego joins one_to_one; frecuencia por factura, no por línea. No shared ID como predictor ni saldo global futuro. Confianza: Confirmado por código y tests, limitado a artefactos auditados.

## Evidencia

11 tests temporales (parametrizados incluidos) validan límites, cero futuro con cobertura completa, cancelación positiva, exclusiones, multiplicidad y perturbación del futuro. 11 tests modelos validan invariancia al target/orden scoring, finitud, keys y madurez. Tests runner verifican hashes de contratos y representación derivada, escape de paths y bloqueo explícito del holdout. Logs en reports/execution/; suite final: 35 tests pasan.

Snapshot checks: 14 cutoffs; 39.677 filas train/development y 2.768 elegibles reservados final. Fechas históricas <cutoff y targets en horizonte en todos, sin resumir outcomes finales. Primer fit 2.652 filas/1 snapshot; último development30.673 filas/10 snapshots. Al fit final13 snapshots/39.677 filas potenciales. Clientes compartidos intencionales y registrados. Los checks de integridad del archivo reservado leen bytes/hash, no métricas finales.

No se afirma independencia ni ceguera completa a distribución: Diagnosis describió fuente global. No correlations/feature importance del holdout. Alta señal del baseline monetario no probaría leakage: deriva solo de compras pasadas.

## Preguntas abiertas

¿Cuál era latencia real? ¿Qué líneas fueron revisiones? ¿ID estable en operación? ¿Capacidad100 y población multipaís representan proceso real? Todas no determinables con la fuente pública; encargo simulado las declara.

## Recomendaciones

Continuar development bajo supuestos aprobados, preservando holdout reservado. Antes de modelar se verifican contratos/dataset; resultados no redefinen ventanas. Para despliegue exigir ingestion as-of y nueva validación operacional. Esta auditoría no entrena ni propone algoritmo; las configuraciones son del plan aprobado. No promover skill por uso manual único.
