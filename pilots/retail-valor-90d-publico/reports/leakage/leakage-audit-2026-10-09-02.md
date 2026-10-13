---
skill: detect-leakage
version: 0.1.0
fecha: 2026-10-09
proyecto: retail-valor-90d-publico
inputs:
  - "analysis/run_retail.py sha256:5ebea2b306211a00adaa54fe38de13fd2847096f8dc4338d73678b6cfdcd28a9"
  - "analysis/retail_evaluation.py sha256:262976514fc5dc647d19a1cdf017a32abca0b29e21f307ef74cb5f4f8e235bc1"
  - "reports/validation/development-selection.json sha256:51962b0e32b98fd1dbd7d1f4f3398ca3602b5fb13931a824569ea052f08d3970"
  - "reports/validation/holdout-attempt.json sha256:6b05ecef1110669764027f84563322560b5e61085d8f37743d68d8538b51a41a"
estado: Seguimiento de evaluación; sin reselección por holdout, observabilidad real no determinable.
---
# Auditoría de evaluación final

## Resumen

Extensión del runner conserva aislamiento de la elección: selection congelada con development antes del marcador STARTED; solo método seleccionado y baseline permitido. Caso actual ambos son el mismo baseline, sin entrenar alternativas finales. Auditoría anterior conservada.

## Hallazgos

Alto / No determinable: disponibilidad as-of/correcciones de UCI sin ingestion; mecanismo e impacto documentados en primer reporte. Requiere históricos operacionales, no check estadístico.

Medio / Confirmado: dependencia entre snapshots; no contaminación prohibida en este escenario de clientes conocidos. No intervalos IID ni estimación de generalización a nuevos clientes.

Informativo / Confirmado: código bloquea intentos siguientes y modificación de contratos/selección; decisión usa exclusivamente desarrollo para elegir candidato. `acceptance_decision` solo puede mantener baseline o elegido, aunque otro modelo tuviera outcome superior. Resultado final no redefine features ni ventanas. Join scores/outcomes one_to_one con población idéntica y horizonte completo. Target ausente de scoring inputs, scaler fittrain y ocho features explícitas.

## Evidencia

50 tests pasan, selección freeze timestamp anterior al inicio, hashes fijados en selection-manifest y marcador de ejecución. Historial de Execution conservado como copias de código; runner actual cambia solo para habilitar etapa autorizada. Diagnósticos de concentración/cancelaciones son posteriores a selección y no la cambian. Archivo final contiene rank, ID, cutoff, score y método, sin outcome como criterio.

## Preguntas abiertas

Latencia y revisiones reales, estabilidad de IDs y capacidad comercial siguen no determinables. La distribución global ya fue vista en Diagnosis; no llamar a este resultado completamente ciego.

## Recomendaciones

Usar resultado como benchmark retrospectivo y conservar baseline conforme al contrato. No reevaluar variantes en este holdout. Para nuevo diseño abrir versión/engagement nuevo y nueva evaluación final; para impacto de contacto usar estudio causal. Sin promoción automática de skill.
