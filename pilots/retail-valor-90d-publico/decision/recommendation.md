# Recomendación

## Decisión

Conservar **historical_sales [OBS001]**, ordenando por ventas válidas del historial de 90 [ASM003] días. Elegibilidad: compra válida en los últimos 180 [ASM001] días; capacidad simulada 100 [ASM004] clientes. Son reglas del piloto, no restricciones acreditadas de una empresa real [LIM002].

La recomendación se apoya en development de 4 [OBS010] períodos: Ridge queda -14,93% [OBS017] y HistGradient -4,59% [OBS018] frente al baseline; cada uno pierde todos los períodos, según checks de aceptación congelados [OBS019][OBS020]. Ningún modelo supera la regla; no buscar más variantes en este holdout.

## Qué respalda el benchmark final

Al cutoff 2011-09-01 [OBS011], se seleccionaron 100 [OBS003] de 2.768 [OBS002] elegibles. Sus ventas válidas futuras hasta 2011-11-30 [OBS012] exclusivo fueron GBP 993.347,93 [OBS004], equivalentes al 41,25% [OBS006] de ventas elegibles. No se atribuye ese importe al efecto de contactar clientes. El resultado final describe baseline sin comparar nuevamente los modelos descartados [LIM003].

## Qué hacer con la lista

`delivery/prioritization_retrospective.csv` es una ilustración histórica, con rank, customer_id, cutoff, score y model_id. No es una campaña para ejecutar hoy ni demuestra una política óptima de contacto [LIM001][LIM002]. No usar sus IDs como contactos comerciales.

Si se requiere campaña actual: confirmar decisión, clientes elegibles, latencia y costes con el owner comercial; construir datos as-of actuales y acordar una prueba causal para medir efecto de contacto [PROP001]. Esa prueba requiere diseño y aprobación propios; este piloto no define sus parámetros.

## Condiciones

Observabilidad inmediata solo supuesta [ASM005]. Cancelaciones separadas y target positivo; no se identifican ventas netas, margen, CLV completo, uplift o ROI [LIM001]. Proponer seguimiento de estabilidad, cobertura y concentración, sin tratar estos diagnósticos como estimadores causales.

Fuente de decisión: `reports/validation/holdout-results.json`; matriz: `evidence/claims.yaml`. Revisión Delivery pendiente, sin publicación ni envío externo.
