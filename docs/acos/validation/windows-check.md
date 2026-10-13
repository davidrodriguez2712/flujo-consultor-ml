# Validación de Windows

El recorrido automatizado pasó en Windows Server 2022 x64/Python 3.11.9 mediante [GitHub Actions](2026-10-08-github-actions-windows-report.md), y después en Windows 11 ARM64/Python 3.13.16. El [informe ARM y runtimes](2026-10-08-windows-arm-runtimes-report.md) registra además arranque y descubrimiento de skills en Claude Code/Codex nativos. Las secciones siguientes permiten repetir el recorrido de ACOS manualmente con PowerShell desde un checkout, con Python 3.11+. La [validación autenticada posterior](2026-10-09-windows-authenticated-report.md) pasó en Claude Code y Codex para x64 y ARM64: skill nativa y continuidad con `continuemos` en sesión nueva, bajo un fixture de solo lectura.

## Suite y simulaciones

```powershell
py -3.11 -m venv .venv-windows
.\.venv-windows\Scripts\python.exe -m pip install ".[dev]" "setuptools>=68" wheel
.\.venv-windows\Scripts\python.exe -m pytest -q
.\.venv-windows\Scripts\python.exe scripts\validate_business_scenarios.py --output "$env:TEMP\acos-windows-simulations.json"
.\.venv-windows\Scripts\python.exe -m build --wheel --no-isolation --outdir artifacts\windows-native-build
```

En este checkout se recolectaron 125 tests desde macOS el 2026-10-08; registrar el conteo real, errores y skips en Windows. La colección no equivale a pruebas aprobadas. La simulación existente incluye 24 escenarios / 164 comprobaciones de etapas. Una prueba crea un symlink para comprobar que un bundle no puede escapar del workspace: el equipo debe permitir crear symlinks (por ejemplo, con Developer Mode). Si esa prueba no puede crear el enlace, registrar la limitación; no contar ese resultado como cobertura de seguridad aprobada.

Para repetir con Foundry:

```powershell
.\.venv-windows\Scripts\python.exe scripts\validate_business_scenarios.py --foundry C:\ruta\david-skill-foundry --output "$env:TEMP\acos-windows-foundry.json"
```

## Executable instalado en entorno aislado

Conservar el checkout abierto. Obtener el wheel antes de cambiar de carpeta:

```powershell
$acosCheckout = (Get-Location).Path
$acosWheel = (Get-Item .\artifacts\windows-native-build\agentic_consulting_os-0.1.0-py3-none-any.whl).FullName
$acosSandbox = Join-Path $env:TEMP ("acos-check-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $acosSandbox
py -3.11 -m venv (Join-Path $acosSandbox "tool")
& "$acosSandbox\tool\Scripts\python.exe" -m pip install $acosWheel
Set-Location $acosSandbox
& "$acosSandbox\tool\Scripts\acos.exe" init --profile-file "$acosCheckout\tests\fixtures\profiles\research.yaml"
```

Rechazar guardar cambios de configuración global durante esta prueba si no se desean. Revisar clasificación y confirmar la composición sintética. Después:

```powershell
Set-Location .\research
& "$acosSandbox\tool\Scripts\acos.exe" status
& "$acosSandbox\tool\Scripts\acos.exe" next
& "$acosSandbox\tool\Scripts\acos.exe" validate
```

Resultados esperados: status/next exit 0; validate exit 3 (`NEEDS_REVIEW`), porque nadie ha revisado discovery. Comprobar `$LASTEXITCODE` inmediatamente después de cada comando. El proyecto generado no equivale a un gate aprobado.

Mover `research` a otra carpeta nueva y repetir status/next/validate sin usar el checkout ni consultar Foundry. Registrar también una prueba de `init --here` en una carpeta de prueba con un archivo ajeno: debe conservarlo; un MANUAL.md existente debe causar conflicto sin sobrescribirlo.

## Registro requerido

Anotar fecha, versión de Windows/Python, arquitectura, comandos, exit codes, resultado de suite/simulaciones, instalación del wheel, traslado y cualquier fallo. La matriz de release acredita solo las combinaciones ejecutadas; una combinación nueva requiere su propia evidencia. La carga de skills por Claude Code/Codex es una comprobación adicional del harness, no una consecuencia de pasar pytest.

## Preparación actualizada — 2026-10-08

El wheel histórico de `dist/` difiere de la fuente actual en `acos/project.py`; no usarlo para acreditar el comportamiento vigente. El recorrido anterior construye un wheel nuevo en `artifacts/windows-native-build` y lo instala en el entorno de prueba. Conservar el hash del wheel realmente instalado.

También se construyó desde macOS un wheel separado, con sus 32 archivos de paquete idénticos a la fuente, en `artifacts/windows-readiness-2026-10-08/`. Los hashes y colección de tests están en [readiness-checks.json](../../../artifacts/windows-readiness-2026-10-08/readiness-checks.json). No se sobrescribió el wheel histórico ni se cambió la instalación del usuario. Este check histórico preparó la ejecución; los informes de GitHub Actions enlazados arriba registran la validación nativa posterior.

## Smoke del wheel fuera del checkout — 2026-10-08

Nueve comandos comprobados en macOS sobre el contenido extraído del wheel: init, status/next/validate antes y después de trasladar proyecto, init --here conservando archivo ajeno y colisión de MANUAL sin sobrescritura. validate devuelve3 por Discovery no revisado; no se aprobaron gates sintéticos. Python/dependencias del entorno existente, sin Foundry/config global y sin llamadas API. No equivale a instalar o ejecutar en Windows. [Resultados](../../../artifacts/windows-readiness-2026-10-08/wheel-smoke-checks.json).
