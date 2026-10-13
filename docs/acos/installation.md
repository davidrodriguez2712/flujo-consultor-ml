# Instalar ACOS

ACOS 0.1.0 es una CLI Python >=3.11. El paquete se construye localmente; todavía no está publicado en PyPI.

## Instalación una vez por laptop

Desde la carpeta de este proyecto:

```bash
uv tool install .
```

Alternativa:

```bash
pipx install .
```

Si instalas desde otra carpeta, reemplaza `.` por la ruta del checkout. `uv`/`pipx` deben estar instalados y sus comandos de tools en PATH. La instalación usa un entorno aislado por usuario; no instala Claude Code ni Codex.

También puedes instalar el wheel generado:

```bash
uv tool install /ruta/agentic_consulting_os-0.1.0-py3-none-any.whl
```

Las tres formas contienen catálogo y recursos; el workspace generado no necesita el checkout original. Para usar sin instalación global durante desarrollo:

```bash
uv sync --extra dev
uv run acos --help
```

## Crear un proyecto desde cualquier ubicación

```bash
acos init fraude-energia
cd fraude-energia
acos status
acos next
```

El wizard pregunta contexto, decisión, éxito, datos, restricciones y entrega. Las preguntas técnicas dependen de esas respuestas. Puedes omitir la identidad real del cliente. Revisa perfil, clasificación, composición y límites antes de confirmar escritura.

- Sin nombre: `acos init` pregunta el nombre y crea subcarpeta.
- En carpeta actual: `acos init --here`; rechaza colisiones, conserva archivos ajenos y no sobrescribe contenido.
- Perfil YAML: `acos init --profile-file /ruta/perfil.yaml`; sigue exigiendo revisión y confirmación.
- No hay `--yes`, actualizaciones automáticas ni creación automática de candidates/skills.

## Foundry por dispositivo

ACOS consulta la ruta configurada o propone `./david-skill-foundry` y `~/david-skill-foundry`. En el primer uso puedes indicar otra ruta y confirmar su almacenamiento. También puedes continuar sin Foundry: se generarán pautas del OS y brechas visibles, sin inventar skills.

La configuración reside en la carpeta de usuario determinada por platformdirs (`acos/config.yaml`). No se copia a proyectos. El resolver solo inspecciona `experiments/skills/` y `stable/`; scratch y snapshots de evaluaciones no son operativos. Una decisión explícita de diferir/conservar como conocimiento impide seleccionar la capacidad.

## Adapter LLM opcional

La ruta normal es local y no invoca servicios. Para `acos init --llm`, configurar voluntariamente `llm_adapter_argv` en el config del usuario. Es una lista argv de un programa propio que lee JSON de stdin y devuelve JSON por stdout:

```yaml
schema_version: 1
foundry_path: /ruta/local/david-skill-foundry
llm_adapter_argv:
  - /ruta/absoluta/python
  - /ruta/absoluta/mi_adapter.py
```

Respuesta admitida:

```json
{"archetypes": ["OPTIMIZE"], "reasons": ["Capacidad operacional limitada"], "unresolved": []}
```

ACOS muestra el executable y el payload antes de cada invocación; solo lo ejecuta tras consentimiento. No envía archivos de datos, nombres de cliente ni credenciales. El programa configurado decide si usa un servicio; ACOS no distribuye ni configura un proveedor. Timeout/salida inválida/rechazo vuelve al classifier local. Las propuestas nunca cambian hechos de negocio ni ejecutan herramientas automáticamente.

## Plataformas

Objetivos: macOS, Linux y Windows. Se verificaron macOS/Python 3.13.2 y Linux ARM64 dentro de Docker/Python 3.11 mediante instalación, suite y simulaciones. Windows Server 2022 x64/Python 3.11.9 se verificó mediante [GitHub Actions](validation/2026-10-08-github-actions-windows-report.md); el [recorrido PowerShell](validation/windows-check.md) permite repetirlo. También se verificó Windows 11 ARM64/Python 3.13.16 en un runner nativo: 125 tests, 24 simulaciones e instalación aislada. Claude Code 2.1.294 y Codex 0.160.0 arrancan y descubren una skill local antes y después del traslado en ambas arquitecturas de Windows. Además, skill nativa y continuidad autenticadas con `continuemos` pasan en las cuatro combinaciones de runtime/arquitectura, en sesión nueva y solo lectura. [Informe autenticado](validation/2026-10-09-windows-authenticated-report.md). [Evidencia y límites](validation/2026-10-08-windows-arm-runtimes-report.md), [matriz de release](release.md).

## Instalación persistente verificada — 2026-10-07

ACOS 0.1.0 instalado mediante `uv tool install .` desde el checkout local. Executable: `/Users/davidrodriguez/.local/bin/acos`; entorno aislado administrado por uv en `/Users/davidrodriguez/.local/share/uv/tools`. El comando se resolvió desde PATH fuera del repositorio.

Se copió el laboratorio cerrado a una carpeta temporal externa y se comprobaron `acos --version`, `acos status` (COMPLETED, integrity OK) y `acos validate --gate handoff` (PASS). [Evidencia](validation/2026-10-07-persistent-install-checks.json). Esta instalación persistente se comprobó en macOS. Posteriormente se verificó instalación aislada por wheel en Windows x64 y ARM64; eso no verifica una instalación persistente con uv/pipx en Windows. No se publicó el paquete en PyPI.

Puedes iniciar el siguiente proyecto desde cualquier carpeta con `acos init nombre-proyecto`. La instalación no es editable: cambios futuros en el código requieren reinstalar/actualizar la herramienta de forma explícita.


## Actualizar la instalación después de un cambio local

Desde este checkout:

```bash
uv tool install --reinstall .
```

La mejora de cierre de `status`/`next` se reinstaló y verificó el 2026-10-07 con una copia del piloto fuera del repositorio. Esta revisión local conserva la versión `0.1.0`; la [evidencia](validation/2026-10-07-closure-cli-checks.json) identifica el hash del código comprobado. No es una nueva release publicada.
