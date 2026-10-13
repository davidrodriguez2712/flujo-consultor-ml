# Protocolo — entregar un task concreto

## Pregunta y alcance

¿Añadir la pauta de borrador concreto mejora que el agente entregue una tarea utilizable en casos nuevos, sin inventar acuerdos ni imponer un task cuando no se pide? Propuestas textuales únicamente, no ejecución analítica, herramientas, permisos reales o gates. Datos/contextos sintéticos; tres casos de draft y un control. No simulaciones de negocio con datos reales ni evaluación de Foundry.

D01 forecast de ventas para reposición, D02 anomalías sin labels, D03 evaluación RAG, D04 tres acciones de seguimiento sin task. Todos tienen expected READY en el alcance de preparación autorizado; las dependencias limitan ejecución posterior, no preparación. No se deriva su estado del tipo de problema.

## Comparación

Baseline snapshot anterior al párrafo de task concreto. Treatment mismo workflow más ese único párrafo; eliminación exacta debe recuperar baseline. No exponer templates/MANUAL/ejemplos/expected/protocolo. Contract y task identical dentro de par. JSON en D01/D03/D04, Markdown en D02, con checker0.2.0 común a ambas ramas. El checker no es tratamiento. Más texto puede aumentar coste: registrar tokens/usage sin atribuir efecto exclusivamente semántico del texto.

Cuatro casos × dos ramas × una repetición propuesta = ocho invocaciones. Alternar orden: D01 baseline/treatment; D02 treatment/baseline; D03 baseline/treatment; D04 treatment/baseline. Proceso/cwd nuevos, no tools, sesión ni contexto compartido. Runtime/modelo/configuración/gasto sin fijar. Smoke técnico separado, si se propone, no es evidencia de eficacia ni usa estos casos.

## Criterios antes de outputs

Expected privados incluyen seis obligaciones por draft y cuatro por control, tres prohibiciones por caso. Rúbrica acepta equivalencias sin exigir campos/frases particulares. Evalúa contenido específico, no presencia de headings. Al menos un output futuro tiene contenido utilizable; el propio borrador no cuenta como output del trabajo posterior. Se permiten propuestas explícitas de outputs/criterios/rutas, no aceptaciones inventadas.

Reportar transporte/aislamiento, formato, estado, concreción, otras obligaciones, prohibiciones, afirmaciones materiales adicionales y referencias. Existencia no equivale a soporte. Content PASS con estado y todas obligaciones, sin prohibiciones ni afirmaciones materiales falsas/desviaciones. Formato inválido permanece FAIL aunque diagnóstico manual reconozca contenido. Raw sin reparar ni retries automáticos. No score ponderado ni porcentaje de obligaciones agregado entre cases.

Señal favorable exploratoria: improvement en cumplimiento conjunto (formato+content) en al menos dos de D01–D03, sin empeorar cumplimiento conjunto en otro case, D04 cumple contenido en ambas ramas, sin nuevos falsos bloqueos ni violaciones de alcance. Si no: mixto/sin ventaja/insuficiente según pares. No se concluye eficacia general con cuatro cases y una repetición; empate no prueba mejora. Con defectos de preparación, declarar cobertura incompleta y no emitir señal favorable sobre plan completo. No cambiar regla/expected después de respuestas.

## Integridad, novedad y review

Payloads solo desde fuentes públicas. Checks locales ejercen descripción numérica de metadata y fixtures; no entrenan ni puntúan agentes. Manifest de preparación congela inputs/expected/pautas/checks. Aprobación del paquete y configuración fuera del freeze, precedencia local no anclada externamente. No recuperar oracles privados desde el runtime.

Casos nuevos respecto de expedientes anteriores, pero el autor conoce el fallo T05 y diseñó esta prueba en respuesta a él. No revisión independiente/ciega ni muestra representativa de consultoría. Rúbrica/juicios/citas deben quedar visibles para revisión humana. Un case expuesto al modelo ya no se declara inédito en retry o versión corregida. Defectos posteriores conservan intentos y bloquean comparación afectada; no reparar expected para mejorar resultados.

Preparación APIUS$0. No ejecutar hasta revisión de paquete, configuración/versiones/aislamiento y autorización nueva de gasto con límites ligados a manifest. Ningún presupuesto previo se transfiere. No modificación de producto/Foundry/promociones ni llamadas por la existencia de este protocolo.
