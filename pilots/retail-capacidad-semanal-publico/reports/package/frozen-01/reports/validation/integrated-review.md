# Revisión técnica integrada — aceptación pendiente

## Resultados comprobados

- Freeze: manifest y copias históricas conservaron SHA-256 tras actualizar plan vivo, STATE, MANUAL y TASKS; aprobación separada y pendiente. Ver freeze-check.json.
- Reproducción: siete archivos originales y reproducidos coincidieron byte por byte en una copia fuera del checkout, mismo macOS y Python 3.13.2. El recorrido respetó escrituras y lecturas CSV/JSON. Ver ../reproduction/reproduction-check.json.
- QA: una copia deliberadamente errónea llamó “último período” al forecast 317,5 de 2011-08-01. La key temporal correcta es 2011-11-28: forecast 556,5, observado 608. Se verificaron tres órdenes de filas y la exclusión de semana parcial 2011-12-05. Ver ../qa/label-check.json y deliberate-error.json. No se modificaron los outputs originales.
- Tests: 153 passed (146 producto + 7 piloto), sin failures. Ver tests.log y tests.xml. TDD: tests de cálculo/runner fallaron antes de implementación; luego pasaron. Durante construcción se corrigió un error de sintaxis, antes del run real y sin cambiar el protocolo.
- Integridad de evidencia anterior: todos los archivos del manifest Handoff retail previo conservaron sus hashes; copia fuente coincidente. Ver previous-pilot-integrity.json.

## Método y utilidad

104 semanas interiores de calendario; dos semanas con cero facturas observadas. Development 30 semanas; final 18. Facturas distintas por semana evitan inflación por líneas repetidas o copias entre hojas; customer_id no es requisito para volumen operativo. No se observaron invoice_id calificantes presentes en varias semanas.

La media de cuatro semanas mejora development frente a semana anterior (WAPE 15,21% frente a 18,40%). Final WAPE 13,15%, MAE 54,33 y bias −37,92 facturas/semana. No se comparó baseline en final; no se estima staffing ni impacto causal.

## Límites de la revisión

Revisión nativa guiada; no independiente ni comparación control/treatment. Las pruebas son ejecutadas explícitamente, no automatización adicional de acos validate. Datos históricos previamente explorados en otro encargo, sin holdout completamente ciego. Latencia cero y completitud del calendario interior son supuestos. Desempeño actual y entre plataformas no verificados. No se instalaron ni evaluaron skills.

No hay blockers técnicos detectados en el alcance acotado; la aceptación de negocio/gates sigue pendiente y el uso operativo carece de inputs suficientes. La autorización del ensayo no constituye aceptación de sus resultados.
