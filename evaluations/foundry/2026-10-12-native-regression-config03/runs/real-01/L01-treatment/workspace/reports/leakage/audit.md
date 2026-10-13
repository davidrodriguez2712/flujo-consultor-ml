---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-12
inputs:
  - path: case.md
    sha256: 89f1c1a622a64a73dafb5b641d871d372e72a1076533a23378ec2446f11e1e14
  - path: inputs/context.md
    sha256: 3e3db7db6249d33479a7e01fdcaee3f8f8fec3f898f7c863e2d252398e613552
  - path: inputs/observations.csv
    sha256: 29e4badcbbcbf9e242bde9f2d31b80d1f55091a52d094b658e6992a457ad0f19
  - path: inputs/pipeline.py
    sha256: fb122bed11f58973887818405e1b992b1589a72f8faf0ea13daf98ddb2f3da63
estado: auditoría completada sobre expediente; hallazgo material confirmado; sin aprobación de gates
condicion: treatment
---

## Resumen
La feature `recovered_kwh` introduce información no disponible al scoring: su `recovered_available_at` (2025-06-09 a 2025-06-12) es posterior a `prediction_at` (2025-06-01T00:00:00Z) y el contexto indica que se determina al procesar la inspección. `history_kwh_90d` es válida: disponible 2025-05-31T23:00:00Z, antes del scoring. Se recomienda retirar `recovered_kwh` del scoring.

## Hallazgos
1. **Confirmado — severidad alta.** Componente: `pipeline.py`, `FEATURE_COLUMNS`. Mecanismo: feature posterior al scoring (disponibilidad posterior al corte). Fuente: `observations.csv` filas S01–S04 (`recovered_available_at` > `prediction_at`); `context.md` (se determina al procesar la inspección). Confianza: alta. Acción: excluir `recovered_kwh` de features de scoring; no usarla para entrenar ni evaluar como predictor.
2. **No hallazgo — `history_kwh_90d`.** Disponible antes del corte (`history_available_at` 2025-05-31T23:00:00Z). Conservar.
3. **Indicio, no prueba.** En las 4 filas, `recovered_kwh > 0` coincide con `fraud_confirmed = 1`. Muestra de 4 filas: no permite inferencia estadística; la confirmación del mecanismo se basa en disponibilidad temporal, no en esta coincidencia.

## Evidencia
- Lectura de `case.md`, `inputs/context.md`, `inputs/pipeline.py`, `inputs/observations.csv`.
- Ejecución de la utility autorizada `check_inputs.py`: hashes, tamaños y conteo (4 filas, 7 columnas) confirmados.
- Comparación manual de timestamps por fila (ejecutada sobre el CSV leído, no por script adicional).
- Skill `acos-eval:detect-leakage` cargada (versión 0.2.0).
- No ejecutados: `pipeline.py`, entrenamiento, split, cross-validation, métricas (fuera de mandato o ausentes).

## Preguntas abiertas
- No hay código de split, fit de transformaciones ni cross-validation; esas familias no son auditables con este expediente.
- Confirmar en producción que el scoring real no consume `recovered_kwh` de forma distinta a la documentada.
- Dado que el expediente es sintético, la extensión a datos reales requiere revisión humana de proceso.
- Limitación: no se verificó si existía un reporte previo en la ruta; el Write no fue precedido por lectura de esa ruta.

## Recomendaciones
- Retirar `recovered_kwh` de `FEATURE_COLUMNS` para el scoring.
- Mantener `history_kwh_90d` con su corte actual.
- Si se requiere evaluar la señal de recuperación, reconstruirla solo con fuente y corte verificables anteriores a `prediction_at`.
- Revisión humana del proceso antes de cualquier uso productivo; esta auditoría no certifica ausencia universal de leakage.
