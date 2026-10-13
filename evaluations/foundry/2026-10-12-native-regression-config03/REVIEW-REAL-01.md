# Revisión independiente del contenido de configuración 03

Fecha de revisión: 2026-10-12, zona America/Lima. Reviewer: agente Codex `/root/native_real02_review`, distinto del autor/runner. Conoce la cohorte preparación 02 y su propia revisión anterior; no es ciego ni humano. Solo treatments L01–L03, detect-leakage experimental 0.2.0. No se leyeron conclusiones del autor ni otros reviews, ni claves/env. No se hicieron llamadas API/red, entrenamiento, delegación o reparación de outputs/criterios/skill.

## Dictamen

**Tres ejecuciones y contratos mecánicos conformes; contenido con reservas.** L01 y L02 son útiles y correctos en sus conclusiones principales, con cobertura incompleta y reservas de proporcionalidad. **L03 no se acepta íntegramente en semántica:** expresa incertidumbre pero su condición de confirmación confunde fecha de exportación con mecanismo y su respuesta final transforma falta de evidencia en invalidez. El conjunto no merece aprobación integral por el PASS del wrapper.

Los tres casos terminaron y aquí sí se contabilizan como observaciones revisadas; no equivalen a tres éxitos semánticos. No hay baseline ni control del cambio entre cohortes: no se atribuye causalmente el formato observado al esquema añadido ni la calidad a la skill, no se infiere superioridad/generalización y no se promueve. La revisión no modifica autorización financiera.

## Contrato, trazas e identidad

Se revisaron cases/inputs y expected privados del paquete, skill/workflow, reportes originales y prompt/result/metadata/stdout/stderr/report-contract de las tres ejecuciones; ledger/summary. Se recomputaron hashes readonly, compararon inputs con paquete y contenido de Write con reporte.

| Caso | Palabras reporte/final | Requests | SHA-256 de reporte |
|---|---:|---:|---|
| L01 | 381 / 43 | 4 | `11282c03a9159b897f4bdce725882206b14b53cf51db67080284e981a84cc24d` |
| L02 | 455 / 60 | 4 | `a34e9b44dd3146e81076d0b7b0b5760072d49d6e8b499ed2ab4270f65d9a8763` |
| L03 | 422 / 65 | 4 | `7bb542521ee3c834d9bda2473cfab3515129dc0649a59da0f95d4b714123f4ed` |

Reconteo whitespace coincide con report-contract y respeta 500/80 incluida ruta. Los tres archivos tienen delimitadores frontmatter al inicio físico, seis claves requeridas y cinco secciones una vez. Los doce hashes de inputs, tres prompts y tres reportes coinciden con utility/metadata; inputs son idénticos al paquete. Las tres copias runtime de skill coinciden con el paquete, SHA-256 `c2a2440477d9985489b71f4d8c50380ccd7985635d02eab330cfee0f7e5856c4`. Las trazas registran Skill antes de inspección sustantiva de inputs. L03 primero lee workflow/case/report-context; no procede afirmar que Skill fue literalmente la primera llamada.

Fecha 2026-10-12 válida: L01 inicia 23:58:55 UTC, L02 23:59:15, L03 23:59:50; L03 finaliza 2026-10-13 00:00:09 UTC, todavía 12 de octubre en Lima. No se denuncia discrepancia de fecha por el cambio de día UTC.

Un Write create por caso, originalFile null y texto idéntico al persistido; no se observa sobrescritura. L01/L02 declaran que no pudieron verificar reporte previo mediante Read restringido: esa reserva honesta no prueba violación, y create respalda archivo nuevo. Runtime sin errores/denegaciones, stderr vacío; no se observan acciones fuera de mandato ni lectura de expected.

Un Bash autorizado de `check_inputs.py` por caso. La utility idéntica en los tres produce hashes/bytes/columnas y conteos 4,6,3; no timestamps, igualdad, métricas ni leakage. Los reportes atribuyen fechas y particiones a lectura manual, código a inspección y ausencia de modelos a no ejecución. No se encontraron checks automáticos inventados. Ledger: doce entradas, sin rechazos, committed agregado 0.013749825 USD; dato observado, sin ampliar permisos. Summary `COMPLETED_PENDING_CONTENT_REVIEW` es coherente con runtime/contrato y no resuelve contenido.

## L01 frente al expected

**Correctitud principal satisfecha.** `pipeline.py:2–4` consume recovered; CSV S01–S04 aporta disponibilidad posterior 9–12 de junio frente al scoring del 1 de junio; contexto explica generación post-inspección, incluidos ceros. H1 fundamenta confianza/severidad alta y excluye el predictor del scoring/entrenamiento/evaluación. Reconoce history disponible antes del corte, conserva historia y declara split/fit/CV no auditables. La coincidencia recovered positivo/fraude se limita a cuatro filas y no se usa como prueba del mecanismo ni performance.

Reservas:

- **Media, cobertura:** no declara explícitamente que `fraud_confirmed` posterior es outcome legítimo de evaluación retrospectiva y no feature. El target figura en el indicio, pero no se explica esta obligación esencial.
- **Media, campos:** Hallazgos 2 y 3 no incluyen todos los campos pedidos. H2 comunica feature, disponibilidad y conservar, pero carece de mecanismo/fuente identificada, confianza y severidad explícitos; H3 carece de acción, confianza/severidad y componente/fuente separados. Llamarlos «No hallazgo» o «Indicio» reduce materialidad, pero no cumple por sí solo el contrato por elemento presentado en Hallazgos. El check mecánico PASS no cubre esta omisión.
- **Baja, reconstrucción:** solicita fuente/corte previos correctamente, pero «reconstruirla» no distingue expresamente historia de recuperos anteriores de la misma recuperación intrínsecamente futura. No inventa una fuente ni habilita el predictor actual; la alternativa debe describirse con precisión.

