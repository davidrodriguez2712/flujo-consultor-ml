# Revisión parcial de 0.2.2 antes de completar muestras

Fecha: 2026-10-13. Reviewer: agente Codex `/root/native_real02_review`, distinto del autor/runner; conoce objetivo y rondas previas, no humano ni ciego. Fuentes: siete outputs emitidos y SSE, ledger/summary, task/guías, rúbrica y expected privados, regresiones N01–N03 con inputs/report-context/skill/reportes. No API/red, delegación, reparaciones ni cambios de criterios, guía/canonical o promoción.

## Dictamen y gate

**Los cuatro treatments emitidos son aceptables en contenido y contrato; no se encuentra un fallo que haga imposible el gate.** La evidencia permite completar las tres muestras pendientes previstas —B4, B5, T5— con mismo task/modelo/cap/guías, paquete nuevo identificado, saldo y guards aplicables. No repetir las siete respuestas existentes. Esto es recomendación de calidad, no nueva autorización financiera.

**Gate aún no satisfecho:** solo hay cuatro treatments y tres controls emitidos. Native L03 no está habilitado hasta quinto treatment aceptable, cinco controls observados, revisión completa y saldo suficiente. No se sustituye 5/5 por 4/4, ni se usa una parada local como respuesta del modelo. Las regresiones no sustituyen muestras faltantes del micro.

## Matriz del micro emitido

| Muestra | Palabras wholefile | Contrato ≤250 | Contenido esencial | Reserva |
|---|---:|---|---|---|
| B1 0.2.0 | 247 | PASS | Parcial | Riesgo/severidad altos por brecha, mecanismo hipotético y sin condición confirmatoria explícita. |
| T1 0.2.2 | 227 | PASS | Aceptable | «No cumplida» debe entenderse no acreditada, no imposibilidad demostrada. |
| T2 0.2.2 | 248 | PASS | Aceptable | Pregunta split/preprocessing fuera del expediente acotado. |
| B2 0.2.0 | 194 | PASS | Parcial | Brechas/validez conjunta correctas; falta condición explícita de confirmación y severidad/confianza. |
| B3 0.2.0 | 227 | PASS | Parcial | Riesgo alto y bloqueo sobredimensionados; pide familias ausentes y no explica condición confirmatoria. |
| T3 0.2.2 | 240 | PASS | Aceptable | «Señal» no inferible por tres filas se interpreta estadísticamente, no como negar observabilidad de igualdad. |
| T4 0.2.2 | 201 | PASS | Aceptable | «Exportación ... no prueba nada» es demasiado amplio; no prueba disponibilidad/estado del scoring. |

Todos los emitidos tienen frontmatter físico, seis campos del micro con versión/fecha 2026-10-13/modo guia_textual adecuados, los tres inputs nombrados y cinco secciones. Un único artifact sin fences o texto externo; no se exige hash de inputs al modelo textual. Outputs coinciden byte por byte con text_delta SSE y terminan end_turn. Ninguno se trata como invocación native.

**B4 no emitido:** output vacío preservado no constituye respuesta LLM, fallo semántico, incumplimiento de 250 palabras ni cuarto control observado. No existen B5/T5 en este lote. Summary registra siete transport_success y el intento B4 false por parada; se conserva esa diferencia entre intento local y request proveedor.

## Fundamentación de los cuatro treatments

Los cuatro mantienen No determinable sin afirmar invalidez, seguridad o disponibilidad previa. Citan contexto/diccionario, identifican ventana/disponibilidad/construcción faltantes y no usan exportación para confirmar mecanismo. Piden linaje/versión histórica/código y disponibilidad; no prometen que aumentar filas resuelva la brecha.

Todos expresan ambas condiciones: confirmar información posterior usada como predictor o disponibilidad posterior tratada como accesible; posible validez exige conjuntamente ventana previa, disponibilidad efectiva al scoring y linaje. Las expresiones abreviadas «información posterior usada» se leen dentro de Hallazgos de complaint_count propuesto como feature; no se interpretan como condena del target retrospectivo legítimo. No se exigen frases idénticas al gold.

Acción provisional queda bajo owner y no transforma complaint_count en outcome. Severidad no estimable separa incertidumbre/impacto; no la deriva de exportación tardía. T1/T3/T4 distinguen alta confianza en brecha de confianza en leakage; T2 baja confianza en ambas direcciones no inventa evidencia. Referenciar Recomendaciones desde Hallazgos evita repetir condiciones y cumple contenido por conjunto del reporte.

