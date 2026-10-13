# Revisión previa de detect-leakage 0.2.2

Fecha: 2026-10-13. Reviewer: agente Codex `/root/native_real02_review`, distinto del autor/runner; conoce preparación y resultados 0.2.1 y cohortes previas. No humano ni ciego. Solo preparación: draft/guías, task, runner, manifest, approval y criterios privados. No se leen outputs nuevos ni se realizan llamadas API/red, delegación, modificaciones de gold/artefactos evaluables/canonical o promociones.

## Dictamen

**Preparación apta para evaluar el micro con gate original; no se encuentra bloqueo material previo.** La compactación mantiene la capacidad esencial y dirige el fallo observado sin alterar caso, criterio o límite. La revisión autoriza un juicio de calidad de la preparación, no concede fondos ni asegura éxito. Mantener el fallo de 0.2.1 intacto y no ejecutar native hasta satisfacer el gate aplicable y saldo.

## Comparación y capacidad conservada

Conteo whitespace del archivo completo: 0.2.0 tiene 719 palabras, 0.2.1 tiene 932 y 0.2.2 tiene 585. El diff no es solo sustitución de versión: reescribe y compacta numerosas secciones, añadiendo una receta de entrega para evitar repetir condiciones. Las dos condiciones siguen siendo obligatorias y explícitas para No determinable; moverlas a Recomendaciones y referenciarlas desde Hallazgos no permite omitirlas.

La nueva guía conserva delimitación de scoring/entrenamiento/población/target; hechos/cálculo/disponibilidad; familias target, temporal, joins, identidad, preprocessing, encoding, selección, resampling y CV; fit train/fold y labels disponibles. Conserva recurrencia legítima de cartera conocida y necesidad de mecanismo frente a señal, solape o identidad. Outcomes retrospectivos siguen siendo labels legítimos; no se transforman features indisponibles en outcomes. Igualdad de muestra observable y ausencia de mecanismo/generalización se distinguen.

Exportación y recálculo posteriores no bastan para demostrar construcción o disponibilidad posteriores. La posible validez temporal exige ventana previa más disponibilidad efectiva y linaje; el mecanismo confirmatorio exige información usada ilegítimamente. La reserva provisional corresponde al owner y se mantiene en resumen/final. La alternativa histórica necesita otra fuente/corte verificables, sin adelantar el mismo dato futuro. Estas instrucciones son generales, sin filas/valores o respuesta específica de L03.

Autoridad, expediente autorizado, persistencia nueva, caller prevalente, campos/fecha/versión y conservación de inputs/reportes permanecen. «No entrenar sin mandato» no amplía acceso ni permiso para ejecutar pipelines; manda el contrato de cada caller. No se concede instalación, gates, producción ni eliminación automática. Metadata Foundry plana con status experimental/version 0.2.2 sigue siendo coherente y no prueba runtime.

## Reservas de regresión y versionado

- **Baja, detalle reducido:** desaparecen menciones explícitas a duplicados, cardinalidad/ventanas de joins y checks encoding/resampling; familias y checks sobre keys/joins/fit siguen presentes. También deja de listar textualmente Probable/Riesgo entre clases, sin prohibirlas. No se demuestra pérdida material, pero la capacidad debe medirse en regresiones, no deducirse de concisión.
- **Baja, severidad:** «sin evidencia de impacto, declarar no estimable» es coherente con no inferir gravedad por exportación. No debe confundirse falta de métricas con falta de impacto temporal demostrado: N01/N03 permiten fundamentar severidad por validez de backtest aun sin performance. La guía no ordena degradar Confirmado a No determinable por no cuantificar métricas.
- **Baja, alcance del patch:** 0.2.2 es razonable como variante experimental de corrección, con ámbito y contrato esenciales conservados. La reescritura es mayor que un parche literal; evidencia de 0.2.0/0.2.1 no valida automáticamente esta versión. No se propone cambiar el estado ni emitir versión estable.

## Protocolo y gold

Task es byte-idéntico al micro-package02 de 0.2.1, incluida aclaración mecánica de delimitadores/fences. Rúbrica privada, expected L03 y expected N01–N03 son byte-idénticos a los de 0.2.1. Control 0.2.0 es idéntico al snapshot anterior; guía micro 0.2.2 coincide con draft. Ningún criterio se relaja para resolver el fallo anterior.

Comparado con runner de micro-package02, el único cambio de código es brazo 0.2.1→0.2.2. Se mantienen requests frescas sin historial/gold/tools, mismo task/modelo, alternancia de orden, cinco repeticiones por brazo, cap 3072 y fechas/versiones suministradas. Manifest recomputado sin discrepancias; approval liga su hash. No se ejecutó runner en este review ni se leyó clave/env. El paquete está preparado; esto no atestigua aún condiciones reales del proveedor.

El gate permanece exacto: cinco tratamientos sin confirmación incorrecta, invalidez falsa o disponibilidad presumida, **más contrato completo**, revisión/comparación y saldo suficiente antes de native. 250 palabras incluyen metadata/títulos/todas las secciones, sin reparación de fences o outputs. Micro textual no prueba native; controls se juzgan con los mismos criterios. Una mejora parcial o cuatro tratamientos favorables no satisfacen 5/5.

Approval declara 0.012 USD de subpresupuesto, prior 0.123365545 y techo 0.15; prior más subpresupuesto es 0.135365545, dentro del techo. Diez requests/cap no garantizan terminar por ese importe; guards deben detener ante falta de saldo, sin retries automáticos. Estos datos documentales no amplían autorización ni constituyen tracker global. Canonical 0.2.0 permanece fuera del scope de escritura de esta revisión; nueva evidencia y decisión aplicable siguen siendo necesarias para cualquier cambio posterior.
