# Engagement simulado con datos reales — priorización comercial retail

Fecha: 2026-10-09.
Estado: diseño aprobado por David el 2026-10-09. La aprobación autoriza preparar el plan; no aprueba gates ni resultados de negocio anticipadamente.

## 1. Propósito y acuerdo inicial

David eligió un engagement independiente de priorización comercial en e-commerce usando Online Retail II. El objetivo es recorrer ACOS de punta a punta con datos públicos reales, producir una recomendación trazable y registrar necesidades de capacidades observadas.

El cliente, el encargo, el owner y la capacidad operacional serán simulados. Las transacciones serán reales e históricas. Independiente significa que no se reutilizan los datos sintéticos, resultados ni decisiones de los pilotos anteriores; no implica un cliente real ni una evaluación ciega de eficacia de skills.

Éxito del piloto: fuente y transformaciones reproducibles, contrato de decisión explícito, evaluación temporal sin leakage, contraste con un baseline, recomendación que respete lo observable y handoff portable. Una mejora del modelo no es requisito para cerrar: recomendar el baseline o declarar evidencia insuficiente son resultados válidos.

## 2. Fuente y hechos verificados

Fuente canónica: [UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii).

La documentación declara 1.067.371 registros de una tienda británica entre el 1 de diciembre de 2009 y el 9 de diciembre de 2011, valores faltantes y un archivo Excel de aproximadamente 43,5 MB. Describe factura, producto, descripción, cantidad, fecha, precio en libras, cliente y país. Facturas cuyo código empieza con c indican cancelación.

Licencia: CC BY 4.0. Atribución: Chen, D. (2012), Online Retail II, UCI Machine Learning Repository, DOI 10.24432/C5CG6D.

Estos son hechos de la ficha, no una auditoría del archivo. Discovery comprobará nombres efectivos de columnas, hojas, cantidades, fechas y semántica. Se conservará el archivo original con URL, fecha de descarga, tamaño y SHA256; ninguna limpieza sobrescribirá la fuente.

## 3. Alternativas y elección propuesta

| Enfoque | Ventaja | Límite |
|---|---|---|
| RFM y ventas históricas | Baseline interpretable, menor complejidad | No estima directamente ventas futuras |
| Predicción de ventas positivas a 90 días y ranking | Permite evaluación temporal contra resultados observados y refleja una decisión concreta | No identifica efecto de contactar ni margen |
| CLV de largo plazo con modelos probabilísticos | Explora recurrencia y valor a mayor horizonte | Añade supuestos de comportamiento y extrapolación con dos años de historia |

Recomendación: segundo enfoque, con el primero como baseline obligatorio. El tercero queda fuera del piloto inicial. El nombre del resultado será ventas esperadas a 90 días, sin presentarlo como CLV completo.

## 4. Encargo de negocio propuesto

Cliente simulado: comercio online de regalos. Owner simulado: responsable comercial; David actúa como reviewer del piloto, sin autoridad sobre clientes reales.

Decisión: al inicio de cada mes, proponer una lista de hasta 100 clientes identificables para revisión comercial, ordenada por ventas positivas esperadas durante los siguientes 90 días.

Capacidad de 100 y horizonte de 90 días son supuestos de diseño, no hechos de UCI. No se enviarán comunicaciones ni se usarán IDs para contactar personas. La salida será una propuesta retrospectiva para revisión humana.

Población propuesta: clientes con identificador y al menos una compra válida en los 180 días anteriores al cutoff. La falta de compras futuras se interpreta como cero ventas observadas durante un horizonte completo, nunca como churn definitivo. Clientes anónimos y nuevos sin historia se reportan como cobertura excluida.

Arquetipos: DIAGNOSE, PREDICT y PRIORITIZE_SELECT. SEGMENT solo como diagnóstico, sin prometer segmentos accionables. No activar OPTIMIZE por tener un Top-K: faltan efectos, costes y una función de utilidad de contacto.

## 5. Contrato analítico

Unidad: cliente y cutoff mensual. Moneda: GBP nominal; no convertir a moneda actual ni extrapolar a otro mercado.

Target propuesto: suma de cantidad por precio de líneas de compra válidas en el intervalo desde el cutoff, incluido, hasta cutoff + 90 días, excluido. Compra válida requiere cantidad y precio positivos y factura no cancelada. La regla final dependerá de la auditoría de códigos y semántica, y se aprobará antes de entrenar.

Esta definición mide ventas positivas registradas: no ingresos netos, beneficio, cash flow ni incremento atribuible a una campaña. Cancelaciones, devoluciones, ajustes, líneas sin cliente y códigos no comerciales se auditan por separado, con volumen e importes. No se borran duplicados solo por igualdad de valores: se necesita una regla justificable.

Features: recency, frequency, monetary y tendencias calculadas exclusivamente con transacciones anteriores al cutoff. Una compra o cancelación futura no puede modificar retroactivamente una feature histórica.

Baseline principal: ventas positivas de los 90 días anteriores; desempate determinista por ID. Clientes elegibles sin compras en esos 90 días tendrán score cero. Comparador secundario: RFM sencillo, con fórmula congelada antes de observar el holdout.

Modelo: una regresión sencilla adecuada a ventas asimétricas, con transformación de target si procede y máximo una alternativa de mayor complejidad. La selección concreta se define después de Diagnosis; no se buscarán modelos hasta obtener mejora.

## 6. Validación y criterios de decisión

