# Runbook de reproducción

## Requisitos

Python 3.11+ para el código de análisis (verificado solo Python 3.13.2/macOS); biblioteca estándar, sin API ni servicios. El uso de comandos ACOS requiere la instalación del compiler y sus dependencias. Los tests usan pytest; no es dependencia del cálculo. Leer analysis/protocol.json y data/source_manifest.json.

## Comando desde la carpeta del proyecto

```sh
python analysis/run_forecast.py --project . --output reports/run-nuevo
```

El destino debe ser nuevo; el runner rechaza uno existente. No modificar raw, protocolo ni outputs anteriores. Reproducir la misma estrategia constituye verificación, no una evaluación con datos nuevos ni permiso para retunear final.

Recorrido: gzip CSV UTF-8 → conteo semanal → CSV guardado/releído (actual int) → predicciones development CSV guardadas/releídas (float .17g) → strategy JSON guardado/releído → predicciones finales CSV guardadas/releídas → métricas y manifests. Cutoff y método son strings; ordenar temporalmente por fecha, no por posición del CSV.

Comparar por cutoff+method: actual/keys/selección exactos; prediction rtol=0, atol=1e-12 predefinidos. En esta reproducción siete archivos coincidieron byte por byte. Ante diferencia, preservar intento, investigar primera frontera y entorno; no ampliar tolerancias silenciosamente.

## Uso y límites

Usar solo con datos/entorno autorizados. No convertir facturas a personal sin tiempos y capacidad. Inspeccionar subestimación, semanas de cierre y frescura. Datos actuales necesitan nuevo framing y evaluación. No afirmar comportamiento fuera del mismo host/Python ni completitud operativa del extract.
