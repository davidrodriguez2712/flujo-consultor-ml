```markdown
---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-11
estado: parcial, sin verificación de split/fit/código
condicion: rehearsal
decision_id: RET-01
inputs: expediente incrustado
---

# Resumen
Auditoría limitada del expediente. `usage_previous_30d` (ventana previa, disponible 2025-10-31T23:00Z) parece anterior al scoring de 2025-11-01T08:00Z. No hay split, fit ni código para confirmar. No hay seguridad universal.

# Hallazgos
- Riesgo (no determinable): ventana y disponibilidad declaradas son coherentes, pero no verificadas por proceso.
- Riesgo: sin código, no se puede comprobar si el target o eventos posteriores entran en la construcción.

# Evidencia
- Scoring: 2025-11-01T08:00Z. Disponibilidad: 2025-10-31T23:00Z. Ventana: 30 días previos.
- Sin split, fit ni código en el expediente.

# Preguntas abiertas
¿Qué código de construcción y fecha de corte exacta de `usage_previous_30d` confirma que no usa datos posteriores a 2025-10-31T23:00Z?

# Recomendaciones
- Verificar el pipeline de construcción y el corte temporal antes de usar la feature.
- Revisar split y orden fit/transform cuando estén disponibles.

# Límites
No demuestra generalización ni ausencia universal de leakage. Revisión humana de proceso requerida.
```