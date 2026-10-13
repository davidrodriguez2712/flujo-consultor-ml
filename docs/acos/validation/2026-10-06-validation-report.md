# Validación de ACOS 0.1.0 — 2026-10-06

## Estado final

V1 apta para un piloto local supervisado en macOS y Linux. No se encontraron fallos del producto en esta ronda. Windows y PyPI siguen pendientes. La continuación verificó la integración básica real de Claude Code/Codex en macOS: [4 pruebas de runtime](2026-10-06-runtime-report.md).

Se aplicó `superpowers:verification-before-completion`: los resultados siguientes provienen de ejecuciones nuevas. No se modificaron las skills ni las decisiones del Foundry.

## Resultados ejecutados

| Entorno / recorrido | Resultado |
|---|---|
| macOS, Python 3.13.2, suite completa | 92 passed, 2.22 s; se repitió al terminar |
| Linux ARM64 en Docker, imagen local `python:3.11-slim`, instalación aislada desde source | 92 passed, 2.36 s |
| macOS, source y Foundry actual | 24/24 escenarios; 164 comprobaciones de etapas |
| macOS, wheel previamente instalado en entorno aislado y Foundry actual | 24/24 escenarios; 164 comprobaciones de etapas |
| Linux, paquete instalado y sin Foundry | 24/24 escenarios; 164 comprobaciones de etapas, gaps explícitos |
| macOS, executable `acos` instalado fuera del checkout | init 0; status 0; next 0; validate 3 (`NEEDS_REVIEW`, esperado) |
| Workspace del smoke trasladado a otra carpeta | next 0; archivos idénticos antes/después de comandos de consulta |
| Build nuevo de wheel y sdist | Exit 0; ambos artifacts 0.1.0 generados |

Son 24 escenarios distintos, repetidos en tres configuraciones; no 72 problemas diferentes. Linux se ejecutó con kernel Linux dentro de Docker en macOS, no en una laptop Linux independiente. Windows no se ejecutó.

La suite incluye contratos, YAML, classifier, resolver, selección del Foundry, bundles ocultos, integridad de snapshots, cancelación, conflictos de destino, rollback, gates, LLM inválido/timeout y distribución. Los escenarios nuevos usan las APIs del paquete; el smoke verifica además los cuatro comandos mediante subprocess del executable instalado.

## Escenarios nuevos

1. Fraude eléctrico: predicción, priorización y optimización.
2. Riesgo de crédito: predicción y selección.
3. Churn: predicción y priorización de retención.
4. CLV: predicción de valor y optimización de presupuesto.
5. Uplift: evaluación causal y selección de intervención.
6. Anomalías sin labels: diagnóstico y selección, sin modelo supervisado.
7. Forecast de demanda.
8. Inventario: forecast y optimización.
9. Pricing: evaluación causal y optimización.
10. Segmentación.
11. Recomendaciones.
12. Rutas: optimización con información geográfica.
13. Staffing: forecast y optimización.
14. Experimento A/B.
15. Causal observacional.
16. Entrada a mercado: research.
17. RAG: solución GenAI y recomendación.
18. Extracción de documentos: solución GenAI.
19. API sin UI: software y modelo; skills UI excluidas.
20. Dashboard: UI planning.
21. Figma handoff: Figma, Design System y React/shadcn confirmados.
22. Visual QA: UI implementada y Orca confirmado.
23. Modelo heredado: entrada en validation.
24. Modelo en producción: operacionalización y feature design.

En cada escenario se verificaron módulos esperados, exclusiones supervisadas/UI relevantes, composición reproducible, workspace generado, gate inicial sin PASS, outputs sintéticos sin revisión → NEEDS_REVIEW, recorrido de etapas con revisiones ficticias → PASS, cierre, consultas sin escritura, traslado y cambio del perfil → BLOCKED. Restaurar el perfil recuperó PASS.

Los outputs y revisores están marcados `SIMULACIÓN`. Son pruebas de estructura, trazabilidad y lógica del compiler; no ejecutan análisis estadístico, entrenamiento, recomendaciones financieras ni evaluación de resultados de cliente. El modelo heredado incluye evidencia sintética de requisitos anteriores, sin declarar esas etapas completadas.

## Foundry y gaps

El scanner encontró 9 skills operativas y ninguna incidencia. Las simulaciones seleccionaron estas 8 según el contexto:

- build-features
- design-validation
- detect-leakage
- figma-handoff
- research-intelligence
- ui-planning
- understand-dataset
- visual-qa

`run-skill-eval` quedó fuera de los proyectos de cliente. Las skills seleccionadas conservaron su madurez `experimental`; ninguna se promovió por estas pruebas.

Persisten capacidades con cobertura parcial por playbooks: framing, síntesis de evidencia, evaluación causal, forecast, optimización, selección operacional, impacto, recomendaciones, segmentación, GenAI, diseño de software, monitorización y síntesis ejecutiva. También hay gaps condicionales de features/Figma/QA cuando faltan sus preconditions. No todos estos gaps requieren crear una skill; deben contrastarse con las 24 fichas y sus decisiones actuales antes de abrir nuevos candidates.

## Evidencia y reproducción

- [Resultados por caso con Foundry](2026-10-06-business-simulations.json).
- [Resultados del wheel instalado](2026-10-06-installed-wheel-simulations.json).
- [Runner reproducible](../../../scripts/validate_business_scenarios.py).

Desde el checkout:

```bash
.venv/bin/python -m pytest -q
PYTHONPATH=src .venv/bin/python scripts/validate_business_scenarios.py \
  --foundry /ruta/a/david-skill-foundry --output /tmp/acos-simulations.json
.venv/bin/python -m build --no-isolation
```

Sin `--foundry`, el runner comprueba el funcionamiento con pautas OS y gaps. Para verificar la distribución se puede ejecutar el mismo runner con el Python del entorno donde esté instalado el wheel, sin `PYTHONPATH`.

La prueba Linux copió source/tests al filesystem temporal del contenedor, instaló `/tmp/acos[dev]`, ejecutó `python -m pytest -q /tmp/acos/tests` y después el runner sin Foundry. El host se montó solo para lectura y el contenedor se eliminó al terminar.

## Siguientes pasos

1. Ejecutar instalación, wizard, cuatro comandos y portabilidad en Windows con Python 3.11+.
2. Integración básica de ambos harnesses completada en macOS: lectura de contratos, skill nativa design-validation y continuidad con `continuemos`. Ampliar en el piloto a las skills seleccionadas y sesiones con escritura autorizada.
3. Hacer un piloto real supervisado: registrar perfil, decisiones, evidencia, bloqueos y esfuerzo; comenzar con crédito o churn si son los casos prioritarios.
4. Evaluar las capacidades experimental utilizadas contra baseline en ese piloto; conservar o revisar candidates según las decisiones del Foundry. Las simulaciones del compiler no sustituyen esa evaluación.
5. Preparar release pública después de cerrar la matriz de plataformas/harnesses. PyPI requiere una acción de publicación posterior.
