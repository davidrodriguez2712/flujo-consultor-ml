---
id: N02
skill: detect-leakage
created: 2026-10-11
domain: suscripciones
difficulty: inicial
source: sintético, ACOS
---

# Contexto

Encargo de auditoría de datos y preparación de un backtest.

# Objetivo

Determinar si el expediente sustenta un uso válido de información en la decisión declarada.

# Tarea

Audita el expediente y fundamenta hallazgos y límites; no calcular performance.

# Inputs

inputs/context.md, inputs/observations.csv e inputs/pipeline.py.

# Restricciones

Expediente sintético. Leer solo archivos autorizados por la whitelist del runner: case.md, inputs, workflow común, utility fija, report-context.json y snapshot/metadata de la skill instalada. El runner genera report-context y utility antes de iniciar; no son fuentes de resultados esperados. Solo utility fija permitida para hashes/conteos; inspeccionar código, no ejecutarlo ni entrenar. Sin red, installs, cambios a inputs ni gates. Reporte nuevo reports/leakage/audit.md, máximo700palabras (conteo whitespace del archivo completo, frontmatter incluido); resumen final≤80palabras (conteo whitespace) y ruta. Expected privado no disponible.

# Criterio de finalización

Frontmatter: skill, version, fecha real, inputs con hashes reales, estado y condicion (valor de .runtime/report-context.json). Baseline: skill none y version null; treatment: skill detect-leakage y version del snapshot. La fecha es la real de ejecución. Body: Resumen, Hallazgos, Evidencia, Preguntas abiertas, Recomendaciones. Cada hallazgo material incluye componente, mecanismo, fuente, confianza, severidad y acción proporcional. No inventar checks ni fechas; la utility no evalúa leakage. La forma correcta no prueba contenido.
