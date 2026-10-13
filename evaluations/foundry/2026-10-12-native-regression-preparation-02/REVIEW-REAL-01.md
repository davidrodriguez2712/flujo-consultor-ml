# Revisión independiente de real-01

Fecha: 2026-10-12. Reviewer: agente Codex distinto del autor/runner, `/root/native_real02_review`. Revisión semántica con expected privado; no es revisión humana ni ciega. No se leyeron conclusiones del autor, otros reviews ni documentos presupuestarios; sí ledger y summary de real-01. No se realizaron llamadas de API/red, entrenamiento ni nuevas ejecuciones evaluadas. Solo se escribe este review; no se modifican outputs, criterios, skill, autorización financiera ni estado de promoción.

## Dictamen

**Evidencia parcial de tratamiento, con reservas semánticas y un fallo contractual bloqueante.** L01 resuelve el mecanismo principal correctamente y cumple el wrapper mecánico, pero su cobertura y los campos por hallazgo tienen reservas. L02 sostiene correctamente que el expediente no confirma leakage; su contrato de entrega falla por ausencia del frontmatter YAML delimitado. No debe contabilizarse como caso íntegramente aprobado. El estado `STOPPED_CONTRACT_FAILURE` de summary es coherente con los artefactos.

Solo se revisan dos tratamientos, L01 y L02, con detect-leakage 0.2.0. L03 no fue ejecutado en real-01 y no cuenta como resultado, éxito ni fallo semántico. No hay baseline en este conjunto: no se infiere mejora causal, superioridad de la skill, generalización ni aptitud para promoción. No se hallan los fallos críticos automáticos definidos por los expected en los dos contenidos revisados; esto no elimina los defectos de cobertura ni convierte runtime_success en cumplimiento integral.

## Evidencia revisada y trazabilidad

Fuentes: `package/public/{L01,L02}/case.md` e inputs; `package/reviewer/{L01,L02}/expected.md`; `package/skill/SKILL.md`; `package/workflow.md`; `runs/real-01/{L01,L02}-treatment/` con reportes persistidos, metadata, prompt, result, stdout, stderr y report-contract; ledger/summary. También se inspeccionaron la utility y report-context de cada workspace para contrastar las afirmaciones del reporte con su capacidad real.

Las trazas registran invocación inicial `Skill(acos-eval:detect-leakage)` y contienen el texto cargado. Las copias runtime de la skill son idénticas al paquete; SHA-256 `c2a2440477d9985489b71f4d8c50380ccd7985635d02eab330cfee0f7e5856c4`, coincidente con report-context. Ambas metadata declaran condición treatment y versión documentada 0.2.0. No consta lectura de expected, ejecución de pipeline, entrenamiento, red o delegación en las llamadas observadas.

La recomputación readonly de SHA-256 confirmó los cuatro hashes de inputs de cada reporte, sus prompts y reportes frente a metadata. Cada input de workspace coincide byte por byte con el paquete público. Hashes de reporte: L01 `2690cb9e9f94cb2c7ad51c9a4bf5a4a90642ab0b5644d1f8c5cf9afc96f5afa9`; L02 `2778cf9df083e876436cc251328422eea5bc46b5da28e2591766e0194ba53639`. Esto acredita identidad actual y concordancia con las trazas; no constituye atestación externa inmutable.

Fecha declarada 2026-10-12 correcta frente a started/finished UTC: L01 23:54:27–23:54:52 y L02 23:54:52–23:55:21; corresponde también al 12 de octubre en Lima. Cada traza tiene un único Write de tipo create, contenido idéntico al archivo persistido y originalFile null: no se observa sobrescritura. Stderr vacío; resultados de runtime sin errores ni denegaciones. Ledger registra ocho requests, sin rechazos, committed agregado 0.01022674 USD. Se informa como registro observado, sin decidir suficiencia o renovación de permisos financieros.

## L01: correctitud principal con reservas

**Mecanismo confirmado y fundamentado.** `pipeline.py:2–4` introduce `recovered_kwh` en las features sin filtro temporal. `observations.csv:2–5` muestra cuatro disponibilidades del 9 al 12 de junio, todas posteriores al scoring del 1 de junio. `context.md:3` explica que se determina al procesar la inspección, incluso cuando vale cero. H1 une construcción, disponibilidad y uso: confianza/severidad alta y retirada del scoring son proporcionales. No depende del nombre de la variable ni de la coincidencia con target.

**Historia válida preservada.** H3 reconoce disponibilidad de `history_kwh_90d` el 31 de mayo a las 23:00, anterior al scoring. No la condena por predictividad. El límite sobre split/fit ausentes queda explícito. No se inventan performance ni entrenamiento.

Reservas independientes:

