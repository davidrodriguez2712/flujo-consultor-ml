# Research, impacto y delivery

Este playbook transforma preguntas, evidencia y findings revisados en alternativas de acción y una comunicación útil para su audiencia. No reemplaza la aprobación de negocio ni las políticas de fuentes/destinos del cliente.

## Research

Antes de buscar:

- convertir la necesidad en una pregunta acotada y una decisión informada;
- identificar período, geografía, población, términos y criterios de inclusión;
- priorizar fuentes primarias y documentación oficial cuando estén disponibles;
- distinguir evidencia directa de comentario, interpretación o inferencia;
- verificar fecha, alcance, método y limitaciones de cada fuente.

Comparar fuentes cuando sea posible. Registrar evidencia a favor y en contra, discrepancias y qué no se pudo confirmar. No ocultar contradicciones para hacer una recomendación más simple. Cumplir restricciones de licencia, acceso, retención y confidencialidad.

## Business impact

Vincular un resultado técnico con una acción que alguien puede ejecutar:

1. quién puede actuar y sobre qué población;
2. tamaño elegible y capacidad operativa;
3. mecanismo plausible y outcome esperado;
4. costos de contacto, implementación, oportunidad y riesgo;
5. escenarios base/alto/bajo con supuestos visibles;
6. fuente de cada input, owner y sensibilidad;
7. plan para medir efecto real y criterio para continuar/cambiar.

No convertir lift predictivo en retorno incremental. Separar forecast/model output, asociación observada y evidencia causal. Si no se identifica un outcome o no se puede actuar, reportar la limitación en lugar de inflar el caso de valor.

## Síntesis de findings

Priorizar findings por importancia para la decisión, evidencia, magnitud, alcance y acción disponible. Para cada uno presentar:

- qué sabemos y a qué población/período aplica;
- evidencia o referencia reproducible;
- qué inferimos y con qué confianza;
- qué información sigue faltando;
- implicación y decisión posible;
- siguiente validación si el riesgo no está resuelto.

Una historia ejecutiva puede ser concisa y aun así incluir límites. Poner la decisión en primer plano, explicar por qué importa, qué la respalda y qué haría cambiar la recomendación. Charts deben preservar denominadores, unidades, períodos y fuentes.

## Delivery

Escoger memo, deck, dashboard, query o handoff según audiencia y uso. Antes de entregar, comprobar:

- las afirmaciones y cifras coinciden con los findings y evidencia aceptados;
- totals, períodos, filtros, denominadores y unidades se reconcilian;
- la versión del artifact corresponde a la versión del análisis;
- supuestos, incertidumbre, generalización y limitaciones son legibles;
- la recomendación tiene owner/acción/siguiente paso;
- la clasificación, audiencia, canal y destino están autorizados;
- la revisión humana requerida está completa.

No enviar/publicar por iniciativa propia. El consultor aprueba la versión final y utiliza el sistema autorizado. Registrar un delivery manifest cuando se necesite trazabilidad de proyecto, con referencias al artifact, fecha/versión, evidencias y aceptación.

Si el deliverable introduce una tarea de interfaz para usuarios, decidir si se activa [`product-ui-and-prototyping.md`](product-ui-and-prototyping.md). Una presentación ejecutiva no activa por sí sola la ruta de frontend.
