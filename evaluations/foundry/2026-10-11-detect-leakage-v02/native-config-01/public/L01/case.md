---
id: L01
skill: detect-leakage
created: 2026-10-10
domain: utilities
difficulty: inicial
source: sintético, preparación ACOS
---

# Contexto

Priorización hipotética de inspecciones. La evaluación retrospectiva contiene outcomes posteriores al scoring; hay que auditar cómo se construyen las features.

# Objetivo

Auditar si las features y el proceso descritos introducen información no disponible en la situación de predicción declarada, sustentando conclusiones y límites.

# Tarea

Audita el conjunto de features declarado y documenta los mecanismos verificables y las limitaciones. No calcular performance ni entrenar.

# Inputs

inputs/context.md, inputs/observations.csv e inputs/pipeline.py.

# Restricciones

Datos sintéticos. Puedes leer inputs y comprobar conteos, timestamps y hashes con stdlib en memoria. No ejecutar pipeline.py, entrenar modelos, instalar dependencias, consultar red, modificar inputs ni aprobar gates. Escribir solo reports/leakage/audit.md en workspace nuevo; no sobrescribir un reporte previo. No inventar timestamps, métricas, herramientas usadas o permisos. Fuente/expected del reviewer no forman parte del expediente disponible.

# Criterio de finalización

Resumen breve y ruta al reporte persistido. Reporte con Resumen, Hallazgos, Evidencia, Preguntas abiertas y Recomendaciones; cada hallazgo incluye componente, mecanismo, fuente, confianza, severidad y acción propuesta. Frontmatter: fecha real, inputs y hashes reales, estado, condición; skill/version solo si realmente se cargó esa skill, none/null en baseline. Citar evidencia por archivo/fila/código según corresponda y declarar límites de inspección; no afirmar checks ejecutados si solo se leyó código.