Reservas menores no activan defecto de gate: en T1/T4 las condiciones «no cumplidas» significan ausencia de evidencia aportada, como aclara la incertidumbre; no se presumen falsas en producción. T2 pide split innecesario y no pregunta disponibilidad otra vez en Preguntas, pero la solicita en resumen/condiciones/acción. T3 declara outcomes solo retrospectivos correctamente. T4 identifica snapshot y código como fuentes de cambio sin afirmar que una sola fuente, por existir, baste: su condición conjunta permanece explícita. La frase «export no prueba nada» no borra las fechas observadas ni altera mecanismo. No se reparan estos textos ni se relaja criterio.

Controls se juzgan igual: no confirman contaminación ni certificar seguridad, pero omiten condiciones de confirmación y separan peor severidad/autoridad. No se contabilizan como éxitos semánticos íntegros solo por cumplir forma. En B1/B3 «bloquear» expresa consejo más fuerte que reserva al owner; no se observa acción externa realizada. No se atribuye causalmente esta diferencia descriptiva a la versión ni se concluye eficacia general.

## Regresiones textuales N01–N03

Cases/inputs son byte-idénticos a 0.2.1; expected N01–N03, L03 y rúbrica micro permanecen idénticos. Los doce hashes de inputs consignados coinciden con recomputación readonly. Copias runtime skill coinciden con draft 0.2.2; report-context declara textual_guide_not_native. Fechas de reporte son 2026-10-13. No hay trazas locales started/finished/result final para atestiguar fecha/utility/final≤80/ausencia de sobrescritura independientemente del coordinador; son límites de revisión instrumental, no fallos semánticos inventados.

| Caso | Palabras | CSV real filas/columnas | Contenido |
|---|---:|---:|---|
| N01 | 399 | 3 / 6 | Disponibilidad tardía confirmada, historia/outcome preservados. |
| N02 | 468 | 4 / 7 | Identidad y recurrencia válidas, fit train-only y temporalidad correctos. |
| N03 | 476 | 4 / 5 | Fit global contaminado confirmado, corregir fit sobre train. |

N01 conecta selección de payment_sum_previous_day, scoring 1nov 08:00 y primer acceso 2nov 03:00; no confunde period_end pasado con acceso. Retira valores indisponibles y exige fuente histórica real/corte bajo owner; no backdating. Target futuro es outcome válido. No repite el conteo falso de siete columnas anterior: reporta solo tres filas, correcto. Magnitud no estimable no diluye Confirmado ni negar impacto sobre validez de backtest.

N02 acepta client_code conocido, cartera recurrente, labels maduros y transformaciones ajustadas solo en train. No convierte el año no literal del ajuste en condición que invierta el escenario: pide corroborar producción sin condenar expediente. Severidad no aplicable para observaciones válidas, recomendaciones proporcionales y clientes nuevos como eventual escenario diferente. No impone GroupKFold ni elimina identidad.

N03 demuestra fit sobre toda tabla antes de particionar; R3/R4 futuros influyen en scaler y no queda evaluación reservada. Mantiene amount temporalmente legítimo, labels retrospectivos, separación previa/fit train-only/transform evaluation y CV solo condicional. Efecto estadístico desconocido no oculta mecanismo confirmado.

Tres reportes con campos/secciones, hashes y límite700 observables; N01 añade modo frontmatter y N02/N03 explicitan textualidad en cuerpo. Ninguno afirma Skill/plugin nativo verificado. Los únicos conteos declarados son correctos; utility real solo sirve hashes/conteos y comparaciones/orden se atribuyen a lectura. Sin stdout de esas ejecuciones no se certifica comando exacto, guards o todos los claims de ejecución. No se emite PASS contractual native; evidencia de contenido/artefactos es aceptable.

## Parada y continuación condicional

Ledger contiene siete requests proveedor, coste 0.0085205 USD y un rechazo local por presupuesto: quote 0.004633375. Con subpresupuesto 0.012, el remanente local 0.0034795 era inferior a la reserva; bloquear B4 antes del proveedor es coherente y no indica truncación ni retry. Saldo aritmético del estudio: prior 0.123365545 más coste = 0.131886045; techo 0.15 deja 0.018113955.

Un subpresupuesto nuevo 0.009 para únicamente B4/B5/T5 cabe aritméticamente en ese saldo, pero reservas/coste real deben gobernar la ejecución; no garantiza completar. La partición de lotes y revisión intermedia se deben declarar en el review final: cinco controles/tratamientos no serán una secuencia ininterrumpida. Se mantienen misma comparación, gold y gate. Si la muestra restante falla, preservar el fallo y detener native; esta revisión parcial no lo prejuzga ni concede aceptación canónica.
