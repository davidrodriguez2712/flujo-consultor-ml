# Runbook de reproducción

## Qué permite este proyecto

Benchmark retail histórico aprobado hasta Delivery. Baseline `historical_sales`, venta positiva válida y horizonte90d; encargo/capacidad simulados. Handoff todavía requiere revisión humana. Los artefactos originales se conservan; reproducir significa recalcular la misma estrategia y comparar, sin nueva selección ni evaluación comercial.

## Requisitos

Python **3.13** (ejecución original3.13.2), paquetes exactos en `analysis/requirements.lock.txt`, fuente Excel y copia normalizada incluidas. Instalar desde un índice autorizado requiere red; después los cálculos son locales. No necesita credenciales API, Foundry ni servicios de modelos. Rutas de fuente del manifest son provenance, no dependencias de ejecución.

La comprobación realizada es local en macOS. Los comandos Windows/Linux siguientes son instrucciones equivalentes; esta reproducción no acredita haber ejecutado el análisis en esas plataformas. El lock fija versiones, no hashes de wheels ni imágenes del sistema; registrar entorno al reproducir.

## Preparar una copia independiente

Copiar el proyecto completo a otra ubicación, excluyendo `.venv-retail`, `__pycache__`, `.pytest_cache` y salidas `reproduced` anteriores. Conservar `analysis/`, `data/`, `.acos/`, `reports/`, `framing/`, `validation/`, `delivery/` y las aprobaciones/manifests. Los outputs originales son la referencia; no borrarlos para permitir un rerun.

Entrar a la raíz de esa copia. Crear **un entorno nuevo**, sin copiar el entorno original.

### macOS / Linux

```sh
python3.13 -m venv .venv-retail
.venv-retail/bin/python -m pip install --retries 0 -r analysis/requirements.lock.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 .venv-retail/bin/python -m pytest analysis -q
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 .venv-retail/bin/python analysis/reproduce_retail.py --root . --out reproduced
```

### Windows PowerShell

```powershell
py -3.13 -m venv .venv-retail
.venv-retail\Scripts\python.exe -m pip install --retries 0 -r analysis/requirements.lock.txt
$env:OMP_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"
.venv-retail\Scripts\python.exe -m pytest analysis -q
.venv-retail\Scripts\python.exe analysis/reproduce_retail.py --root . --out reproduced
```

## Resultado esperado

`reproduced/reproduction.json`: PASS. Compara normalización desde Excel, snapshots, scores development/final y ranking. Filas, keys, métodos y miembros seleccionados exactamente iguales; valores numéricos rtol1e-8/atol1e-6. Timestamps y logs no requieren igualdad byte a byte. MAE monetario no aplica a RFM ordinal.

Si output ya existe, el comando rechaza sobrescribirlo. Si evidencia/contratos cambian, la comprobación debe fallar; conservar logs y analizar causa. No cambiar criterios o hashes para forzar PASS.

## Comandos originales y restricciones

```sh
.venv-retail/bin/python analysis/run_retail.py development --root .
.venv-retail/bin/python analysis/run_retail.py holdout --root .
```

Son comandos de la ejecución original, **no instrucciones de rerun en el proyecto aprobado**. Development rechaza sobrescribir outputs; holdout rechaza un segundo intento por su marcador. No borrar marcador ni modificar aprobación/selección para habilitar otro resultado. La reproducción usa funciones congeladas con configuración aprobada en una copia y outputs nuevos; no llama otra vez esos entrypoints ni altera el marcador.

## Lectura y verificación

Leer `.acos/state.yaml`, MANUAL, contract retail/evaluation y approvals externas. `PROPOSED` en contratos es metadata histórica; la aprobación externa fija hashes. El manifest Discovery inicial tenía dos vistas mutables: usar `evidence-manifest-02.json`, conservando el inicial como incidente histórico. Verificar también manifests de Framing, Diagnosis, Execution, Validation, Delivery y Handoff.

El pipeline no utiliza rutas absolutas del dispositivo ni Foundry. Algunos logs/provenance históricos conservan rutas originales informativas. Handoff debe incluir resultados y log del entorno reconstruido, sin afirmar portabilidad general a partir de una sola máquina.

## Incidente de reproducción resuelto

La primera reproducción entrenaba desde snapshots en memoria y produjo diferencias en HistGradient. El original entrenó después de guardar/releer CSV. El harness ahora replica ambos límites de persistencia (normalizado y snapshots); pequeños cambios binarios pueden cambiar splits de árboles. Se añadieron tests, se conservó el fallo y la segunda reproducción pasó sin ampliar rtol/atol. Ver reports/handoff/reproduction-incident.json.
