# Validación de ACOS en Windows mediante GitHub Actions

Fecha local: 2026-10-08, America/Lima. Ejecución exitosa el 2026-10-09 03:19–03:21 UTC.

## Resultado

Validación nativa del software en **Windows Server 2022 x64 / Python 3.11.9** mediante runner `windows-2022`. Se comprobó el código del commit `051c46a71c80efaad3213e0b430d4cd4e18ada33`, versión de paquete 0.1.0; no se publicó una nueva release.

[Repositorio privado](https://github.com/davidrodriguez2712/agentic-consulting-os) · [Ejecución exitosa](https://github.com/davidrodriguez2712/agentic-consulting-os/actions/runs/37878718698).

| Comprobación | Resultado |
|---|---|
| Suite | 125 passed, 0 failures, 0 errors, 0 skipped |
| Simulaciones sintéticas del compiler | 24 casos / 164 comprobaciones de etapas |
| Wheel vigente | Construido e instalado en venv nuevo fuera del checkout |
| Smoke del executable instalado | 12 comandos con exit codes esperados |
| Traslado y rutas con espacios | status/next/validate correctos antes y después |
| `init --here` | Conserva archivo ajeno y rechaza MANUAL existente sin escribir workspace parcial |
| Gate inicial | NEEDS_REVIEW, exit 3; el probe no aprobó un proyecto de consultoría |
| Artifact | Descargado localmente; logs, dependencias, JUnit, simulaciones, wheel y smoke |

El smoke comprueba que el módulo procede del venv activo, sin PYTHONPATH del checkout. Usa el executable instalado y confirma perfiles sintéticos por stdin; no prueba todas las preguntas del wizard ni ejecuta runtimes LLM. Las simulaciones usan aprobaciones sintéticas para probar el software, no representan aprobación humana de entregables.

## Intentos y correcciones

1. [Run 01](https://github.com/davidrodriguez2712/agentic-consulting-os/actions/runs/37878382343): 124 passed, un fallo al construir wheel. El runner tenía setuptools 65.5.0; la instalación del workflow no exigía el mínimo >=68 del build-system. Se corrigió el requisito del workflow y del recorrido documental.
2. [Run 02](https://github.com/davidrodriguez2712/agentic-consulting-os/actions/runs/37878523298): suite, simulaciones y build correctos; falso positivo del smoke por comparar alias Windows corto RUNNER~1 con runneradmin. Se sustituyó la comparación textual externa por una comprobación resuelta dentro del Python del venv.
3. [Run 03](https://github.com/davidrodriguez2712/agentic-consulting-os/actions/runs/37878718698): todos los pasos correctos. Se conservan artifacts de los tres intentos; no se omitieron tests ni se modificó código del compiler para obtener el resultado.

Hay un aviso de deprecación del runtime Node.js 20 de checkout/upload-artifact v4, ejecutados por GitHub con Node.js 24; no produjo fallo. Actualizar acciones puede tratarse en una revisión posterior del workflow.

## Reproducción

Workflow manual [windows-validation.yml](../../../.github/workflows/windows-validation.yml), sin ejecución automática por push ni schedule. Desde una sesión autenticada:

```sh
gh workflow run windows-validation.yml --repo davidrodriguez2712/agentic-consulting-os --ref main
gh run list --repo davidrodriguez2712/agentic-consulting-os --workflow windows-validation.yml
```

Seleccionar el run y usar `gh run watch <id> --repo davidrodriguez2712/agentic-consulting-os --exit-status`. Descargar con `gh run download <id> --repo davidrodriguez2712/agentic-consulting-os --dir <carpeta-nueva>` antes de que expire el artifact (14 días). Las ejecuciones usan recursos de GitHub Actions; no se midió ni se afirma coste cero.

## Evidencia y alcance

- [Metadatos remotos](../../../artifacts/github-actions-windows-2026-10-08/run-03-metadata.json).
- [Resumen comprobado](../../../artifacts/github-actions-windows-2026-10-08/verification.json).
- [Inventario local](../../../artifacts/github-actions-windows-2026-10-08/evidence-manifest.json).
- Archivos descargados en `artifacts/github-actions-windows-2026-10-08/run-01`, `run-02` y `run-03`.

Repo privado creado por instrucción de David: 69 archivos de código, recursos, tests, schemas, utilidades y el checker requerido por tests. No se subieron Foundry, pilotos, fuentes/datos de esos pilotos ni resultados históricos. El Git usado para publicar está en una copia temporal; el workspace original conserva su organización sin inicializar Git.

El resultado acredita este recorrido de CLI en Windows Server 2022 x64. Windows 11/ARM, Claude Code/Codex nativos en Windows, carga de skills en esos harnesses y consultoría con datos reales no están acreditados. No hay nueva evidencia de eficacia de skills ni promoción del Foundry. Se conserva la evidencia congelada de los pilotos cerrados.

## Continuación posterior

El [informe Windows 11 ARM y runtimes](2026-10-08-windows-arm-runtimes-report.md) registra la siguiente ronda: ACOS y descubrimiento local de skills en ambos runtimes pasan en Windows x64 y ARM64. La conversación autenticada continúa pendiente. Los artifacts y resultados de este informe se conservan como evidencia de la primera ronda.
