---
skill: detect-leakage
skill_version: 0.2.0
skill_sha256: c2a2440477d9985489b71f4d8c50380ccd7985635d02eab330cfee0f7e5856c4
condicion: treatment
caso: L01
fecha: 2026-10-11
estado: completado (auditoría de expediente; sin ejecución de pipeline)
inputs:
  - case.md sha256 89f1c1a622a64a73dafb5b641d871d372e72a1076533a23378ec2446f11e1e14
  - inputs/context.md sha256 3e3db7db6249d33479a7e01fdcaee3f8f8fec3f898f7c863e2d252398e613552
  - inputs/observations.csv sha256 29e4badcbbcbf9e242bde9f2d31b80d1f55091a52d094b658e6992a457ad0f19 (4 filas)
  - inputs/pipeline.py sha256 fb122bed11f58973887818405e1b992b1589a72f8faf0ea13daf98ddb2f3da63
---

# Resumen

La feature `recovered_kwh` introduce información no disponible al scoring (2025-06-01T00:00:00Z): su disponibilidad declarada es 2025-06-09 a 2025-06-12, y el pipeline la incluye en `FEATURE_COLUMNS`. Hallazgo confirmado por contraste de timestamps y código. `history_kwh_90d` es válida: disponible 2025-05-31T23:00:00Z, antes del corte. No se audita split, fit ni métricas por ausencia en el expediente.

# Hallazgos

**H1 — Leakage temporal por feature posterior al scoring (Confirmado)**
- Componente: `inputs/pipeline.py`, línea 2 (`FEATURE_COLUMNS`) y línea 4 (`build_features`).
- Mecanismo: `recovered_kwh` se determina al procesar la inspección; `context.md` indica que no existe para el sistema antes de `recovered_available_at`, y que un cero posterior tampoco era conocido al scoring.
- Fuente: `inputs/observations.csv` columna `recovered_available_at` (2025-06-09T12:00Z, 06-10, 06-11, 06-12), todas posteriores a `prediction_at` 2025-06-01T00:00Z.
- Confianza: alta (timestamps y código en el expediente).
- Severidad: alta.
- Acción propuesta: retirar `recovered_kwh` del conjunto de features de scoring. Reconstruir solo si hay fuente con corte histórico verificable (valor disponible a 2025-06-01). No rellenar con supuestos.

**H2 — Indicio de señal perfecta sobre el target (Riesgo; no concluyente)**
- En las 4 filas, `recovered_kwh > 0` coincide con `fraud_confirmed = 1` (S01, S03) y `recovered_kwh = 0` con `fraud_confirmed = 0` (S02, S04).
- Esto es solo un indicio: n=4, sin construcción verificada de la relación. Ausencia de igualdad no descarta leakage; la presencia tampoco lo prueba por sí sola. Refuerza H1 como mecanismo a retirar.
- Acción: no usar como evidencia de desempeño; verificar con datos completos y proceso de construcción.

**H3 — Historia de consumo (No se detecta mecanismo de leakage)**
- `history_kwh_90d` disponible desde 2025-05-31T23:00Z, anterior al scoring. Válida según el expediente.
- Entidades: los supply_id son únicos en las 4 filas; no se evaluó recurrencia.

# Evidencia

- `case.md`, `inputs/context.md`: definiciones de scoring, target a 14 días, disponibilidad de ambas features, alcance (split, fit y métricas ausentes).
- `inputs/pipeline.py`: `FEATURE_COLUMNS = ["history_kwh_90d", "recovered_kwh"]`; `build_features` selecciona ambas sin filtrar por disponibilidad.
- `inputs/observations.csv`: 4 filas, 7 columnas; timestamps como arriba.
- Utilidad `check_inputs.py` ejecutada una vez: devolvió hashes, tamaños y conteos (4 filas, columnas coincidentes). No ejecuta pipeline ni evalúa leakage.

# Preguntas abiertas

- ¿Cómo se construye `recovered_kwh` en el sistema productivo y existe un snapshot a la fecha de scoring?
- ¿Existe split temporal y fit de transformaciones? No está en el expediente.
- ¿El scoring real es sobre la misma población y fecha que el expediente?

# Recomendaciones

1. Excluir `recovered_kwh` de las features de scoring (H1).
2. Mantener `history_kwh_90d` con verificación de la fuente de corte.
3. Verificar en proceso (no solo en este expediente) disponibilidad de todas las features y el split/fit antes de cualquier evaluación.

# Límites

Auditoría basada solo en el expediente autorizado: 4 filas sintéticas, código fragmentario sin ejecución. No demuestra generalización ni ausencia de leakage en otras partes. Requiere revisión humana del proceso de construcción. No se ejecutaron checks de split, fit ni métricas porque no existen en el expediente.
