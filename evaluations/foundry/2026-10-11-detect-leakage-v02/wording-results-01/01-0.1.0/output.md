```markdown
---
skill: detect-leakage
version: 0.1.0
fecha: 2026-10-11
estado: auditoría parcial; sin hallazgos confirmados; leakage no determinable
condicion: rehearsal
decision_id: RET-01
inputs: expediente incrustado
---

## Resumen
Expediente insuficiente para concluir leakage. Scoring 2025-11-01T08:00Z; la feature usage_previous_30d tiene disponibilidad 2025-10-31T23:00Z, anterior al scoring, y su ventana es previa. Riesgo no determinable: falta split, fit y código.

## Hallazgos
- **Bajo (Probable ausencia de leakage temporal para usage_previous_30d):** ventana previa y disponibilidad anterior al scoring. Confianza: Probable.
- **Medio (Riesgo no determinable):** no se puede verificar que la ventana no incluya datos posteriores al corte de disponibilidad ni que el target no haya contaminado la feature. Confianza: No determinable.

## Evidencia
Timestamps declarados en el expediente: disponibilidad 2025-10-31T23:00Z; scoring 2025-11-01T08:00Z. No hay checks deterministas ejecutables (sin split, fit ni código).

## Preguntas abiertas
¿Cómo se construyó usage_previous_30d (código o consulta) y se verificó que su ventana termina antes de 2025-10-31T23:00Z?

## Recomendaciones
Obtener el código de construcción y el esquema de split; verificar la ventana y el orden de fit antes de confiar en métricas. No atribuir seguridad universal a la feature.

## Límites
Auditoría limitada al expediente incrustado; sin entrenamiento, sin acceso a datos ni validación de negocio. Un experto del dominio debe confirmar la semántica de la variable.
```