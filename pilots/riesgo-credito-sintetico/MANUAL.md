# Manual — Piloto sintético de riesgo de crédito

## Decisión del proyecto

Priorizar solicitudes para revisión manual con capacidad de 100 revisiones al mes; la decisión de aprobar corresponde al reviewer humano.

Métrica de éxito: Discriminación y calibración temporal en créditos concedidos con label madura; ranking de solicitudes como propuesta pendiente de validación en rechazadas.
Restricciones: Datos 100% sintéticos, seed 20261008; no extrapolar resultados a solicitantes reales., Capacidad del laboratorio: hasta 100 revisiones mensuales, sin aprobación o rechazo automático., Target: 30 días de mora alcanzados dentro de 90 días desde desembolso; label completa disponible al día 97., Rechazadas sin outcome observado; no asumir ausencia de mora ni generalización del modelo a esa población., Ranking por riesgo como propuesta; no identificar ahorro, impacto de revisión ni valor causal., Ejecución local; sin llamadas adicionales a APIs.

## Situación al inicializar

Etapa: discovery
Objetivo: Comprender contexto, stakeholders, fuentes y restricciones.

Esta sección es una vista inicial. Leer `.acos/state.yaml` o ejecutar `acos status` y `acos next` para la situación vigente.

## Tu siguiente trabajo

1. Revisar PROJECT, profile y estado canónico; resolver preguntas abiertas.
2. Acordar un contrato de tarea y usar las pautas seleccionadas en `workflow/` y `playbooks/`.
3. Producir outputs con fuentes, supuestos y límites; no llenar campos sin evidencia.
4. Ejecutar `acos validate`; corregir bloqueos y obtener revisión humana.
5. Registrar evidencia, reviewer y decisión en `gate_reviews` del state. Solo después de aprobación explícita modificar etapa y registrar el cambio en DECISIONS.
6. Al cerrar sesión, actualizar STATE, MANUAL y TASKS como vistas del estado vigente.

## Preguntas de la etapa inicial

- ¿Quién decide y qué acción cambiará?
- ¿Qué fuentes y restricciones existen?

## Outputs requeridos en esta etapa

- context/business_context.md

## Capabilities disponibles

- understand-dataset 0.1.0 [experimental] — foundry:experiments/skills/understand-dataset
- design-validation 0.1.0 [experimental] — foundry:experiments/skills/design-validation
- detect-leakage 0.1.0 [experimental] — foundry:experiments/skills/detect-leakage

Ver CAPABILITIES para cobertura parcial y límites. Una skill experimental no es garantía de un entregable.

## Continuidad

`acos status`: estado, bloqueos y siguiente gate. `acos next`: objetivo, preguntas y outputs del stage actual. `acos validate`: checks y revisión; nunca cambia la etapa.

Antes de invocar una skill comprobar si el runtime la expone. Cambiar profile/composición invalida los hashes y requiere revisar/compilar un workspace nuevo; no hay update automático V1.

## Feedback de capacidades

Registrar observación local (útil/parcial/falló), tarea, versión, evidencia y límites en DECISIONS. Revisar/anonimizar antes de proponer un case o ajuste al Foundry; nunca subir datos ni promover estados automáticamente.

## Continuación vigente — Piloto cerrado

Handoff y cierre aprobados por David mediante «aprobar». Estado canónico COMPLETED, siete etapas completadas y todos los gates PASS. `acos status` y `acos next` deben mostrar cierre sin próximo gate; `acos validate` debe mostrar PASS.

Consultar `handoff/closure.md`, el runbook y el inventario de cierre. El paquete preparado para revisión se conserva como evidencia histórica; sus referencias a aprobación pendiente describen el momento anterior al cierre.

La decisión operacional global sigue parcialmente respondida. Próximas iniciativas en `handoff/next_steps.md`; no son tareas obligatorias pendientes del laboratorio. Las skills permanecen experimental. Para reproducción usar salidas nuevas según el runbook; el holdout ya está observado.
