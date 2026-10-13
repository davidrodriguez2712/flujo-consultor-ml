# Piloto sintético de churn / retención

## Estado

COMPLETED. Siete etapas y doce gates aprobados por David. Laboratorio cerrado y entregado localmente; skills conservan su estado experimental. Datos sintéticos: Precision@50 media 10,67%, Recall@50 11,02%, Lift@50 2,52.

## Por dónde continuar

1. Leer [balance de cierre](handoff/closure.md), [runbook aprobado](handoff/runbook.md) y [MANUAL.md](MANUAL.md).
2. Consultar [decision memo](decision/recommendation.md), [aprobación final](evidence/approvals/2026-10-07-handoff.md) e [inventario de cierre](handoff/handoff-manifest-02-closed.json).
3. Ejecutar acos status y acos validate --gate handoff para verificar el cierre. Nuevos trabajos se plantean como iniciativas separadas.

## Archivos principales

- `data/raw/`: cuatro CSV de trabajo corregidos v2; usar solo estos inputs.
- `analysis/generate_synthetic_data.py`: generador reproducible, sin dependencias externas.
- `analysis/outputs/`: checks deterministas y verificación de comandos/reproducibilidad.
- `evaluation/design-validation/`: comparación exploratoria baseline/treatment y criterios fijados antes de la ejecución.
- `.acos/`: contratos y estado canónico.
- `.agents/skills/` y `.claude/skills/`: snapshots experimental de understand-dataset, design-validation y detect-leakage; no modificarlos.
- `data/interim/generator-draft-v0/`: borrador defectuoso archivado; excluido de análisis y evaluaciones.

## Reproducir datos

Desde cualquier sistema con Python 3.11+, crear los mismos CSV en un destino vacío:

```bash
python analysis/generate_synthetic_data.py --output /ruta/a/carpeta-vacia
```

Comprobar hashes contra data/raw/manifest.json. La seed es 20261007. La extracción simulada es 2026-01-15; el horizonte del target es el mes calendario que comienza al scoring y las labels maduran 7 días después de cerrar esa ventana.

## Límites

Este caso comprueba el uso del OS con datos generados. No mide generalización a un cliente real ni efecto causal de una campaña. MRR en riesgo no es margen recuperable ni ROI. La comparación de una skill en un solo caso no justifica promoción en Foundry.

## Reproducir baseline

```bash
python analysis/baseline.py --output /ruta/a/destino-vacio
```

Cinco JSON deben coincidir con analysis/outputs/baseline-development/. Ocho tests del baseline pasan. Ver model brief y policy para método y límites.

## Evaluación final preservada

Runner: analysis/evaluate_holdout.py. Outputs: analysis/outputs/holdout-final. Modelo y policy de desarrollo conservan hashes. 105 tests pasan. El test ya está observado y no debe usarse como reserva intacta para seleccionar mejoras.
