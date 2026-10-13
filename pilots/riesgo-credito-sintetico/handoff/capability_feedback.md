# Feedback de capabilities — piloto de crédito

Fecha:2026-10-08. Observaciones locales; no evaluación canónica ni promoción del Foundry. Las tres skills siguen 0.1.0 experimental.

| Capability | Uso | Evidencia | Límite |
|---|---|---|---|
| understand-dataset | Aplicación manual de pautas | Reporte estructural, grain, keys, missing y fan-out 35.914  frente a 7.200 | Sin comparación controlada o invocación nativa nueva |
| design-validation | Aplicación manual de pautas | Diseño por disponibilidad,455 labels tardías, clientes nuevos/recurrentes | No demostrar mejora contra baseline de la skill |
| detect-leakage | Aplicación manual antes/después del pipeline | Variables posteriores, controles fit/predict/joins y audit | No garantía absoluta de ausencia ni dominio real |

La review por otro agente complementó el trabajo; el mismo reviewer conoció fases anteriores. No presentarla como ciega/humana externa. Brier favorable del modelo no prueba eficacia de las skills.

## Hipótesis y brechas reutilizables

1. Auditoría debe tratar overlap de entidades según escenario, sin llamar leakage a todo cliente compartido. La redacción de checklists podría inducir falsos positivos; aquí se aplicó el criterio de uso. No se midió un fallo causado por la skill.
2. Selección requiere distinguir población con outcomes, cobertura de labels y scores fuera de esa población. El contraste concedidas/global evidencia una limitación que debe permanecer en el memo.
3. Un Top-K retrospectivo puede no representar la decisión al llegar solicitudes. Una pauta de revisión operacional podría pedir momento, ventanas de llegada, presupuesto y efecto identificable antes de proponer política.
4. Delivery necesita preservar lineage, denominadores, calibración, incertidumbre y límites de beneficio causal. Aquí se usó el playbook/cobertura parcial, no una skill nueva.

Mantener como conocimiento/hipótesis locales. Antes de nueva candidate, revisar las fichas existentes y comprobar recurrencia, procedimiento, inputs/output y verificación. La necesidad determina skill, agent, playbook/template u otro artefacto; no convertir automáticamente estos hallazgos en capacidades.

## Disciplina Foundry

Problema/fuente → candidate → experimental → evaluated → validated → stable. El proyecto usó experimental según política autorizada; aprobar sus gates no altera madurez. No se modificó Foundry/snapshots ni se transfirió evidencia. Cualquier traslado requiere revisar/anonimizar y seguir autoridad/proceso canónicos.
