# Ciclo de vida del proyecto

Este documento define cómo avanzar desde una necesidad de negocio hasta una decisión respaldada por evidencia. El ciclo guía el trabajo, pero no impone una cascada: se puede volver a una etapa anterior, reducir el alcance o cerrar cuando la respuesta ya es suficiente.

## Vista general

```text
Intake y límites
      ↓
Enmarcar la decisión
      ↓
Entender y validar los datos
      ↓
Elegir método y alcance
      ↓
Ejecutar con evidencia
      ↓
Revisar y medir
      ↓
Recomendar, entregar y cerrar
      ↺ volver a la etapa necesaria si cambian los supuestos o falla un gate
```

La pregunta que guía todas las etapas es: **¿qué decisión o acción podría cambiar con el resultado de este trabajo?** Si todavía no puede responderse, primero se aclara el problema; no se empieza eligiendo una herramienta o un modelo.

## Etapas y condiciones de salida

| Etapa | Trabajo | Resultado y condición de salida |
|---|---|---|
| Intake y límites | Identificar quién solicita el trabajo, owner de decisión, deadline, entorno, fuentes y permisos. | Alcance inicial y límites de acceso/herramientas claros. Si falta autorización, limitarse a planificación o datos sintéticos. |
| Enmarcar la decisión | Aclarar problema, usuario/beneficiario, acción posible, población, KPI, horizonte y restricciones. | Brief con pregunta y criterio de éxito revisables. Si no hay decisión ni outcome claro, resolverlo con el sponsor o registrar el bloqueo. |
| Entender y validar datos | Revisar grain, claves, definiciones, disponibilidad temporal, cobertura, calidad y límites de uso. | Contrato/auditoría cuando aplique; se sabe qué permiten y qué no permiten concluir las fuentes. |
| Elegir método y alcance | Elegir una ruta por la pregunta y la evidencia disponibles; definir entregables, aceptación y esfuerzo proporcional. | Tarea ejecutable con método y criterio de salida. Puede ser análisis sin modelo, un experimento, una interfaz o un memo, entre otros. |
| Ejecutar con evidencia | Realizar el análisis, research, experimento, modelado o build autorizado. Registrar fuentes, código/consultas, runs, supuestos y checks pertinentes. | Resultado trazable y reproducible en el nivel adecuado al alcance. Si cambia una definición, volver a framing o registrar una decisión. |
| Revisar y medir | Revisar método, cálculos, robustez, limitaciones y posible impacto con QA proporcional al riesgo. | Findings aceptables o una lista explícita de correcciones, límites y validación pendiente. Si falla un check crítico, no avanzar como si estuviera resuelto. |
| Recomendar, entregar y cerrar | Comunicar qué hacer, por qué, bajo qué supuestos y cómo observar el resultado; registrar aceptación y handoff. | Entrega coherente con la evidencia, responsable del siguiente paso y estado actualizado. |

El nivel de documentación depende de la tarea. No se crean documentos vacíos para completar una plantilla: se persiste lo que debe sobrevivir a la sesión, sostener una decisión o permitir revisión.

## Elegir la ruta de trabajo

El routing se decide en “Elegir método y alcance”. Una tarea puede combinar rutas, pero cada una conserva su gate:

| Ruta | Usar cuando | Gate de decisión |
|---|---|---|
| `RESEARCH` | Hace falta contexto externo, comparar opciones o sintetizar evidencia. | Fuentes pertinentes, calidad y contradicciones declaradas. |
| `ANALYSIS` | Hace falta describir o diagnosticar qué ocurre en datos existentes. | Grain, población, definiciones y denominadores coherentes; límites causales visibles. |
| `EXPERIMENT` | Se necesita estimar el efecto de una intervención. | Estimand y diseño acordados; supuestos, guardrails y límites explícitos. |
| `MODEL` | Un ranking o predicción podría cambiar una acción operativa. | Hay acción/owner de uso, target y horizonte definidos, baseline, validación y métricas alineadas. |
| `BUILD` | Hay que mantener una lógica, pipeline, producto o servicio. | Contrato, aceptación, pruebas/verificaciones y observabilidad acordes al riesgo. |
| `PRODUCT_UI` | Se requiere una interacción nueva o modificada para que alguien complete una tarea. | Usuario, tarea, decisión, reglas y datos están claros antes de decidir wireframe, Figma o build. Ver [`product-ui-and-prototyping.md`](../playbooks/product-ui-and-prototyping.md). |
| `DELIVERY` | Hay que convertir findings revisados en una comunicación o artifact para una audiencia. | Afirmaciones y cifras trazables; audiencia, límites y recomendación claros. |

`PRODUCT_UI` puede combinarse con `MODEL` o `BUILD`, pero no se activa por el mero hecho de producir una predicción. Si los resultados se consumen en un CSV, CRM o dashboard que ya existe, primero se evalúa si la interfaz actual resuelve la tarea.

## Gates transversales

1. **Acceso:** la fuente, identidad y operación están autorizadas para este proyecto.
2. **Decisión:** existe una pregunta y alguien que usará la respuesta.
3. **Datos:** definiciones y calidad permiten responder, o las limitaciones están acordadas.
4. **Método:** la ruta responde la pregunta; no se añade ML, Figma, infraestructura ni automatización por defecto.
5. **Evidencia:** las afirmaciones importantes se sostienen con fuentes y verificaciones pertinentes.
6. **Entrega:** owner entiende recomendación, incertidumbre, limitaciones y siguiente acción.

Los gates no son aprobaciones ceremoniales. Un gate que no se cumple conduce a parar, acotar el resultado o renegociar el alcance, según el riesgo.

## Retornos y decisiones de alcance

- Si cambia la pregunta, población o KPI, volver a `Enmarcar la decisión` y registrar el cambio.
- Si la fuente no contiene la población, ventanas o definiciones necesarias, volver a `Entender y validar los datos`; no rellenar el gap con supuestos silenciosos.
- Si un modelo no altera ninguna acción, cerrar por `ANALYSIS`/`RESEARCH` sin modelar o replantear el uso.
- Si la evidencia apoya una decisión pero no una causalidad, entregar la conclusión descriptiva y proponer medición causal por separado.
- Si surge una nueva interacción de usuario, decidir si activa `PRODUCT_UI`; no asumir automáticamente que se requiere Figma o frontend.
- Si un trabajo descubre una capacidad potencialmente reutilizable, seguir [`capability-lifecycle.md`](capability-lifecycle.md). No confundir ese ciclo con el estado del proyecto.
- Si una tarea se bloquea por permisos, datos, owner o dependencia, actualizar `STATE`/tracker autorizado con el bloqueo y una próxima acción concreta.

## Intensidad del proceso

La intensidad se elige según reversibilidad, alcance e impacto:

- **Ligera:** pregunta acotada y reversible; brief corto, análisis/revisión propia y evidencia comprobable.
- **Estándar:** varias fuentes o transformaciones mantenidas; contratos pertinentes, checks deterministas y revisión independiente de puntos críticos.
- **Reforzada:** decisión sensible, producción o compromiso externo; validación ampliada, reviewer independiente y aprobación humana antes de la acción pertinente.

La intensidad aumenta la evidencia y revisión que hacen falta; no obliga a añadir agentes o archivos. Para responsabilidades, autoridad y cierre, consultar [`execution-and-qa.md`](execution-and-qa.md). Para acceso y memoria de proyecto, consultar [`isolation-and-context.md`](isolation-and-context.md).
