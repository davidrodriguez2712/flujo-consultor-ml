# Engagement retail con datos públicos — Plan de ejecución

> **Para agentes ejecutores:** SUB-SKILL REQUERIDA: usar `superpowers:executing-plans` para implementar este plan en la sesión principal, tarea por tarea. Los pasos usan checkboxes para registrar avance. No delegar sin autorización del usuario.

**Estado:** plan aprobado por David. Discovery aprobado y cerrado; tarea 2 en Framing, contrato propuesto preparado para revisión antes de Diagnosis.

**Goal:** recorrer ACOS con transacciones reales de Online Retail II y entregar una propuesta retrospectiva de priorización por ventas positivas esperadas a 90 días, comparada con un baseline.

**Architecture:** inicializar un workspace independiente con el compiler existente y mantener el análisis dentro del piloto. Separar adquisición/auditoría, construcción temporal y evaluación; los contratos aprobados son entradas explícitas del pipeline. Los resultados no modifican el producto ni promueven capacidades del Foundry.

**Tech Stack:** Python local, ACOS existente, pandas, NumPy, openpyxl, scikit-learn y pytest. Usar un entorno aislado del piloto, registrar versiones resueltas y congelarlas después de comprobar el entorno. No añadir estas dependencias al paquete ACOS.

**Spec:** [diseño aprobado](../specs/2026-10-09-retail-public-data-engagement-design.md).

## Global Constraints

- Cliente, owner, encargo y capacidad simulados; transacciones reales e históricas.
- Decisión: lista de hasta 100 clientes identificables al inicio de cada mes.
- Horizonte de target: 90 días; elegibilidad basada en compra válida en los 180 días anteriores.
- Target de ventas positivas registradas en GBP, no CLV completo, margen, ingreso neto ni uplift.
- Original inmutable, provenance y SHA256; limpieza y exclusiones trazables.
- Features anteriores al cutoff; labels de entrenamiento completas y maduras a la fecha de fit.
- No etiquetas cero para horizontes incompletos. Compartir clientes entre períodos reproduce el uso propuesto.
- Máximo un modelo sencillo y una alternativa más compleja; mantener baseline es un resultado válido.
- Sin llamadas API de pago, contactos comerciales, publicación externa o cambios del compiler.
- Foundry en lectura; snapshots experimentales provisionales, sin promoción ni candidates automáticos.
- Gates humanos y estado canónico en `.acos/state.yaml`; no avanzar por existencia de archivos.
- No inicializar Git en el workspace original. Conservar registros por tarea y hashes; no hacer commits en este directorio.
- Español en documentación; terminología y campos técnicos en inglés.

## Review Focus

1. Hojas y nombres del Excel distintos de la ficha: auditar, mapear explícitamente o detener carga; tarea 1.
2. Facturas canceladas, ajustes, precios/cantidades no válidos y duplicados ambiguos: exclusiones visibles sin borrar fuente; tareas 1 y 3.
3. Horizontes incompletos, compra exactamente en cutoff y label que madura después del fit: límites temporales exactos; tarea 3.
4. IDs ausentes, menos de 100 elegibles y empates: cobertura excluida, K efectivo y orden determinista; tareas 2 y 5.
5. Ranking concentrado en pocos clientes o resultados inestables por período: no afirmar utilidad causal o ventaja general por una media agregada; tareas 5 y 6.

## Archivos y responsabilidades

Todos los paths siguientes son relativos a `pilots/retail-valor-90d-publico/`, salvo el perfil de entrada y este plan.

| Archivos | Responsabilidad |
|---|---|
| `docs/acos/pilots/retail-valor-90d-profile.yaml` (fuera del piloto) | Entrada canónica al compiler |
| `.acos/*`, adaptadores y snapshots generados | Contexto, composición, procedencia y continuidad |
| `analysis/retail_source.py`, `analysis/test_retail_source.py` | Descarga, normalización y auditoría de fuente |
| `analysis/retail_temporal.py`, `analysis/test_retail_temporal.py` | Compras válidas, elegibilidad, features, target y madurez |
| `analysis/retail_models.py`, `analysis/test_retail_models.py` | Fit, predicción y ranking de modelos |
| `analysis/retail_evaluation.py`, `analysis/test_retail_evaluation.py` | Métricas, Top-K y checks de aceptación |
| `analysis/run_retail.py` | CLI local que coordina módulos y contratos, sin avanzar gates |
| `data/raw/`, `data/interim/`, `data/processed/` | Original, transacciones normalizadas y snapshots |
| `framing/retail_contract.yaml`, `validation/evaluation_contract.yaml` | Reglas semánticas y evaluación aprobadas |
| `reports/<stage>/`, `evidence/`, `decision/`, `delivery/`, `handoff/` | Evidencia, revisión, recomendaciones y reproducción |

