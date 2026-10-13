# Technical handoff

## Componentes

- retail_source.py: adquisición y normalización/auditoría UCI, sin mutar raw.
- retail_temporal.py: reconciliación de copias, filtros con razones, snapshots y train maduro.
- retail_models.py: baseline/RFM y dos configuraciones fijas, ocho features explícitas.
- retail_evaluation.py: Top-K, métricas y regla de aceptación.
- run_retail.py: entrypoints originales con contratos/selección/intent único.
- reproduce_retail.py: reconstrucción y comparación contra referencias, en carpeta nueva de una copia.
- tests: límites temporales, exclusiones, invariancia de scoring, aceptación, hashes/paths y comparadores.

## Contratos y provenance

YAML de Framing/evaluación y representación JSON aprobada; aprobaciones externas con hashes, sin reescribir metadata histórica. Source Excel SHA en data/source_manifest.json. Pipeline usa paths relativos al root recibido. Skills son snapshots experimentales para metodología, no dependencias de Python. El compilador ACOS se instala/configura aparte para consultar status/gates; no se importa su código desde el análisis.

## Datos y aislamiento

Normalizado preserva todas las líneas. Cross-sheet copy_map y excluded_transactions mantienen provenance. customer_snapshots contiene13 períodos train/development; reserved/holdout_snapshot es referencia final ya abierta en ejecución única. Reproductor recalcula mismos cortes/modelos sin reselección y escribe en reproduced; guarda nuevo entorno/tiempo, compara tolerancias.

## Invariantes

Historia[cutoff-180d,cutoff), target[cutoff,cutoff+90d), madurez label_end<=fit, mismo cliente/población por método, score descendente e ID textual lexicográfico. ID/target/fecha absoluta no features. Scaler fittrain, sin tuning/early stopping oculto. Compartir clientes es intencional; no confundir con generalización a clientes nuevos.

## Operación y fallos

No modificar scores/contratos para hacer pasar métricas ni repetir comando final. Ante fallo conservar logs, identificar cambio de dato/paquete/interpretación y crear nueva versión de trabajo si cambia la estrategia. Reproducción en copia no extiende evidencia estadística ni abre un holdout nuevo. No usar endpoints externos, claves ni dependencias del Foundry para ejecutar análisis.

## Límites de soporte

Benchmark, no servicio productivo ni integración de campaña. Sin ingestion/latencia real, SLA, deployment, experimentación causal o monitorización operacional acreditados. Python3.13 y versiones fijadas; soporte analítico multiplataforma no demostrado por esta reproducción local.
