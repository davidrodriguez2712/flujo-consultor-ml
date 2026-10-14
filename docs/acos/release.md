# Preparación de distribución ACOS

Versión inicial: 0.1.0. Paquete: `agentic-consulting-os`; executable: `acos`.

## Desarrollo y verificación

```bash
uv sync --extra dev
uv run python -m pytest -q
uv run python -m build --no-isolation
```

El catálogo se deriva de Agentic Consulting OS 2.0; cambios del OS o templates empaquetados deben revisarse conjuntamente con `resources/catalog.yaml`. El inventario Foundry no se fija en el paquete; se inspecciona cada vez que se inicializa.

Verificar wheel en entorno limpio y carpeta diferente del checkout; inicializar con los perfiles de `tests/fixtures/profiles/`, comprobar status/next/validate y mover un proyecto sin Foundry. Mantener separación entre pruebas del compiler y evaluación de skills.

## Matriz de entrega actual

| Comprobación | Resultado/alcance |
|---|---|
| Contratos, catálogo, resolver, compiler, comandos | Suite local de software |
| Perfiles E2E | 7 fixtures de la suite + 24 simulaciones de negocio, incluyendo crédito y churn |
| macOS | Instalación aislada, CLI y generación local verificadas |
| Linux | Docker ARM64: instalación, 92 pruebas y 24 simulaciones con Python 3.11 |
| Windows x64 | GitHub Actions: Windows Server 2022 / Python 3.11.9; 125 tests, 24 simulaciones y 12 comandos de smoke aislado. [Evidencia inicial](validation/2026-10-08-github-actions-windows-report.md) |
| Windows 11 ARM64 | Runner nativo / Python 3.13.16; 125 tests, 24 simulaciones y 12 comandos de smoke aislado. [Evidencia](validation/2026-10-08-windows-arm-runtimes-report.md) |
| Python 3.11 mínimo | Verificado en Linux dentro de Docker |
| Claude Code / Codex | macOS: 4/4 pruebas reales; skill nativa design-validation y continuidad con `continuemos` verificadas. Windows x64/ARM64: instalación, arranque y descubrimiento antes/después de traslado PASS; skill nativa y continuidad autenticadas en sesión nueva PASS, 4/4 combinaciones y 8 ejecuciones. [Informe y límites](validation/2026-10-09-windows-authenticated-report.md) |
| Publicación PyPI | 0.1.0 publicada el 2026-10-13 (wheel sha256 `8d596375…`, sdist `9c64899d…`, idénticos a los artifacts locales); instalación desde el índice en venv limpio verificada (`acos --version` 0.1.0). Verificación de plataformas sigue limitada a lo indicado arriba |

No declarar cobertura de las plataformas pendientes ni eficacia de las skills por pasar estas pruebas. Leer el ledger de ejecución para comandos/resultados concretos.

Ronda adicional: [informe de validación del 2026-10-06](validation/2026-10-06-validation-report.md), con resultados por caso y siguientes pasos.

Continuación: [pruebas reales de runtime](validation/2026-10-06-runtime-report.md) y [recorrido Windows preparado](validation/windows-check.md).

## Publicación posterior

Preparar wheel/sdist, revisar versión/metadatos, documentación y evidencia de plataformas. Publicar es una acción aparte: presentar artifacts concretos para autorización antes de enviar a PyPI. Hasta publicar, instalar desde ruta o wheel local, no prometer `uv tool install agentic-consulting-os` desde el índice público.

## Actualización local — 2026-10-07

Instalación persistente de usuario realizada con uv, ACOS 0.1.0 accesible por PATH. Smoke check de proyecto copiado fuera del checkout: status COMPLETED/integrity OK y handoff PASS. [Registro](validation/2026-10-07-persistent-install-checks.json). Piloto sintético de churn cerrado; esto no certifica capacidad de skills ni plataformas pendientes.
