# Pruebas reales de runtime — 2026-10-06

## Resultado

4/4 pruebas aprobadas en macOS: dos con Codex CLI 0.160.0 y dos con Claude Code 2.1.290. Se repitió además la suite del producto: 92 passed en 2.51 s. No se modificó código del producto ni Foundry.

| Runtime | Prueba guiada de skill | Mensaje exacto `continuemos` | Workspace sin cambios |
|---|---|---|---|
| Codex | Leyó `.agents/skills/design-validation/SKILL.md` | Retomó validation/BLOCKED y pidió inputs faltantes | Sí |
| Claude Code | Invocó la herramienta Skill con `design-validation`, desde `.claude/skills/` | Retomó validation/BLOCKED y pidió inputs faltantes | Sí |

Las trazas muestran acciones reales de lectura/invocación, no solamente una afirmación del modelo. [Resultados y respuestas](2026-10-06-runtime-results.json).

## Fixture y criterios

ACOS compiló un workspace temporal de churn con el Foundry actual y ambos runtimes. Se cambió únicamente el estado canónico para representar una sesión posterior:

- Etapa `validation`; status `BLOCKED`.
- Objetivo `RUNTIME-CHECK-CHURN: auditar split temporal y leakage antes de recomendar retención`.
- Bloqueo: falta confirmar la fecha de disponibilidad de las labels.
- Vistas STATE/MANUAL conservadas con el objetivo inicial.
- Sin dataset, entrenamiento, resultados reales ni revisiones de gates.

En la prueba guiada se pidió retomar el proyecto, identificar vistas obsoletas y usar la skill nativa para un checklist temporal. Ambos runtimes identificaron el objetivo canónico y el bloqueo, reconocieron las vistas obsoletas, conservaron la madurez experimental de la skill y propusieron un checklist sin inventar fechas ni aprobar gates.

La segunda prueba abrió una sesión nueva con el único mensaje `continuemos`. Ambos retomaron el estado correcto, identificaron que no había datos/evidencia suficientes y solicitaron inputs concretos. Claude no invocó skills innecesariamente cuando faltaban sus preconditions. Ninguno avanzó la etapa ni aprobó un gate.

Cada ejecución comparó SHA-256 de todos los archivos del workspace antes y después: sin cambios. Esta prueba cubre reanudación desde archivos canónicos en una sesión nueva; no comprueba el mecanismo de resume de una conversación persistida ni comportamiento con permisos de escritura.

## Configuración de ejecución

Codex:

```bash
codex exec --ignore-user-config --ephemeral --skip-git-repo-check \
  --sandbox read-only --json -C /ruta/al/workspace "continuemos"
```

Claude Code, desde la carpeta generada:

```bash
claude -p "continuemos" --output-format stream-json --verbose \
  --no-session-persistence --setting-sources project \
  --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
  --tools Read,Glob,Grep,Skill --allowedTools Read,Glob,Grep,Skill \
  --permission-mode dontAsk --max-budget-usd 2
```

Se mantuvo el modelo por defecto de cada runtime. No se instalaron ni reconfiguraron runtimes. En Codex una ejecución registró un timeout al refrescar la lista de modelos, pero el turno terminó correctamente con exit 0. No fue un fallo de ACOS.

El puente generado `CLAUDE.md → @AGENTS.md` funcionó: la traza de Claude muestra la lectura de AGENTS.md y de los contratos del proyecto. En Codex, el comportamiento observado coincide con la documentación oficial: [instrucciones AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) y [skills locales](https://learn.chatgpt.com/docs/build-skills).

## Alcance pendiente

Esto verifica la integración básica real de ambos runtimes y una skill representativa, `design-validation`. No evalúa todas las skills, la eficacia estadística de sus outputs ni la operación del harness en Windows/Linux.

Siguiente trabajo: ejecutar el [recorrido Windows](windows-check.md) y comenzar un piloto real con inputs autorizados. El piloto debe comprobar outputs reproducibles, intervención humana en gates y utilidad de las skills experimental contra baseline. PyPI sigue pendiente.