No crear todas las carpetas por anticipado: generar las del compiler y añadir las del piloto al producir cada artefacto.

### Tarea 1: Inicialización y paquete Discovery

**Files:** perfil de entrada; `analysis/retail_source.py`, `analysis/test_retail_source.py`; `analysis/requirements.in`, `analysis/requirements.lock.txt`; `data/raw/online_retail_II.xlsx`, `data/source_manifest.json`; `context/business_context.md`; `reports/discovery/`.

**Interfaces:** `download_source(url: str, destination: Path) -> dict`; `load_transactions(path: Path) -> tuple[pandas.DataFrame, dict]`; `audit_transactions(frame: pandas.DataFrame) -> dict`. Frame normalizado con `invoice_id`, `stock_code`, `description`, `quantity`, `invoice_at`, `unit_price`, `customer_id`, `country`, `source_sheet`, `source_row`.

- [x] Crear el perfil: DIAGNOSE/PREDICT/PRIORITIZE_SELECT, Excel, temporal/panel/tabular/supervised, labels `partial`, Discovery, analytical report y decision memo; incluir supuestos y límites del diseño.
- [x] Leer instrucciones del Foundry y escanear su inventario actual. Obtener preview del resolver existente y registrar selección, gaps y fallbacks en `reports/discovery/composition.md`; no usar un inventario histórico como lista fija.
- [x] Crear workspace desde `pilots/` con `../.venv/bin/acos init retail-valor-90d-publico --profile-file ../docs/acos/pilots/retail-valor-90d-profile.yaml`, confirmando la composición y snapshots conforme al alcance aprobado. Conservar stdout y no activar `--llm`. Detenerse si destino existe o aparece una capacidad fuera del alcance.
- [x] Crear entorno `.venv-retail` y dependencias locales: pandas, NumPy, openpyxl, scikit-learn y pytest, usando releases compatibles con Python local. Registrar versión de Python y `pip freeze`; no modificar `.venv` ni `pyproject.toml` del producto.
- [x] Escribir tests de carga con Excel pequeño de dos hojas: conservar ambas, mapear variantes documentadas de columnas, mantener customer_id ausente como ausente y rechazar columna requerida faltante. Escribir test de fuente existente con hash diferente: rechazar reemplazo. Ejecutarlos y registrar RED antes de implementar.
- [x] Implementar adquisición con biblioteca estándar: URL de descarga obtenida desde UCI, staging temporal, extracción exclusiva del XLSX esperado sin escape de rutas, movimiento sin sobrescritura. Manifest con landing URL, download URL, DOI, licencia, fecha UTC, tamaño y hash. Una fuente existente con hash idéntico se verifica, no se vuelve a descargar.
- [x] Implementar carga/auditoría sin limpieza destructiva. Reportar por hoja: filas, schema, fechas, ID ausente, códigos, cancelaciones, cantidades/precios no válidos, duplicados potenciales y errores de parseo; conservar filas y ubicación original.
- [x] Ejecutar tests GREEN y descargar/auditar el dataset completo; registrar divergencias frente a la ficha, sin corregir datos para hacer coincidir conteos.
- [x] Completar brief, provenance y `data/data_contract.yaml` como propuesta; personalizar MANUAL/STATE/TASKS. Ejecutar `acos status`, `acos next`, `acos validate --gate discovery` y conservar outputs con códigos de salida.
- [x] Presentar paquete Discovery a David. Estado final esperado: Discovery pendiente de revisión, no PASS automático. Tras aprobación explícita registrar reviewer/evidencia/perfil y avanzar a Framing.


### Tarea 2: Framing y Diagnosis con evaluación congelada

**Files:** `framing/framing.yaml`, `framing/retail_contract.yaml`, `data/data_contract.yaml`, `analysis/analysis_plan.md`, `analysis/selection_plan.md`, `validation/evaluation_contract.yaml`, `reports/framing/`, `reports/diagnosis/`, `evidence/findings.md`.

