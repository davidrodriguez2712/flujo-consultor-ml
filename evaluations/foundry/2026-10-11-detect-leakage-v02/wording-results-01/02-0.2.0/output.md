```markdown
---
skill: detect-leakage
version: 0.2.0
fecha: 2026-10-11
estado: auditoría parcial; sin split/fit/código verificado
condicion: rehearsal
decision_id: RET-01
inputs: expediente incrustado
---

# Resumen
Feature usage_previous_30d disponible 2025-10-31T23:00Z; scoring 2025-11-01T08:00Z. Disponibilidad aparente válida; construcción no verificada.

# Hallazgos
- Riesgo: ventana de cálculo de usage_previous_30d no confirmada. Mecanismo posible: incluir actividad posterior a 23:00Z. Fuente: expediente. Confianza: baja. Severidad: media. Acción: verificar cutoff de agregación.

# Evidencia
- Timestamp de disponibilidad y de scoring declarados en el encargo.
- Sin código de construcción, split ni fit en el expediente.

# Preguntas abiertas
¿Cuál es el cutoff exacto de la agregación que produce usage_previous_30d y se ejecuta con datos solo hasta 2025-10-31T23:00Z?

# Recomendaciones
- Confirmar con el proceso de construcción el cutoff y la ventana.
- Revisar split y fit cuando estén disponibles.
- Límites: no demuestra ausencia universal de leakage ni generalización; revisión humana sigue necesaria.
```