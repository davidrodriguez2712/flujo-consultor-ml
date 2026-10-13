# Operar un proyecto ACOS

## Punto de entrada

Lee MANUAL.md y PROJECT.md, y ejecuta:

```bash
acos status
acos next
```

Abre `codex` o `claude` si tienes el runtime instalado. AGENTS.md conserva las instrucciones compartidas; CLAUDE.md es un puente mínimo. Las skills se copian a `.agents/skills/` o `.claude/skills/` según el runtime confirmado, con bytes/version/hash idénticos cuando se seleccionan ambos. Verifica su exposición en el harness antes de invocarlas.

## Qué es canónico

- `.acos/project-profile.yaml`: perfil confirmado al compilar.
- `.acos/modules.yaml`: composición confirmada, motivos, límites y gaps.
- `.acos/state.yaml`: etapa, objetivo, bloqueos, decisiones abiertas y revisión de gates.
- `.acos/manifest.yaml`: versión/procedencia e integridad de snapshots.
- `TASKS.md`: backlog humano NOW/NEXT/LATER/BLOCKED.
- `DECISIONS.md`: rationale y aprobaciones.

STATE.md y la sección inicial de MANUAL son vistas; el agente debe refrescarlas al cerrar sesión. Los comandos de lectura nunca reescriben archivos. No editar snapshots; cambios del perfil o composición invalidan la compilación y exigen revisar/compilar un workspace nuevo (V1 no ofrece update).

## El ciclo diario

1. Leer profile/state y preguntar por contexto faltante que afecte la decisión.
2. Definir una tarea con inputs, output, preconditions y aceptación.
3. Consultar el playbook pertinente y las capabilities disponibles.
4. Producir evidencia y outputs reproducibles, conservando límites y supuestos.
5. Ejecutar `acos validate` o `acos validate --gate framing`.
6. Corregir campos faltantes/integridad y pedir revisión del contenido a la persona responsable.
7. Registrar reviewer, evidencia y decisión antes de avanzar state; dejar rationale en DECISIONS.
8. Actualizar TASKS, STATE y MANUAL al cerrar la sesión.

## Aprobar un gate

`PASS` combina checks deterministas con una declaración de revisión humana trazable. No certifica matemáticamente que el análisis sea correcto. Plantillas Markdown existentes no prueban que el contenido esté completo; el reviewer debe revisarlo.

Ejemplo para discovery, tras revisar el contenido:

```yaml
gate_reviews:
  discovery:
    decision: PASS
    reviewer: David
    evidence:
      - context/business_context.md
    profile_sha256: <copiar valor de .acos/manifest.yaml>
```

El state debe conservar sus otros campos. Reviewer vacío, evidencia ausente/vacía, hash diferente o outcome incompleto no aprueban el gate. Las evidencias deben ser rutas relativas dentro del workspace, sin symlinks. Para YAML se comprueban campos obligatorios; por ejemplo framing requiere decision, owner, metric, unit y horizon. El método y su interpretación siguen requiriendo QA.

Solo tras aprobar todos los gates de la etapa, el consultor autoriza añadirla a `completed_stages`, cambiar `current_stage` y actualizar `objective`. No existe comando automático de avance V1. Si se inició en evaluación de un modelo heredado, no se marcan completas discovery/framing por defecto: recuperar o documentar sus inputs antes de afirmar conclusiones.

Codes: `0` operación correcta/PASS; `2` entrada inválida; `3` NEEDS_REVIEW; `4` BLOCKED/conflicto; `130` cancelación. No confundir `acos status` exitoso con un gate aprobado.

## Proyecto completado

Cuando `state.status` es `COMPLETED`, los comandos comprueban la integridad, las aprobaciones y los contratos de los gates antes de comunicar el cierre:

- `acos status`: conserva la etapa `handoff` y muestra `next_gates: []` si el cierre es válido.
- `acos next`: muestra «Proyecto completado; no hay una siguiente etapa», con `questions: []`, `outputs: []` y `gate: null`.
- Si el cierre es inconsistente, ambos muestran `integrity: BLOCKED`, hallazgos concretos y devuelven código `4`; `next` indica corregir y validar el cierre.

El campo `status` conserva el valor declarado en state, incluso si la verificación lo bloquea. Interpretarlo junto con `integrity` y `findings`. Las capabilities y sus gaps siguen visibles como contexto; su presencia no implica trabajo pendiente después del cierre. Estos comandos no modifican archivos ni avanzan etapas. [Comprobación del cierre y de la instalación local](validation/2026-10-07-closure-cli-checks.json).

## Brechas y feedback

Una pauta/template puede permitir trabajar sin una skill específica. CAPABILITIES declara cobertura parcial; no presenta conocimiento como skill nativa. Las skills experimental requieren revisar sus outputs dentro de su alcance, sin promoción implícita.

Registrar feedback local con nombre, versión, tarea, evidencia y resultado (útil/parcial/falló). Revisar y anonimizar antes de trasladar algo al Foundry; no hay sincronización, publicación ni promoción automática. Las decisiones de mantener como conocimiento o diferir se respetan hasta que un nuevo fallo/fuente cumpla el trigger de reapertura.

## Conflictos y recuperación

`init` no sobrescribe un destino existente ni colisiones con artifacts seleccionados en `--here`. Si falla la escritura, intenta retirar solo sus propios archivos sin cambios; si algo quedó modificado, informa rutas para revisión. El manifest se escribe último: sin `initialization: complete`, el proyecto no está listo. Un lock de inicialización existente requiere investigar la ejecución propietaria; V1 no lo borra ni reanuda silenciosamente.