**Interfaces:** contrato retail con `capacity=100`, `history_days=180`, `baseline_days=90`, `horizon_days=90`, semántica de compra válida, ID, productos y exclusiones. Contrato de evaluación con cutoffs, comparación, `holdout_cutoff`, `seed=20261009`, modelos permitidos y regla de recomendación.

- [x] Resolver desde la auditoría el mapping, códigos no comerciales, cancelaciones y duplicados. No exigir que toda línea sea mercancía ni descartar duplicados por mera igualdad. Si queda ambigüedad material, proponer exclusión trazada o BLOCKED.
- [x] Definir ID normalizado como representación textual estable, sin convertir NA a cliente literal ni mezclar identificadores. Fijar desempate lexicográfico ascendente sobre esa representación, después del score descendente.
- [x] Documentar target, elegibilidad, KPI, owner simulado y supuestos de observabilidad. Presentar Framing para revisión; registrar PASS solo tras aprobación y avanzar a Diagnosis.
- [x] Producir diagnóstico de clientes, cohortes, recurrencia, concentración, cancelaciones y cobertura excluida sin inspeccionar desempeño del holdout ni entrenar modelos.
- [x] Construir propuesta de cutoffs mensuales con 180 días de historia y 90 futuros completos. Holdout: último cutoff mensual admisible. Development: hasta cuatro cutoffs anteriores, con separación mínima de 90 días y al menos un snapshot de entrenamiento maduro disponible en cada fit. Elegir desde cobertura temporal, no desde resultados. Si hay menos de dos períodos development, documentar insuficiencia y revisar alcance.
- [x] Congelar antes de entrenar regla de decisión: modelo elegible si mejora ventas Top-K agregadas en development y no reduce ventas Top-K en más de la mitad de sus períodos frente al baseline; si ambos modelos son elegibles, escoger el sencillo salvo que la alternativa lo supere en ventas Top-K en todos los períodos development; si solo uno es elegible, seleccionar ese modelo. En holdout, solo recomendar modelo si no pierde frente al baseline; empate mantiene baseline. Documentar que es una regla del piloto, sin demostrar superioridad estadística o causal.
- [x] Presentar fechas, suficiencia temporal, aceptación, supuestos y contratos para revisión de Diagnosis/data-quality. Registrar gates tras aprobación; cualquier revisión posterior de estas reglas exige nueva versión y no puede llamarse holdout intacto si ya se observó.

### Tarea 3: Dataset temporal reproducible

**Files:** `analysis/retail_temporal.py`, `analysis/test_retail_temporal.py`; `data/processed/customer_snapshots.csv`; `reports/execution/snapshot_checks.json`.

**Interfaces:** `valid_purchases(frame: DataFrame, contract: dict) -> DataFrame`; `build_snapshot(frame: DataFrame, cutoff: Timestamp, contract: dict, observed_until: Timestamp) -> DataFrame`; `training_rows(snapshots: DataFrame, fit_at: Timestamp) -> DataFrame`. Snapshot: `customer_id`, `cutoff`, `label_end`, `target_sales_90d`, `recency_days`, `orders_90d`, `orders_180d`, `sales_90d`, `sales_180d`, `units_180d`, `distinct_products_180d`, `tenure_observed_days`.

- [x] Escribir tests RED: compra justo en cutoff pertenece al target, no a features; compra justo en label_end queda fuera del target; horizonte incompleto rechaza snapshot evaluable; no compras futuras con horizonte completo produce cero; label_end posterior a fit queda fuera de entrenamiento.
- [x] Añadir tests de cancelación con cantidad positiva y código c, cantidad negativa, precio cero, ID ausente, códigos excluidos y duplicado ambiguo: respetar contrato sin alterar el frame original. Las líneas excluidas conservan motivo y source_row.
- [x] Implementar transacciones válidas y ventanas semiabiertas. Requerir cobertura desde cutoff-180 días y hasta label_end; conservar customers con compras válidas en historia y agregar por factura para frequency.
- [x] Implementar snapshots y selección de entrenamiento por `label_end <= fit_at`, bajo supuesto explícito de observación inmediata; no permitir que transformaciones del futuro alteren snapshots anteriores.
- [x] Ejecutar tests GREEN y construir snapshots reales según contratos aprobados. Registrar filas por cutoff, clientes compartidos, ceros, suma de target, exclusiones y fechas máximas de features/labels.
- [x] Registrar hashes de contratos, fuente y outputs. Si checks fallan, mantener Execution BLOCKED; no sustituir datos con generación sintética.