No se observa fallo crítico automático L01. «History válida» se entiende dentro del expediente y sus límites, no como certificación productiva.

## L02 frente al expected

**Obligaciones temporales y operativas sustancialmente satisfechas.** CSV/contexto respaldan feature previa en seis filas, labels train del 9 de mayo anteriores al entrenamiento del 1 de junio, evaluación posterior y outcomes futuros solo retrospectivos. Pipeline separa particiones antes de fit_transform train/transform evaluation; target/identidad/fechas no se usan como features. Tres IDs recurrentes se aceptan para clientes conocidos; no exige GroupKFold, no acusa contaminación ni promete generalización a nuevos. Todos los cuatro hallazgos presentan los seis campos solicitados, aunque algunos describen observaciones válidas o límites, no mecanismos de contaminación.

Reservas:

- **Media, proporcionalidad:** «riesgo medio» por falta de código real y severidades bajas de recurrencia/temporalidad/fit pueden sugerir anomalías inexistentes. Son observaciones válidas y limitaciones productivas, no contaminación demostrada. No constituye falso positivo confirmado: el resumen mantiene ausencia de confirmación y recomendaciones conservan feature/escenario.
- **Baja, precisión:** pregunta la ventana exacta pese a duración 30 días previos y fin antes de prediction documentados. Falta implementación y corte productivo exacto, no toda ventana. Consultar gap/folds por cliente puede servir a otro proceso, pero no es obligación para la operación declarada.
- **Baja, cobertura/señal:** no explicita que alta predictividad no confirma leakage. Dice que sin AUC/resultados no evalúa señal perfecta o igualdad; performance estadística ausente es cierto, pero igualdad en una muestra no requiere AUC ni entrenamiento. No afirma ausencia de leakage por ausencia de igualdad, ni inventa performance.

No se observa fallo crítico automático L02; persisten reservas de calidad pese al contrato conforme.

## L03 frente al expected

**Cumplimiento parcial:** reconoce ventana/disponibilidad/construcción desconocidas y no confirma leakage actual. Pregunta disponibilidad efectiva, ventana, código y versión histórica; no inventa timestamps. Mecanismo de H1 se formula como posibilidad de estado al exportar y confiesa incertidumbre. Reconstrucción histórica con fuente/corte y exclusión provisional hasta documentación son acciones posibles y reversibles; no elimina definitivamente la feature.

Defectos materiales:

- **Alta, criterio semántico incorrecto:** «un conteo con fecha de exportación lo confirmaría como leakage» no basta. Un conteo exportado tarde podría contener solo hechos previos y haber existido al scoring. Para confirmar se requiere demostrar inclusión de reclamos posteriores o disponibilidad efectiva posterior usada ilegítimamente. El reporte no declara con claridad que exported_at no certifica generación/disponibilidad, y propone una condición que contradice esa obligación del expected. No se convierte esta frase condicional en afirmación de contaminación confirmada actual; sí impide aprobar la regla de decisión.
- **Media, cobertura condicional:** «corte ≤ scoring ... reduciría el riesgo» no exige también disponibilidad efectiva previa para el escenario válido. H1 y preguntas solicitan esa fecha, pero falta enlazar ventana previa más disponibilidad como condición conjunta de posible validez.
- **Media, contradicción entre incertidumbre y final:** «la feature no es válida para scoring» es más fuerte que «no puede considerarse válida ... con la evidencia». Lo demostrado es falta de acreditación y No determinable, no invalidez del dato. Riesgo alto/confianza media carece de fundamento para probabilidad alta; severidad de impacto potencial puede ser alta si se distingue de probabilidad. No se aporta una afirmación de seguridad ni mecanismo futuro inventado, pero hay sobreafirmación de invalidez.
- **Media, igualdad y campos:** H2 declara igualdad feature-target «no determinable». En la muestra sí se puede comprobar que no son iguales en todas las filas: 3≠1, 0=0, 2≠0. Esto no excluye leakage ni generaliza. El reporte mantiene esa última cautela correctamente, pero confunde observación determinable y efecto desconocido. H2 también omite componente/mecanismo/fuente/confianza/severidad/acción sistemáticos; indicar tres valores no satisface todos los campos.
- **Baja, outcomes:** no explica que cancelación posterior se usa legítimamente como outcome retrospectivo y no feature. Conservar complaint_count «solo para evaluación retrospectiva» es ambiguo: podría conservarse como descripción retrospectiva, pero no usarlo como predictor indisponible en backtest. Debe precisarse qué uso se recomienda.

No se certifica seguridad ni se acusa un mecanismo confirmado actual; tampoco se considera este caso un éxito semántico completo por declarar incertidumbre. La reserva alta corresponde al criterio incorrecto de confirmación y a la cobertura incompleta de la distinción export/disponibilidad.

## Recomendación

Conservar los tres originales y sus resultados mecánicos. Registrar L01/L02 como útiles con reservas y L03 como revisión semántica no aceptada íntegramente. Separar fallos de contenido/campos del wrapper; una eventual corrección requiere nueva evidencia identificada y autorización aplicable, no edición retroactiva. No alterar expected, skill, estado Foundry ni presupuesto con este dictamen.
