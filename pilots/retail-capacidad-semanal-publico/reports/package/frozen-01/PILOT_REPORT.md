# Piloto integrado — forecasting de volumen semanal

**Estado:** ensayo técnico preparado; aceptación humana pendiente. Fuente pública real, contexto de negocio simulado. Costo API US$0.

## Decisión y datos

Proponer una previsión de facturas positivas registradas por semana en Reino Unido como proxy de carga de preparación. No hay datos de horas, personal, productividad o capacidad para convertirla en staffing óptimo.

UCI Online Retail II, Chen, D. (2012), CC BY 4.0, DOI 10.24432/C5CG6D. [Fuente](https://archive.ics.uci.edu/dataset/502/online+retail+ii). Se reutilizó una copia independiente del CSV normalizado del piloto anterior, con SHA-256 verificado; no se reparseó el Excel original.

Se revisaron 1.067.371 filas; 958.501 califican como líneas positivas UK. El target cuenta invoice_id únicos por semana con al menos una fila calificante, incluyendo facturas sin customer_id. Se excluyen cancelaciones C y quantity/price no positivos. Hay 104 semanas interiores de calendario; primera y última parciales excluidas. Semanas 2009-12-28 y 2010-12-27 tienen cero facturas observadas; no se confirmó completitud externa ni ausencia de demanda.

## Resultados

| Tramo / método | Semanas | Facturas observadas | WAPE | MAE, facturas/semana | Bias, facturas/semana |
|---|---:|---:|---:|---:|---:|
| Development / semana anterior | 30 | 8.670 | 18,40% | 53,17 | −10,50 |
| Development / media de 4 semanas | 30 | 8.670 | 15,21% | 43,95 | −11,80 |
| Final / media de 4 semanas elegida | 18 | 7.439 | 13,15% | 54,33 | −37,92 |

Development: [2011-01-03, 2011-08-01); final: [2011-08-01, 2011-12-05). Forecast de una semana, usando solo semanas anteriores. Se persistió la elección por WAPE de development antes de generar/evaluar final; no se evaluó baseline final. No afirmar superioridad en final frente a un método no comparado allí.

Última semana completa final: **[2011-11-28, 2011-12-05)**; forecast **556,5** frente a **608** facturas observadas. Semana 2011-12-05 incompleta y excluida.

## Tres mejoras ejercitadas

| Mejora | Resultado | Evidencia |
|---|---|---|
| Freeze frente a documentos vivos | PASS: versiones históricas y manifest intactos | [Checks](reports/validation/freeze-check.json) |
| Reproducción con serialización | PASS: 7 archivos idénticos en copia independiente | [Checks](reports/reproduction/reproduction-check.json) |
| Correspondencia cifra/etiqueta/período | PASS: error deliberado detectado y fuente conservada | [Checks](reports/qa/label-check.json) |

**153 tests pasan**: 146 del compiler y 7 del análisis. [Revisión integrada](reports/validation/integrated-review.md). La evidencia del piloto anterior conservó sus hashes.

## Recomendación y aceptación

Usar la media de cuatro semanas como referencia retrospectiva de este caso y revisar su subestimación. Antes de uso real: datos actuales, calendario de cierres/eventos, latencia, tiempos/capacidad y costo de errores; definir criterio operativo con un owner real.

[Decision memo](decision/recommendation.md) · [Runbook](handoff/runbook.md) · [Feedback](handoff/capability_feedback.md).

El state permanece en **validation / IN_PROGRESS**, sin etapas completadas ni gates aprobados. Delivery y handoff son paquetes preparados para revisión; no hay avance silencioso. Los tests no sustituyen aceptación humana. No se instalaron skills ni se modificó Foundry.

Límites: datos 2009–2011 ya explorados previamente, completitud/latencia asumidas, reproducción solo mismo host/Python y ejecución guiada. No demuestra eficacia de agentes, skills o decisiones actuales.