### Tarea 4: Baselines y modelos acotados

**Files:** `analysis/retail_models.py`, `analysis/test_retail_models.py`, `analysis/run_retail.py`, `modeling/model_brief.md`, `reports/execution/model_runs.json`, `data/processed/development_predictions.csv`.

**Interfaces:** `fit_predict(train: DataFrame, score_rows: DataFrame, model_id: str, seed: int) -> DataFrame` devuelve IDs, cutoff y score; no usa target de score_rows. Model IDs: `historical_sales`, `rfm`, `ridge_log`, `hist_gradient_log`.

- [x] Escribir tests RED: agregar/modificar target del scoring no cambia predicción; orden de filas no altera asociación ID-score; entrenamiento vacío y features no finitas se rechazan; modelo inesperado se rechaza.
- [x] Implementar baseline principal `sales_90d`. RFM secundario: promedio de rangos percentiles calculados en la población del cutoff para menor recency, mayor orders_180d y mayor sales_180d; documentar empates y su papel exclusivamente comparador.
- [x] Implementar modelo sencillo Ridge(alpha=1) sobre log1p(target), con StandardScaler ajustado únicamente en train. Predicción expm1 con piso cero. No incluir ID, fecha absoluta ni label_end entre features.
- [x] Implementar como única alternativa HistGradientBoostingRegressor sobre log1p(target): learning_rate=0.1, max_iter=100, max_leaf_nodes=15, min_samples_leaf=20, early_stopping=False y random_state del contrato. Sin hyperparameter search. Si dependencia/modelo falla, registrar error sin sustituirlo silenciosamente.
- [x] Implementar CLI `python analysis/run_retail.py development --root .` que valida hashes/contratos, entrena separadamente para cada cutoff development y conserva scores y configuración. `holdout` será un subcomando separado, no se ejecuta durante development.
- [x] Ejecutar tests GREEN y development. Conservar resultados del baseline aunque el modelo pierda. Presentar paquete Execution; gate pendiente, no avance a Validation.

### Tarea 5: Evaluación y holdout final

**Files:** `analysis/retail_evaluation.py`, `analysis/test_retail_evaluation.py`, `validation/model_validation.md`, `reports/validation/`, `data/processed/holdout_predictions.csv`, `delivery/prioritization_retrospective.csv`.

**Interfaces:** `top_k(predictions: DataFrame, capacity: int) -> DataFrame`; `ranking_metrics(predictions: DataFrame, outcomes: DataFrame, capacity: int) -> dict`; `acceptance_decision(development: dict, holdout: dict, contract: dict) -> dict`. Métricas: `effective_k`, `eligible_count`, `top_k_sales`, `sales_share`, `mae`, delta frente al baseline y concentración Top-1/Top-10.

- [x] Escribir tests RED: 3 elegibles/capacidad100 devuelve K=3; empates preservan desempate contractual y orden; IDs repetidos o sin outcome completo se rechazan; ventas totales cero devuelve sales_share=null, no división por cero ni valor inventado.
- [x] Añadir tests de regla de aceptación: ganancia agregada con pérdidas en mayoría de períodos no recomienda modelo; empate conserva baseline; modelo ganador en development que pierde en holdout no se recomienda. No usar target de holdout para escoger otro modelo.
- [x] Implementar métricas por período y misma población para todos los métodos. Revisar estabilidad, concentración y cancelaciones de seleccionados como diagnósticos separados del target.
- [x] Congelar selección desde development según contrato y ejecutar `python analysis/run_retail.py holdout --root .` una vez como evaluación final. Guardar configuración, tiempo, resultados y cualquier fallo; una repetición técnica debe demostrar mismo artefacto/cálculo, no redefinir la estrategia.
- [x] Comparar con baseline y documentar límites: ventanas solapadas en entrenamiento, pocos períodos efectivos, disponibilidad histórica asumida, horizonte finito, población identificable y falta de efecto de contacto.
- [x] No generar intervalos de confianza si no hay suficientes períodos/clientes para una interpretación útil. Si se incluyen, usar bootstrap por cliente con todos sus períodos, seed del contrato y explicar que no estima generalización entre mercados o épocas.
- [x] Ejecutar tests GREEN, checks temporales y los cinco gates seleccionados de Validation. Paquete presentado; aprobaciones humanas pendientes antes de Delivery. No contar el check estructural como revisión metodológica.

