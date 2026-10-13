# Feedback de capacidades

## Alcance y madurez

Uso nativo guiado por una persona/agente con diseño conocido. Datos reales, engagement simulado. No es evaluación ciega ni baseline/treatment de eficacia. Las cuatro skills permanecen **experimental0.1.0**; no se escribieron/promovieron artefactos en Foundry. Resultado de reproducibilidad del análisis no demuestra eficacia de una skill.

| Capacidad | Tarea/output | Expected verificable | Utilidad observada y límites |
|---|---|---|---|
| understand-dataset0.1.0 | reports/dataset/dataset-understanding-2026-10-09.md | Unidad transacción, mapping, ID/fechas, dos hojas y cobertura explícitos | Sirvió como checklist. Auditoría determinista detectó overlap; no atribuir detección autónoma o mejora a la skill sin comparación. |
| design-validation0.1.0 | reports/validation/validation-design-2026-10-09.md | Futuro mensual de conocidos, labels maduras, final reservado, cuatro propósitos distinguidos | Diseño justificó entidades compartidas y mostró primer fit frágil a7d. No demuestra latencia real ni superioridad sobre trabajar sin skill. |
| build-features0.1.0 | reports/features/feature-plan-2026-10-09.md | Hipótesis/input/ventana/viabilidad por señal y descartes de familias | Plan separó diseño e implementación. No prueba aporte predictivo; modelos pierden baseline y eso no mide fallo de la skill por sí solo. |
| detect-leakage0.1.0 | reports/leakage/leakage-audit-2026-10-09.md y-02.md | Mecanismo/confianza, ventanas, joins, scaler fittrain y no reselección final | No leakage confirmado en alcance inspeccionado; as-of no determinable. El overlap de entidades no implica contaminación en clientes conocidos: mantener contexto para no convertir heurísticas en reglas universales. |

## Gaps y candidates existentes

Foundry consultado solo en lectura; rutas siguientes relativas al Foundry. Estado de fichas consultadas: candidate/mantener como conocimiento. No reabrir o promocionar automáticamente.

| Necesidad del piloto | Candidate relacionado | Tratamiento propuesto tras este caso |
|---|---|---|
| Framing de decisión, KPI y observabilidad | candidates/2026-10-04-acos-frame-business-decision.md | Reutilizar template/gate existente primero; aquí no se observó un fallo que exija skill nueva. |
| Top-K, misma población, empates y baseline ganador | candidates/2026-10-04-acos-evaluate-operational-selection.md | Adjuntar evidencia local si se decide revisión; contrato/tests cumplieron. No declarar recurrencia real ni evaluar targeting causal. |
| Claims y límites de síntesis ejecutiva | candidates/2026-10-04-acos-synthesize-evidence-to-recommendation.md | Playbook/template y verificadores de43claims fueron suficientes; no basta el éxito para crear skill/agent. |
| Labels maduras y observabilidad supuesta | candidates/2026-10-04-acos-validate-delayed-outcome-targets.md | Mantener decisión previa de conocimiento. Sensibilidad7d no acredita fallo real del baseline actual; no reactivar variantes retiradas. |
| Separar venta observada de efecto/ROI | candidates/2026-10-04-acos-quantify-decision-impact.md | No faltan costes por descuido: son no observados en fuente; reporte limita conclusión. No inventar business case. |

## Problemas concretos del proceso

1. Freeze Discovery incluyó dos planes mutables: actualización legítima produjo mismatch. Se conservaron hashes y originales, versionando manifest02. Evidencia: reports/framing/freeze-incident.json. Hipótesis local: template/regla de freeze que distinga vistas mutables y copias históricas; no crear candidate automática.
2. Log de estabilidad usó índice posicional y etiquetó un intervalo como último. JSON completo correcto; correction.json conserva el error y valor correcto. Hipótesis local: checks de etiquetas/cutoffs además de cifras. No convertirlo automáticamente en skill.
3. `python3` del dispositivo era3.14, mientras el entorno original usa3.13; instalación inicial sufrió DNS restringido. Runbook fija minor explícito, reconstrucción nueva desde lock y logs. Problema de entorno, no evidencia contra skills metodológicas.

## Cómo usar este feedback

Antes de trasladar evidencia al Foundry, revisar y anonimizar contexto; decidir si basta conocimiento, template, gate o test. Para capacidad nueva/ampliada: candidate→experimental→evaluated→validated→stable, con evaluación independiente y expected fuera del contexto. Este Handoff registra hipótesis, no ejecuta esa evaluación ni asigna autoridad a agents nuevos.

## Evidencia adicional del Handoff

El primer harness de reproducción omitió persistencia/lectura CSV y divergió en scores de árboles; respetar solo tolerancia de inputs no garantiza estabilidad del ajuste. La segunda reproducción conserva recorrido original y pasa. Hipótesis local: runbook/contrato de fronteras de serialización antes de crear capacidad nueva. Esto es un fallo de implementación del harness, no una evaluación de efficacy de las cuatro skills. Review nativo registra además helpers ligados al schema numérico; hardening de API general fuera de este piloto.
