---
skill: detect-leakage
version: 0.2.2
fecha: 2026-10-13
inputs:
  - path: case.md
    sha256: db7f2572bc7e591a8d537735dade9cdbcc1da74a100ecb2dd245673b3540e951
  - path: inputs/context.md
    sha256: ae79d0d67bdd4f71349d51644732c99ae1ce547ad618a6d663a30195042b1c7e
  - path: inputs/dictionary.json
    sha256: 72636cf89cf406c70e90c0c1325ddcb7c89229a915199153c35c9f167c414fe3
  - path: inputs/observations.csv
    sha256: 32ae7c42472e440093583da2798aba677eb2ceae58289e5d5dc77f3e46354532
estado: auditoría en modo lectura completada; resultado No determinable; no aprueba gates
condicion: treatment
---

## Resumen
Resultado: **No determinable**. La feature `complaint_count` no puede clasificarse como leakage confirmado ni como temporalmente válida con el expediente disponible. Falta la ventana de conteo, la fecha de disponibilidad efectiva y el código de construcción. La exportación del 2025-08-01 no demuestra disponibilidad al scoring del 2025-06-01. Acción provisional: exigir evidencia antes de usar la feature; el uso queda reservado a la autoridad del owner.

## Hallazgos
1. **Componente:** `complaint_count` (feature). **Brecha:** ventana de conteo y disponibilidad no documentadas (`dictionary.json`; `context.md`). **Mecanismo:** no determinable; el conteo podría reflejar el estado al exportar, que incluiría reclamos posteriores al scoring. **Fuente:** `context.md`, línea 3. **Confianza en la brecha:** alta. **Confianza en leakage:** baja, sin evidencia de mecanismo. **Severidad:** no estimable, sin evidencia de impacto. **Acción:** obtener la definición de ventana, fecha de cada reclamo y snapshot verificable al 2025-06-01.
2. **Componente:** metadatos de disponibilidad. **Brecha:** `feature_available_at` y `construction_code` son `null`. **Fuente:** `dictionary.json`. **Confianza:** alta. **Severidad:** no estimable. **Acción:** documentar linaje antes de cualquier uso.
3. **Componente:** target `cancelled_next_30d`. **Hecho:** los outcomes son posteriores al scoring y sirven como etiqueta retrospectiva legítima; no son features. **Fuente:** `context.md`; `observations.csv`. **Acción:** excluirlos de las features.

Condiciones (ver Recomendaciones): ninguna se cumple.

## Evidencia
- Ejecutado: `check_inputs.py` (hashes, tamaños, columnas y conteo de filas: 3 filas, 5 columnas). Solo verifica integridad; no evalúa leakage.
- Leído: `case.md`, `workflow.md`, `report-context.json`, `inputs/context.md`, `inputs/dictionary.json`, `inputs/observations.csv`.
- Observado en `observations.csv`: `prediction_at` = 2025-06-01T00:00:00Z en las 3 filas; `exported_at` = 2025-08-01T00:00:00Z; `complaint_count` = 3, 0, 2; target = 1, 0, 0. Con 3 filas no hay inferencia estadística.
- Skill `detect-leakage` cargada (versión 0.2.2), según `report-context.json`.
- No ejecutado: `pipeline.py`, entrenamiento, evaluación, consultas de red ni verificación de runtime de producción.
- Límites: datos sintéticos; sin código, sin historial, sin split ni preprocessing documentados.

## Preguntas abiertas
1. ¿Cuál es la ventana exacta de `complaint_count` (p. ej., 30/90 días antes de `prediction_at`)?
2. ¿Cuál es la fecha de disponibilidad efectiva del conteo en producción?
3. ¿El conteo se calcula desde un snapshot al 2025-06-01 o desde una extracción posterior?
4. ¿Existe código de construcción y linaje verificable?
5. ¿Hay timestamps por reclamo que permitan reconstruir el conteo a una fecha de corte?

## Recomendaciones
**Condición de confirmación (no cumplida):** demostrar que se usó información posterior de forma ilegítima, o que la disponibilidad efectiva posterior se usó como disponible al scoring. La exportación no la satisface.

**Condición de posible validez temporal (no cumplida):** ventana previa documentada y disponibilidad efectiva al scoring, con linaje aplicable. Esto no certifica otras familias (joins, preprocessing, CV).

**Acción provisional:** no usar `complaint_count` en modelado o scoring hasta contar con evidencia de ventana, disponibilidad y linaje; el uso queda bajo autoridad del owner. Si se requiere una alternativa histórica, usar un snapshot con corte verificable al 2025-06-01, nunca el valor futuro. Revisión humana de proceso obligatoria antes de producción.