### Tarea 6: Recomendación y entrega

**Files:** `decision/recommendation.md`, `delivery/decision_memo.md`, `delivery/analytical_report.md`, `delivery/delivery_contract.md`, `evidence/claims.yaml`, `reports/delivery/verification.json`.

**Interfaces:** claims con ID, texto, tipo (`observed`, `assumption`, `proposal`, `limitation`), fuente relativa y campo de resultado cuando aplique. Los documentos consumen outputs congelados, no recalculan cifras manualmente.

- [x] Preparar recomendación coherente con acceptance_decision: baseline, modelo o evidencia insuficiente. La lista es ilustrativa de un cutoff histórico, no una campaña para ejecutar hoy.
- [x] Explicar exclusiones, target de ventas positivas y efecto de cancelaciones; distinguir ventas observadas del Top-K de ventas inducidas por una acción. No llamar óptima a la política de contacto ni atribuir margen/ROI.
- [x] Crear matriz de claims y comprobar todas las cifras contra JSON/CSV, denominadores/poblaciones y períodos. Añadir verificaciones de vocabulario y revisión semántica para detectar frases de uplift, profit, CLV completo o cliente real sin sustento.
- [x] Entregar memo ejecutivo y reporte técnico en español, sin deck o dashboard adicionales. Revisar consistencia entre ranking, narrativa y métricas.
- [x] Presentar Delivery con criterio de aceptación y limitar cualquier recomendación a una futura prueba comercial con diseño causal. Gate Delivery preparado, aprobación humana pendiente antes de Handoff.

### Tarea 7: Handoff, reproducción y feedback

**Files:** `handoff/runbook.md`, `handoff/business_handoff.md`, `handoff/technical_handoff.md`, `handoff/capability_feedback.md`, `handoff/next_steps.md`, `handoff/handoff-manifest.json`, `reports/handoff/reproduction.json`.

**Interfaces:** manifiesto de outputs congelados con paths relativos, bytes y SHA256; excluir estado/vistas mutables. Runbook describe instalación desde lock, fuente y contratos, comandos development/holdout y restricciones.

- [x] Ejecutar suite del piloto y verificar manifiestos de fuentes, snapshots y resultados; conservar logs y códigos. No presentar esta ejecución local como nueva cobertura Windows del análisis.
- [x] Copiar proyecto a carpeta temporal, excluir entorno virtual, reconstruir entorno desde lock y reproducir pipeline con fuente congelada. Comparar filas, IDs y selecciones exactamente, y scores/métricas con rtol=1e-8 y atol=1e-6; timestamps/logs no requieren igualdad byte a byte. Verificar que no depende de Foundry ni rutas absolutas del dispositivo.
- [x] Registrar feedback por capacidad: tarea, versión, output, utilidad/fallo, expected verificable, fuentes y límites. Contrastar gaps con candidates actuales, sin crear o promover fichas automáticamente.
- [x] Presentar handoff y reproducción a David. David aprobó Handoff; todos los gates PASS y estado COMPLETED verificados en closure-verification.json.
- [x] Preparar status final: decisión recomendada, resultados, limitaciones, coste API US$0, capacidades usadas/gaps y siguiente caso real o evaluación concreta. Conservar pilotos anteriores intactos.

## Ejecución y puntos de pausa

Mantener ejecución nativa en la sesión principal, siguiendo la preferencia previa de David y evitando contextos de agentes adicionales. La aprobación de este plan permite ejecutar la tarea 1 hasta su paquete Discovery. Las tareas posteriores dependen de sus revisiones y contratos, sin volver a pedir permisos para lecturas, cálculos o fixes rutinarios ya incluidos.

No lanzar modelos antes de cerrar Framing/Diagnosis. No aprobar gates futuros al aprobar este plan. Si la auditoría invalida el caso, reportar evidencia y proponer el cambio más pequeño que preserve el objetivo.

## Revisión del plan

Cobertura revisada contra el diseño: fuente/licencia (1), encargo/contratos (2), temporalidad/target (3), baselines/modelos (4), evaluación/aceptación (5), entrega/claims (6), portabilidad/Foundry (7). Los cinco riesgos del Review Focus tienen checks en sus tareas. No se escribieron scripts, no se descargó el dataset, no se instalaron dependencias ni se ejecutaron pruebas en esta fase.
