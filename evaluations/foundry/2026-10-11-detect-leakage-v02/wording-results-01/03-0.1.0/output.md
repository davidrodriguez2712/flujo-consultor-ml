```markdown
---
skill: detect-leakage
version: 0.1.0
fecha: 2026-10-11
estado: auditoría parcial; sin hallazgos confirmados de leakage
condicion: rehearsal
decision_id: RET-01
inputs: expediente incrustado
---

## Resumen
Expediente insuficiente para concluir leakage. Solo consta `usage_previous_30d`, ventana previa, disponible 2025-10-31T23:00Z, frente a scoring 2025-11-01T08:00Z. Sin split, fit ni código.

## Hallazgos
- **Temporal (Riesgo, medio):** la disponibilidad (23:00Z del 31) es anterior al scoring (08:00Z del 1). Según lo declarado, no hay leakage temporal, pero la ventana exacta no consta.
- **Pipeline/validación (No determinable, alto):** sin split, fit ni código no puede verificarse contaminación train-test ni preprocessing leakage.

## Evidencia
Única evidencia: metadatos temporales de una feature. No se ejecutaron checks deterministas (sin datos ni código).

## Preguntas abiertas
¿La ventana de `usage_previous_30d` termina antes de 2025-10-31T23:00Z, y el split y los fit de preprocessing se hicieron solo con datos previos al corte de scoring?

## Recomendaciones
Aportar código del pipeline, split y ventana de agregación; verificar que ningún dato posterior al corte entre en la feature.

## Límites
No garantiza ausencia de leakage. No evalúa otras features, joins ni la semántica de negocio. Requiere validación de un experto del dominio.
```