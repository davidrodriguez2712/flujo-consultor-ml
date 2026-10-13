# Plan de análisis

Ver protocolo fijado en analysis/protocol.json y copia histórica en reports/protocol/frozen/. Filtrar Reino Unido, filas con quantity y unit_price positivos, invoice_id presente y no cancelación C. Contar invoice_id distintos por semana calendario; no requerir customer_id.

Excluir semanas de frontera parcial; completar calendario interior con cero facturas observadas, conservando la limitación de completitud. Forecast de una semana a partir únicamente de semanas completas anteriores. Development 2011-01-03 a 2011-08-01 exclusivo; final 2011-08-01 a 2011-12-05 exclusivo. Seleccionar por WAPE de development, empate a favor de baseline. No evaluar challengers ni retunear final.

Datos ya explorados en otro encargo: no afirmar holdout completamente ciego. El runner registra estrategia antes de generar resultados finales. Fuentes, código y comandos se documentan para reproducción con fronteras CSV/JSON idénticas.