- **Media, cobertura semántica:** la distinción de `fraud_confirmed` como target retrospectivo legítimo está solo implícita al citarlo en H2 y recomendar conservar `recovered_kwh` como dato retrospectivo. Falta expresar que el target posterior de fraude puede evaluar y no es feature. El remedio principal es correcto, pero conservar recovered como outcome no explica por sí solo la legitimidad del target declarado.
- **Media, accionabilidad:** preguntar por reconstruir `recovered_kwh` con disponibilidad histórica verificable no separa con suficiente precisión los recuperos de inspecciones anteriores del recupero intrínsecamente posterior de esta fila. No afirma que esa fuente exista, ni justifica usarlo ahora; aun así, el expected pide fuente y corte previos para una historia alternativa. Conviene explicitar esa alternativa sin sugerir adelantar el mismo dato futuro.
- **Baja, precisión de evidencia:** H3 dice «La ventana de cálculo no está en el expediente». El código de agregación no está, pero el contexto sí suministra duración de 90 días y hechos anteriores al scoring. La frase niega de forma demasiado amplia evidencia disponible. Pedir verificación de implementación productiva es legítimo; presentar como ausente toda ventana es impreciso.
- **Baja, campos por hallazgo:** H3 incluye componente, evidencia/fuente, confianza, severidad y acción, pero omite el campo explícito mecanismo exigido por case/skill. Su evidencia comunica validez temporal, aunque no subsana la omisión formal. Su severidad «no determinada como riesgo» tampoco define una severidad concreta; refleja ausencia de problema, no un riesgo demostrado. El wrapper no comprueba esta obligación.
- **Baja, redacción de H2:** la coincidencia `recovered_kwh > 0` y target se verifica en las cuatro filas. El propio reporte limita confianza, tamaño y capacidad probatoria; no inventa una métrica. Llamarla «no una medición» y asignarle severidad media introduce ambigüedad: es una observación de muestra, no mecanismo adicional ni desempeño medido.

## L02: contenido esencial correcto, entrega fallida

El resumen y Evidencia establecen disponibilidad de features previa a scoring en las seis filas; labels train del 9 de mayo previos al entrenamiento del 1 de junio; scoring de evaluación del 2 de junio y outcomes del 10 usados retrospectivamente. `pipeline.py:3–7` separa particiones y ajusta scaler con train, transformando evaluación sin refit. La única feature declarada excluye target, fechas e identidad. CSV registra tres filas train, tres evaluation y C01–C03 en ambas. El escenario justifica esa recurrencia; no se exige GroupKFold ni se condena split, feature o preprocessing.

Reservas:

- **Media, proporcionalidad semántica:** H1 atribuye severidad baja a recurrencia explícitamente esperada, H2/H3 atribuyen media a limitaciones de proceso y código. Son límites productivos válidos, pero no mecanismos de contaminación sustentados. «Quedan riesgos ... muestra de 6 filas sin métricas» en resumen/final mezcla insuficiencia de evidencia con riesgo de leakage; métricas no aportadas no son defecto del expediente, y no se pidieron. Clasificar por separado observación válida y limitación evitaría confundir al lector.
- **Baja, contradicción parcial:** H2 pide aportar la ventana y Preguntas abiertas pregunta cuál es; contexto ya declara consumo de 30 días previos y sin target. Falta implementación real, no toda información de ventana. H3 dice «Código de split/entrenamiento incompleto»: código de entrenamiento ausente es cierto, pero la separación por partition sí aparece. Labels mostrados ya cumplen el corte; un filtro no observado no demuestra incumplimiento.
- **Baja, cobertura:** no explicita que una señal predictiva fuerte no prueba leakage, ni el límite de generalización a nuevos clientes. Tampoco afirma lo contrario. Recomendar métricas de clientes nuevos y revisar folds excede el escenario demostrado; debe formularse condicionado a un futuro cambio de población o proceso.

**Alta, contrato bloqueante:** `audit.md` empieza físicamente con `skill:`, carece de `---` de apertura y cierre, aunque incluya los valores esperados. `prompt.txt` exige frontmatter YAML al inicio físico; `report-contract.json` registra `frontmatter:missing`. La skill manda listar y entregar todos los campos/formato antes de cerrar. Es un incumplimiento real del deliverable, no una diferencia cosmética que pueda dispensarse en esta revisión. Metadata mantiene runtime_success true pero contract_success/execution_success false; el texto final «Reporte escrito» acredita persistencia, no contrato satisfecho.

Los tres hallazgos L02 presentan los seis campos solicitados. En H2/H3, «mecanismo» describe falta de evidencia, no construcción ilegítima identificada; debe conservarse esa distinción semántica. No se acusa falsamente leakage confirmado.

## Checks y contrato: alcance exacto

En cada caso se observa un único Bash con el comando autorizado de `check_inputs.py`, seguido por salida de hashes, tamaños, nombres de columnas y número de filas. La utility no compara timestamps, hace joins, calcula predictividad ni audita leakage. Los reportes separan honestamente esa ejecución de comparación manual de fechas y lectura de código. Sus conteos 4/6 filas y siete columnas son correctos. No se encontraron checks automáticos inexistentes atribuidos a la utility.

Reconteo independiente por whitespace coincide con report-contract: L01 444 palabras/reporte y 58/final; L02 425 y 73. Las cinco secciones están una vez en ambos. L01 tiene el frontmatter exigido; L02 falla aun con valores correctos. El éxito del wrapper de L01 no valida los campos individuales ni resuelve sus reservas semánticas.

## Recomendación de revisión

Conservar las ejecuciones como evidencia parcial y registrar por separado correctitud esencial, cobertura/campos y contrato. L01: resultado útil con reservas; L02: razonamiento útil con reservas y entrega contractual fallida. No recalificar L02 mediante edición del artefacto observado. Una corrección futura requiere evidencia identificada como nueva; este review no autoriza ejecutarla, no promueve la capacidad y no amplía autorización financiera.
