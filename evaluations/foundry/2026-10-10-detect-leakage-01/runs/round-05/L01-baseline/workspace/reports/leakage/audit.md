---
fecha: 2026-10-11
caso: L01
skill: none
skill_version: null
estado: borrador para revisión humana
condicion: baseline (sin skill cargada)
inputs:
  - path: case.md
    sha256: 89f1c1a622a64a73dafb5b641d871d372e72a1076533a23378ec2446f11e1e14
    bytes: 1728
  - path: inputs/context.md
    sha256: 3e3db7db6249d33479a7e01fdcaee3f8f8fec3f898f7c863e2d252398e613552
    bytes: 776
  - path: inputs/observations.csv
    sha256: 29e4badcbbcbf9e242bde9f2d31b80d1f55091a52d094b658e6992a457ad0f19
    bytes: 417
    filas: 4
  - path: inputs/pipeline.py
    sha256: fb122bed11f58973887818405e1b992b1589a72f8faf0ea13daf98ddb2f3da63
    bytes: 204
---

# Auditoría de leakage — L01

## Resumen

El conjunto declarado de features (`history_kwh_90d`, `recovered_kwh`) contiene un mecanismo de leakage verificable: `recovered_kwh` solo existe para el sistema después de `recovered_available_at` (2025-06-09 a 2025-06-12), es decir, 8 a 11 días después del scoring (2025-06-01T00:00:00Z). Debe excluirse de las features de predicción. `history_kwh_90d` es temporalmente consistente en las 4 filas (disponible 2025-05-31T23:00:00Z, antes del scoring), aunque con evidencia limitada. `pipeline.py` no aplica ningún corte temporal, de modo que la protección depende de que los datos de entrada ya estén filtrados.

## Hallazgos

**H1 — Leakage por feature futura (`recovered_kwh`)**
- Componente: `inputs/pipeline.py`, `FEATURE_COLUMNS`; `inputs/observations.csv`, columna `recovered_kwh` y `recovered_available_at`.
- Mecanismo: el valor se determina al procesar la inspección y está disponible después del scoring. El cero posterior tampoco era conocido al scoring (`context.md`).
- Fuente: `inputs/context.md`; filas S01–S04 de `observations.csv` (`recovered_available_at` = 06-09, 06-10, 06-11, 06-12 frente a `prediction_at` = 06-01).
- Confianza: alta (la diferencia temporal es directa en los datos y en el contexto).
- Severidad: alta.
- Acción propuesta: retirar `recovered_kwh` de `FEATURE_COLUMNS`. Solo podría reconsiderarse si se define una versión con corte `recovered_available_at <= prediction_at`, lo que requiere decisión del owner.

**H2 — Ausencia de corte temporal en el proceso de features**
- Componente: `inputs/pipeline.py`, `build_features`.
- Mecanismo: `build_features` solo selecciona columnas por nombre; no compara `*_available_at` con `prediction_at` ni descarta valores posteriores. Cualquier columna añadida a la lista se incorporaría sin control.
- Fuente: `inputs/pipeline.py` líneas 2–4.
- Confianza: alta para lo que el fragmento hace; el resto del pipeline no está en el expediente.
- Severidad: media.
- Acción propuesta: añadir una validación explícita de `available_at <= prediction_at` por feature antes de construir el vector.

**H3 — `history_kwh_90d` consistente en temporalidad (sin hallazgo de leakage)**
- Fuente: `context.md` (uso de días anteriores al scoring); `observations.csv`, `history_available_at` = 2025-05-31T23:00:00Z en las 4 filas.
- Confianza: media. Solo se verificaron timestamps declarados en 4 filas sintéticas; no se auditó cómo se calcula la columna upstream.
- Severidad: no aplica.
- Acción propuesta: confirmar con el owner de datos la lógica de la ventana de 90 días.

## Evidencia

- Verificación determinista (utilidad `.runtime/check_inputs.py`, único comando ejecutado): hashes y tamaños de los cuatro inputs listados arriba; `observations.csv` con 4 filas y las 7 columnas esperadas.
- Lectura directa de `case.md`, `workflow.md`, `inputs/context.md`, `inputs/pipeline.py`, `inputs/observations.csv`.
- Comparación temporal: `prediction_at` (2025-06-01T00:00:00Z) frente a `history_available_at` y `recovered_available_at` en cada fila. Es una comparación manual de timestamps, no un cálculo de métricas.

## Límites de inspección

- No se ejecutó `pipeline.py`, no se entrenó, no se calcularon métricas de performance ni se evaluó la relación entre features y `fraud_confirmed`; según el encargo, esas partes están fuera de alcance.
- Datos sintéticos de 4 filas: las conclusiones son sobre el mecanismo declarado, no sobre distribuciones.
- No hay split, fit de transformaciones ni código de entrenamiento en el expediente; no se concluye sobre esas partes.
- Skill: no se invocó `acos-eval:detect-leakage` porque no figura entre las skills disponibles. Por eso `skill: none`. La auditoría es manual y basada en lectura de código y timestamps.
- Fuente/expected del reviewer no forman parte del expediente y no se usaron.

## Preguntas abiertas

1. ¿Qué owner acepta la definición de la feature `recovered_kwh` y puede confirmar que no se usará en ninguna versión sin corte temporal?
2. ¿Cómo se genera `history_kwh_90d` en el sistema origen y se garantiza el corte de 2025-05-31T23:00:00Z?
3. ¿Existe en otro código (fuera del expediente) un filtro temporal aplicado antes de `build_features`?

## Recomendaciones

1. Excluir `recovered_kwh` de las features de predicción (H1). Prioridad alta.
2. Introducir una validación temporal explícita por feature en `build_features` (H2).
3. Mantener `history_kwh_90d` pendiente de confirmación del owner de datos (H3).
4. Antes de cualquier evaluación de performance, re-auditar con el pipeline completo; esta auditoría no lo cubre.
