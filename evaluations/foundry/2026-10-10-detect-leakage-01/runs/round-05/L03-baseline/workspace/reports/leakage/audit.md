---
fecha: 2026-10-11
caso: L03
skill: none
skill_version: null
inputs:
  - path: case.md
    sha256: db7f2572bc7e591a8d537735dade9cdbcc1da74a100ecb2dd245673b3540e951
    bytes: 1711
  - path: inputs/context.md
    sha256: ae79d0d67bdd4f71349d51644732c99ae1ce547ad618a6d663a30195042b1c7e
    bytes: 644
  - path: inputs/dictionary.json
    sha256: 72636cf89cf406c70e90c0c1325ddcb7c89229a915199153c35c9f167c414fe3
    bytes: 150
  - path: inputs/observations.csv
    sha256: 32ae7c42472e440093583da2798aba677eb2ceae58289e5d5dc77f3e46354532
    bytes: 223
    filas: 3
estado: cerrado con bloqueo; no aprobado
condicion: baseline
---

# Resumen

La feature `complaint_count` no puede considerarse disponible en el momento de predicción (2025-06-01T00:00:00Z) con la evidencia del expediente. Su ventana, fecha de disponibilidad y código de construcción no están documentados, y el expediente indica que el conteo podría reflejar el estado al momento de la exportación (2025-08-01T00:00:00Z), posterior al scoring y a la ventana de outcome. El riesgo de leakage es material. No se verificó con datos suficientes ni con código; la conclusión es de auditoría documental. Recomendación: no usar `complaint_count` como feature predictiva hasta que un owner confirme su disponibilidad.

# Hallazgos

**H1. Disponibilidad temporal no documentada (leakage potencial, no demostrado).**
- Componente: feature `complaint_count`.
- Mecanismo: el conteo podría incluir reclamos ocurridos entre 2025-06-01 y 2025-08-01, es decir, después del scoring y dentro o alrededor de la ventana de cancelación de 30 días.
- Fuente: `inputs/context.md` (“No se conoce si el conteo refleja el estado al scoring o al exportar”; “no hay … fecha de disponibilidad, ventana de conteo … ni construction code”); `inputs/dictionary.json` (`feature_available_at: null`, `construction_code: null`).
- Confianza: alta en que la evidencia es insuficiente; media en que haya leakage real (inferencia).
- Severidad: alta (bloquea aceptación de la feature).
- Acción propuesta: excluir la feature del set predictivo provisionalmente; solicitar al owner la definición de ventana y el timestamp de snapshot.

**H2. Riesgo de post-outcome contamination.**
- Componente: exportación retrospectiva (`exported_at` = 2025-08-01) con `cancelled_next_30d`.
- Mecanismo: si el conteo se calculó al exportar, los reclamos asociados a una cancelación ya ocurrida pueden entrar como predictor. El expediente no permite distinguirlo.
- Fuente: `inputs/observations.csv` (columnas `exported_at`, `complaint_count`, `cancelled_next_30d`); `inputs/context.md` (“contiene outcomes conocidos después del scoring”).
- Confianza: media (inferencia desde la estructura de la exportación).
- Severidad: alta.
- Acción propuesta: reconstruir la feature como snapshot con filtro `timestamp <= prediction_at` y verificar contra la fuente original, sin usar la exportación como prueba de disponibilidad.

**H3. Muestra insuficiente para cualquier evaluación empírica.**
- Componente: `inputs/observations.csv`.
- Hecho observado: 3 filas (check_inputs: `rows: 3`). Solo U01 tiene `cancelled_next_30d=1` y `complaint_count=3`.
- Confianza: alta. Severidad: media (no permite medir ni descartar leakage).
- Acción: no extraer conclusiones de correlación; requerir muestra mayor si se evalúa.

**H4. Metadata correctamente separada.**
- `customer_id`, `prediction_at`, `exported_at` y `cancelled_next_30d` se tratan como metadata/target, según `context.md`. Confianza alta. Severidad baja.

# Evidencia

- Verificación determinista (utilidad autorizada, sin pipeline): los 4 archivos listados arriba con sha256, bytes y conteo de filas; columnas de CSV coinciden con las esperadas.
- Lectura directa de `case.md`, `workflow.md`, `inputs/context.md`, `inputs/dictionary.json`, `inputs/observations.csv`.
- No se ejecutó `pipeline.py`, no se entrenó modelo, no se calcularon métricas, no se consultó red.

# Límites

- Skill `acos-eval:detect-leakage` no estaba instalada en el entorno (solo `plugin-authoring` disponible); no fue invocada. `skill: none`.
- Sin código de construcción, sin versión histórica ni split/preprocessing; sin expected del reviewer (fuera del expediente).
- Datos sintéticos de 3 filas: no sustentan métricas ni inferencia estadística.
- Los hallazgos H1–H2 son inferencias documentales, no hechos validados.

# Preguntas abiertas

1. ¿Qué ventana cubre `complaint_count` (p. ej., últimos N días antes de `prediction_at`)?
2. ¿El conteo es snapshot al scoring o estado al exportar?
3. ¿Existe fecha de disponibilidad o log histórico de reclamos con timestamp de ingreso?
4. ¿Se registran reclamos posteriores a la cancelación que podrían contaminar el conteo?
5. ¿Quién es el owner que acepta la definición de la feature?

Qué cambiaría la conclusión: evidencia de que el conteo se construye con timestamps `<= prediction_at` (H1 pasaría a riesgo bajo, sujeto a verificación con código y datos reales), o un snapshot histórico que confirme el valor disponible en 2025-06-01.

# Recomendaciones

1. Mantener `complaint_count` fuera del set predictivo hasta confirmar disponibilidad (owner pendiente).
2. Solicitar `construction_code` y timestamp de snapshot; completar `feature_available_at` en `dictionary.json` solo con evidencia.
3. Re-auditar con muestra mayor y reconstrucción as-of antes de cualquier decisión de negocio.
4. Esta auditoría no aprueba la feature ni el caso; la decisión corresponde a un humano responsable.
