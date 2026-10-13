# Selección mensual — benchmark retrospectivo

Ranking descendente de score, empate por application_id ascendente; hasta100 solicitudes de cada población declarada. K efectivo=min(100,elegibles). Filas únicas por solicitud; no deduplicar clientes.

En development se evalúan concedidas maduras de enero/febrero2025: Precision, Recall y Lift por mes con población y denominadores explícitos. No extrapolar a las listas de todas las solicitudes. Si una población tiene labels incompletos, Recall/Lift no identificados; Precision solo si todos los seleccionados tienen label observado. Coverage seleccionado se reporta aparte. Sin positivos, Recall/Lift indefinidos; conK0,Precision/coverage indefinidas.

La lista mensual retrospectiva no prueba que la revisión podría haberse ejecutado antes de aprobación/desembolso. Sin efecto de revisión ni ahorro identificado. La decisión real de conceder permanece bajo responsabilidad humana.
