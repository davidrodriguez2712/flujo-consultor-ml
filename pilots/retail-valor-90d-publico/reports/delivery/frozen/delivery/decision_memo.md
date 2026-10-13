# Decision memo — priorización comercial retail

## Decisión propuesta

**Mantener el baseline historical_sales [OBS001]** para este benchmark. El encargo y cliente son simulados; las transacciones UCI son reales e históricas [LIM002]. El ranking sirve para ilustrar una revisión comercial, sin campaña observada.

## Evidencia para decidir

| Desarrollo | Ventas válidas Top-K agregadas | Frente al baseline |
|---|---:|---:|
| Ventas históricas | GBP 2.606.803,55 [OBS014] | Referencia |
| Ridge | GBP 2.217.514,29 [OBS015] | -14,93% [OBS017] |
| HistGradient | GBP 2.487.103,96 [OBS016] | -4,59% [OBS018] |

Comparación sobre 4 [OBS010] períodos y misma población por cutoff. Ambos modelos pierden en todos los períodos [OBS019][OBS020]; ninguno cumple la aceptación. Selección congelada antes del final, sin tuning posterior.

En el final histórico (2011-09-01 [OBS011] → 2011-11-30 [OBS012] exclusivo): 100 [OBS003] seleccionados de 2.768 [OBS002] elegibles concentran **GBP 993.347,93 [OBS004]**, el **41,25% [OBS006]** de ventas válidas elegibles. Este es desempeño descriptivo del baseline; no una mejora comparativa final ni ventas adicionales causadas por contactarlos [LIM003].

## Precauciones que afectan la decisión

- Concentración de outcome dentro del Top-K: Top-1 11,84% [OBS008]; Top-10 54,57% [OBS009]. El resultado depende de pocos clientes con compras grandes.
- Cancelaciones se auditan aparte: 522 [OBS027] líneas de 51 [OBS028] seleccionados; importe firmado GBP -47.363,08 [OBS029]. No restarlo para atribuir ventas netas sin vínculo con compras originales.
- Capacidad 100 [ASM004] e historia/horizonte son supuestos del encargo; disponibilidad as-of no acreditada [ASM005][LIM002].
- Cero ventas futuras no demuestra churn; clientes anónimos/nuevos sin historia quedan fuera del ranking. El target no identifica beneficio, CLV completo o efecto de contacto [LIM001].

## Siguiente decisión

Aprobar una futura validación con datos actuales as-of y, si interesa efecto comercial, una prueba causal con población y costes acordados [PROP001]. La lista histórica no debe activarse como campaña actual.

## Calidad y coste

50 [OBS032] tests pasan; selección previa y apertura final única trazables [OBS034]. Gasto API **US$0 [OBS013]**. El coste reportado no incluye tiempo humano, infraestructura o herramientas.

Fuente: Chen, D. (2012), [Online Retail II — UCI](https://archive.ics.uci.edu/dataset/502/online+retail+ii), licencia CC BY 4.0. Provenance: `data/source_manifest.json`. Estado: Delivery pendiente de revisión.
