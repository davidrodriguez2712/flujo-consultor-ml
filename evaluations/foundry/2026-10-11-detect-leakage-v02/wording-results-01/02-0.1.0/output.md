```markdown
---
skill: detect-leakage
version: 0.1.0
fecha: 2026-10-11
estado: auditoría parcial; sin hallazgos confirmados; sin split, fit ni código disponibles
condicion: rehearsal
decision_id: RET-01
inputs: expediente incrustado
---

## Resumen
No hay evidencia de leakage confirmada. Falta el pipeline real, por lo que no se puede auditar el split ni las transformaciones. La variable usage_previous_30d es, en principio, compatible con el scoring, con una ventana previa y disponibilidad 2025-10-31T23:00Z, anterior al scoring 2025-11-01T08:00Z.

## Hallazgos
- **Informativo:** usage_previous_30d tiene ventana previa y disponibilidad anterior al prediction timestamp. Confianza: Probable (no es leakage temporal por lo declarado).
- **Riesgo (medio):** sin código de agregación no se verifica que la ventana use solo datos anteriores a 2025-10-31T23:00Z. Confianza: Riesgo.

## Evidencia
Timestamps declarados: disponibilidad 2025-10-31T23:00Z < scoring 2025-11-01T08:00Z. No se ejecutaron checks de solape de entidades, orden de fit/split ni cardinalidad de joins: no hay artefactos.

## Preguntas abiertas
¿Qué tablas y consulta generan usage_previous_30d, y se fija su fecha de corte antes de 2025-11-01T08:00Z?

## Recomendaciones
Obtener el código de agregación y el esquema de split antes de validar. No confiar en métricas hasta cerrar la auditoría del pipeline.

**Límites:** auditoría parcial sobre expediente incrustado; no garantiza ausencia de leakage, ni sustituye validación de negocio.
```