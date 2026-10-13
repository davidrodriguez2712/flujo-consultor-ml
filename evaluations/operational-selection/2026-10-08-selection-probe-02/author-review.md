# Revisión semántica del autor

Se leyeron las 24 respuestas completas contra task, inputs, expected y rubric. Revisión no ciega; el autor preparó los casos. Los resultados deterministas y esta revisión se mantienen separados. La revisión de otro agente se archiva aparte y no es humana externa.

## Decisiones y razones centrales

Ambas condiciones filtran elegibilidad, mantienen ranking/selección separados, respetan presupuesto/capacidad, no descuentan coste dos veces, eligen vacío cuando maximiza valor y no completan labels ausentes. En E identifican efectos promedio por estrato bajo diseño/supuestos y optimizan point estimates. En F identifican falta de efectos y coste de P, sin convertir ranking en campaña óptima ni aprobar ejecución. No se observó error en los campos evaluados.

Los intervalos adicionales de E son numéricamente compatibles con Wald no pooled declarado y suma de varianzas de estratos independientes. Ver additional-ci-arithmetic.json. Esto verifica aritmética aproximada; no acredita supuestos reales, cobertura simultánea o validez de intervalos postselección. No formaban parte de los expected numéricos.

## Hallazgos localizados

- A/baseline/1, reason: «no tienen incertidumbre estimable» con dos registros. Es una afirmación categórica no sustentada: las métricas del lote conocido son exactas; para generalizar, la incertidumbre podría calcularse bajo supuestos, aunque sea grande.
- A/treatment/2, open_questions[1]: repite la afirmación categórica de incertidumbre no estimable. El tratamiento no elimina este problema.
- C/baseline/1, open_questions[2]: afirma que elevar A a ≥20 cambia el óptimo solo si cabe con otro elemento. Es incorrecto: A solo cuesta 6 y, a valor 20, gana por menor coste frente a BC; con valor >20 gana por valor. No altera la selección correcta para A=13.
- F/baseline/2, reason: «P solo cabría si su coste fuera ≤4» inmediatamente después de hablar de pares. ≤4 vale para P+Q/P+R; P solo permite coste ≤8. Puede ser shorthand de pares, pero la redacción no distingue singleton. F/treatment/2 sí separa ambos límites.
- B/baseline/1 y B/baseline/2, metrics.reason: afirman que R no fue inspeccionado. El input solo acredita label ausente; podría faltar por otra causa. Es una inferencia no respaldada que no afecta las cotas ni la no identificación de recall/lift.
- B/baseline/1, metrics.reason: sugiere posible sesgo de Precision@2 por selección histórica. Para W/Q totalmente etiquetados, 1/2 es el valor exacto del lote. Cualquier riesgo de generalización debe separarse de ese cálculo; no se demuestra sesgo del número actual ni su dirección.
- F/treatment/1, open_questions[2], y F/treatment/2, open_questions[2]: introducen conversión monetaria (efecto×CLV−coste) y reabren el objetivo explícito de clientes salvados. Si se propusiera otro objetivo, cambiaría la tarea; monetizar no es un requisito para maximizar número esperado de clientes salvados. La falta de efecto sigue siendo una brecha válida.

Todas las ramas producen preguntas que reconfirman hechos u objetivos explícitos y comentarios útiles fuera del alcance inmediato. No se asigna un score semántico global ni se compensa un hallazgo con aciertos de otros campos.

## Interpretación

No aparece mejora decisional en dos escenarios ni entre repeticiones: todos los checks están empatados. Algunos motivos secundarios son más precisos en treatment, pero mantiene afirmaciones adicionales discutibles. No demostrar eficacia a partir de la cantidad de texto, de CIs no solicitados ni de un schema válido. Conservar contrato como propuesta local y candidate como conocimiento; sin nueva skill, promoción o integración automática.
