# Runbook — riesgo de crédito sintético

Versión 0.1.0 · 2026-10-08 · Handoff preparado; cierre requiere revisión humana.

## Retomar el proyecto

Desde esta carpeta:

```sh
acos status
acos next
acos validate
```

Leer `.acos/state.yaml` (canónico), MANUAL, PROJECT y CAPABILITIES. Abrir `codex` o `claude` y pedir «continuemos»; el agente debe respetar la etapa y gates del state. La copia de skills no demuestra por sí sola su exposición en un runtime: comprobarla antes de invocación nativa.

Estado esperado al preparar este runbook: handoff / IN_PROGRESS, gate Handoff NEEDS_REVIEW. Delivery y etapas anteriores aprobados. No registrar COMPLETED ni PASS de Handoff por existir archivos.

## Requisitos

ACOS 0.1.0 instalado para status/next/validate; Python 3.11+ para generator/modelos (stdlib). Pytest para pruebas. Datos/código/contracts/snapshots incluidos; no se necesita Foundry para reproducir estos modelos. Claude Code/Codex se requieren solo si se usa su interfaz; no hay llamadas a APIs en los comandos de reproducción.

## Reproducir sin cambiar evidencia

Usar siempre directorios de salida nuevos. Desde esta carpeta, con Python del entorno disponible:

```sh
python analysis/generate_synthetic_data.py --output replays/generated-data
python analysis/credit_baseline.py --freeze-file reports/execution/development-freeze.json --output replays/development
python analysis/credit_final.py --freeze-file reports/final-validation/final-freeze.json --output replays/final
```

Los runners usan `data/raw` del proyecto y verifican hashes; el primer comando produce una copia para comparar, no sustituye las fuentes. Comparar cinco CSV/manifest con data/raw, seis JSON de development y siete JSON estables de final con los outputs aceptados. `metadata.json` final contiene un timestamp nuevo; comparar sus otros campos, no exigir identidad del timestamp.

Estas ejecuciones son replay, no nueva evaluación independiente ni permiso para tuning. El holdout ya está observado. No modificar código, policy, fuentes o contratos congelados; para otra versión, usar un proyecto/evaluación nueva y datos independientes.

## Checks y errores

`acos validate` devuelve 3 para NEEDS_REVIEW, 4 para BLOCKED. Usar el contenido, no interpretar código 3 como fallo del programa. Runner rechaza destino existente o drift de hashes; conservar evidencia y resolver la causa, sin editar el freeze para ocultar cambios.

La comprobación de reproducción y portabilidad de este handoff queda en `reports/handoff/reproduction-checks.json`. Prueba en otra carpeta del mismo macOS/Python; no acredita Windows nativo ni un runtime LLM nuevo.

## Límites del resultado

Brier final 0.102487 frente a 0.116530; ROC-AUC 0.752283 en 447 concedidas maduras. No transferir esas métricas a rechazadas. Top-100 de todas las solicitudes: coverage 22–26%; métricas globales no identificadas. Calibración no certificada, benchmark mensual retrospectivo, sin causalidad/ahorro identificado.

## Cierre y siguientes trabajos

Revisar `handoff/review.md`, memo aprobado, inventario y pendientes. Tras aprobación explícita: registrar reviewer/evidencia/hash en gate_reviews.handoff, marcar etapa handoff completada, status COMPLETED y refrescar vistas. `acos status/next` deberán mostrar proyecto completado sin próximos gates.

El cierre del proyecto no madura skills. Las tres capacidades 0.1.0 siguen experimental; feedback local y next_steps no crean candidates ni modifican Foundry automáticamente.
