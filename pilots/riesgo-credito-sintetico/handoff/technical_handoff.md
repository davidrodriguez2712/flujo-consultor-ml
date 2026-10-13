# Handoff técnico

## Componentes conservados

- `.acos/`: perfil/módulos/manifest y estado canónico; el perfil/composición iniciales no se reescribieron.
- `.agents/skills/` y `.claude/skills/`: snapshots de tres capacidades 0.1.0 experimental; AGENTS/CLAUDE son adaptadores locales.
- `data/raw/`: cinco CSV/manifest sintéticos, seed 20261008.
- `analysis/`: generator, baseline development y runner final, con sus pruebas.
- `reports/`: checks, freezes, reviews y manifests de cada fase.
- `delivery/` y `decision/`: entregables aprobados por David.

## Entrenamiento y scoring

Regresión logística L2, cinco features, 600 iteraciones, lr 0.05, L2=0.01; imputación/estandarización y referencia solo train. Un refit final al 2025-07-01 con 2.140 filas/249 positivos; modelo fijo julio–septiembre. Predicciones guardadas antes de labels del periodo final; análisis evaluable 447 concedidas maduras. Cutoff de label inclusivo y grain application_id.

No hay serving/API/UI/deployment; los scripts reproducen el análisis del fixture. No introducir esas piezas por cerrar el laboratorio.

## Conservación

Hashes en reports/execution/evidence-manifest.json, reports/final-validation/evidence-manifest.json y reports/delivery/delivery-manifest.json. Se conservan planes de development congelados; los documentos final_* complementan sus referencias. No cambiar archivos históricos para actualizar su estado de preparación: el state y aprobaciones posteriores determinan el avance.

## Pruebas y cobertura

La ejecución de Validation verificó 191 pruebas combinadas (125 producto, más pruebas del piloto/evaluaciones previas). No es evidencia de eficacia de capacidades ni cross-platform total. Minor de cobertura documentadas: ciertos bordes de imputación/ausencia, Precision parcial, cutoff exacto de evaluation y ninguna label evaluable. No bug observado; una mejora futura requiere nuevos tests/versiones y preservar evidencia actual.

## Portabilidad

Runbook con comandos relativos, fixtures y snapshots locales. Comprobación en copia fuera del checkout y replay en el mismo entorno; Windows nativo y carga automática en runtimes de otra laptop siguen fuera de esta evidencia.