Evaluación temporal: desarrollo en cutoffs históricos y período final posterior aislado. En cada fecha de fit, ninguna label de entrenamiento tendrá un horizonte que termine después de esa fecha. Se registrará que disponibilidad inmediata de transacciones es un supuesto retrospectivo: UCI no documenta latencias de ingestión ni correcciones.

Las fechas exactas se fijarán después de auditar cobertura y antes de ajustar modelos o inspeccionar resultados del holdout. Todos los cutoffs evaluables requieren 180 días anteriores y 90 días futuros completos. La parte final incompleta del archivo no se etiqueta como cero.

Compartir clientes entre períodos puede ser correcto porque la decisión propuesta vuelve a puntuar clientes conocidos. No imponer separación por cliente sin cambiar el escenario de generalización. Los horizontes solapados no cuentan como observaciones independientes; se preferirán cutoffs de evaluación separados al menos 90 días cuando la cobertura lo permita y se declarará el número efectivo de períodos.

Métrica primaria: ventas positivas futuras agregadas en el Top-K de clientes elegibles, con K = mínimo entre 100 y tamaño de la población. Reportar la diferencia frente al baseline con la misma población y cutoff. Esta métrica mide calidad retrospectiva del ranking, no uplift.

Métricas secundarias: MAE, cobertura de clientes, fracción de ventas elegibles capturada cuando el denominador es positivo y estabilidad del ranking entre períodos. Diagnósticos: concentración, cancelaciones/devoluciones de seleccionados y desempeño por país o antigüedad cuando los tamaños permitan interpretarlo.

No recomendar modelo por mejorar un único número agregado. Contrastar consistencia por período, concentración en pocos clientes y coste de complejidad. Si se cuantifica incertidumbre, remuestrear a nivel cliente conservando sus períodos y declarar límites de la escasa historia temporal.

No existe umbral de mejora inventado. Antes del holdout, el reviewer aprobará una regla de aceptación basada en los períodos disponibles, utilidad del ranking y estabilidad; una decisión NEEDS_REVIEW o mantener baseline es válida.

## 7. Recorrido ACOS y artefactos

Workspace propuesto: `pilots/retail-valor-90d-publico/`, inicializado con el compiler existente, runtimes Codex y Claude Code, perfil personalizado y snapshots pertinentes. La estructura efectiva se deriva de sus módulos; no copiar el árbol completo del catálogo.

| Etapa canónica | Resultado requerido |
|---|---|
| discovery | Brief simulado, provenance/licencia, fuente congelada, auditoría inicial y preguntas abiertas |
| framing | Población, target, capacidad, horizonte, métricas, alcance y supuestos aprobados |
| diagnosis | Calidad, cobertura, cancelaciones, cohortes, suficiencia de períodos y diseño temporal propuesto |
| execution | Transformaciones reproducibles, baseline y modelo acotado; trazas de features y labels |
| validation | Evaluación congelada, checks temporales, comparación y limitaciones |
| delivery | Decision memo, reporte analítico y ranking retrospectivo ilustrativo |
| handoff | Runbook, manifiesto de resultados, instrucciones de reproducción y feedback local |

`MANUAL.md`, `STATE.md` y `TASKS.md` se personalizan; `.acos/state.yaml` conserva autoridad. Ningún gate se aprueba por existencia de archivos. La aprobación de este diseño permite planificar, no aprobar anticipadamente resultados de negocio.

## 8. Capacidades y Foundry

Consultar el inventario actual, sin fijar una lista de skills por sus nombres históricos. Resolver necesidades de dataset understanding, calidad, features temporales, validación, leakage, ranking y entrega mediante skills disponibles o pautas OS.

Snapshots experimentales se aceptan provisionalmente, con versión, hash, razón de selección y límites. Una capacidad ausente queda como gap y se cubre con un contrato, template, playbook o procedimiento local explícito. No bloquear el piloto esperando una skill nueva.

Registrar tarea, output, fallo esperado/observado y evidencia antes de proponer candidates. Contrastar con fichas existentes; no duplicar automáticamente CLV, ranking o contratos temporales. No promover estados ni escribir en el Foundry durante este piloto.

## 9. Ejecución, límites y revisión

Ejecución local con el tooling existente. Sin llamadas de pago a modelos, sin publicación externa de entregables y sin modificar los pilotos cerrados o el código del compiler. Si aparecen defectos del producto, registrar un expediente y separar su corrección de este diseño.

Comprobar licencia, hashes, calidad, transformaciones, horizonte completo y exclusión de futuro. Conservar comandos y salidas, incluidos fallos; preparar un entorno y runbook reproducibles. Los tests se limitarán a los checks de este piloto y a sus cálculos.

La ejecución comienza tras aprobación del diseño escrito y del plan posterior. Las decisiones de gates siguen revisión humana; aprobación del piloto no equivale a aprobación de un resultado aún no producido.

## 10. Preguntas que debe resolver Discovery

- ¿Qué hojas, columnas y códigos tiene realmente el Excel, y coinciden con la ficha?
- ¿Cómo se distinguen compras, cancelaciones, ajustes y líneas no comerciales?
- ¿Cuánta población y ventas se excluyen por identificadores ausentes?
- ¿Hay suficientes cutoffs con historia y horizontes completos para una comparación defendible?
- ¿Qué limitaciones impone no conocer disponibilidad histórica ni correcciones de transacciones?
- ¿Qué regla de aceptación de ranking puede aprobarse sin observar el holdout?

Si las respuestas invalidan el target o la evaluación, detener Modeling y proponer revisión explícita. No fabricar labels ni modificar la fuente para satisfacer el diseño.
