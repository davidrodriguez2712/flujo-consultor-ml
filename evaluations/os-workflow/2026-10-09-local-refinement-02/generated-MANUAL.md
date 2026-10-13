# Manual — Revisión local de contrato de tarea

## Decisión del proyecto

Pendiente de definir

Métrica de éxito: Pendiente; confirmar antes de decidir.
Restricciones: Pendientes de confirmar.

## Situación al inicializar

Etapa: discovery
Objetivo: Comprender contexto, stakeholders, fuentes y restricciones.

Esta sección es una vista inicial. Leer `.acos/state.yaml` o ejecutar `acos status` y `acos next` para la situación vigente.

## Tu siguiente trabajo

1. Revisar PROJECT, profile y estado canónico; resolver preguntas abiertas.
2. Acordar un contrato de tarea y usar las pautas seleccionadas en `workflow/` y `playbooks/`.
3. Producir outputs con fuentes, supuestos y límites; no llenar campos sin evidencia.
4. Ejecutar `acos validate`; corregir bloqueos y obtener revisión humana.
5. Registrar evidencia, reviewer y decisión en `gate_reviews` del state. Solo después de aprobación explícita modificar etapa y registrar el cambio en DECISIONS.
6. Al cerrar sesión, actualizar STATE, MANUAL y TASKS como vistas del estado vigente.

Preparar una propuesta de tarea y ejecutarla son acciones distintas. Dentro del mandato de revisión/propuesta, redactar la siguiente tarea y sus pendientes; detener únicamente las acciones que dependan de permisos, scope o gates todavía no acordados. Un plan vivo actualizado no invalida una copia histórica íntegra ni exige congelar cada borrador. Congelar la versión cuando sustente la aceptación correspondiente; una aceptación previa no cubre alcance nuevo.

Si se solicita un borrador de task, entregar la tarea redactada: objetivo, inputs conocidos, outputs propuestos con contenido esperado, criterios observables de revisión y dependencias que impiden ejecutar. No reemplazarla por una lista de instrucciones para redactarla después. Marcar lo desconocido como pendiente y los outputs/criterios no acordados como propuestas; no inventar owners, permisos ni aceptación. Usar el formato contratado: en JSON, incluir el borrador en los campos permitidos sin texto Markdown adicional fuera del objeto.

## Contrato de salida de la tarea

Acordar consumidor, formato, campos/tipos y texto adicional permitido. El contrato específico controla la salida; los ejemplos Markdown del OS no cambian un pedido de JSON puro. Si se exige un único objeto JSON sin texto adicional, entregar solo ese objeto, sin fences, prefacio ni explicación posterior. Para personas, usar el formato humano acordado.

Comprobar formato y contenido por separado. Conservar outputs inválidos y registrar cualquier corrección como versión nueva autorizada; no quitar wrappers para hacer pasar el original ni repetir llamadas de pago por iniciativa propia. Usar `templates/project-and-task.md` para registrar el contrato pertinente.

## Preguntas de la etapa inicial

- ¿Quién decide y qué acción cambiará?
- ¿Qué fuentes y restricciones existen?

## Outputs requeridos en esta etapa

- context/business_context.md

## Capabilities disponibles

- Pautas/templates del OS; ninguna skill operativa seleccionada.

Ver CAPABILITIES para cobertura parcial y límites. Una skill experimental no es garantía de un entregable.

## Evidencia e historial

Separar documentos vivos (STATE, MANUAL, TASKS y planes actualizables), evidencia congelada y aprobaciones humanas. Antes de solicitar un gate, conservar copias históricas de los documentos vivos que sustentan la decisión y registrar rutas relativas, versión y SHA-256 en un manifest de evidencia. Excluir el estado y sus vistas actualizables del paquete congelado.

Verificar los hashes antes de revisar y entregar. Guardar la aprobación fuera del paquete, vinculada a la ruta, versión y SHA-256 del manifest exacto revisado; referenciarla en `gate_reviews` y DECISIONS. Una corrección conserva el original y registra nueva versión, motivo e impacto sobre la aceptación previa; no hereda automáticamente su aprobación.

Consultar `workflow/execution-and-qa.md` y `templates/delivery-and-handoff.md`. `.acos/manifest.yaml` describe la composición inicial; no sustituye el manifest de evidencia de negocio. Estas pautas requieren ejecución y revisión explícitas: `acos validate` no verifica automáticamente paquetes históricos.

## Reproducción de resultados

Cuando el resultado depende de cálculos o modelos, registrar entorno/dependencias, código/configuración, comandos e inputs versionados. Documentar el recorrido inputs → transformaciones → escrituras → lecturas → cálculo/fit → outputs, con formatos, tipos, precisión, fechas, nulos y orden cuando importen. Respetar las fronteras de serialización originales; no sustituir artifacts leídos por objetos en memoria sin verificar equivalencia.

Acordar antes del nuevo run las keys de comparación, outputs exactos y tolerancias numéricas justificadas. Comparar también métricas y selección/ranking final: datos cercanos no garantizan la misma decisión. Reproducir en un destino nuevo autorizado, conservar originales e intentos fallidos, e investigar la primera frontera discrepante antes de cambiar tolerancias. No reabrir un holdout para seleccionar estrategias durante la reproducción.

Separar reproducción fiel, diagnóstico y corrección del método. Si el original escribe `14.96` con `.1f` y relee `15.0` antes de aplicar `>= 15.0`, repetir ese recorrido debe conservar su selección. Si la reproducción omitió el writer/reader, repetirlos primero en un destino nuevo autorizado. No declarar correcta la selección sobre la fuente cruda ni eliminar el redondeo por defecto. Registrar cualquier propuesta metodológica y su autorización por separado; un método nuevo no reemplaza la reproducción del anterior.

Usar el registro de `templates/delivery-and-handoff.md` y el procedimiento en `workflow/execution-and-qa.md`. `acos validate` no ejecuta ni reproduce el análisis automáticamente.

## QA de cifras y etiquetas

Antes de aceptar o entregar una afirmación material, vincular su cifra a las keys de métrica, método, población y período/cutoff del artifact fuente, con unidad y denominador. Contrastar títulos, leyendas, tablas, texto y logs; un valor existente puede estar atribuido al resultado equivocado.

Identificar períodos por fechas y keys explícitas. Definir “último” dentro del método/población y los períodos elegibles y completos; declarar la fecha concreta y no elegir por posición de fila. Comprobar ventanas, límites y madurez cuando afecten la interpretación. Resolver keys duplicadas o ambiguas antes de aceptar el resultado. Conservar el original y registrar correcciones con fuente, motivo e impacto sobre la aceptación.

Usar `templates/findings-and-qa.md` y `workflow/execution-and-qa.md`. `acos validate` no interpreta automáticamente las etiquetas de los entregables.

## Continuidad

`acos status`: estado, bloqueos y siguiente gate. `acos next`: objetivo, preguntas y outputs del stage actual. `acos validate`: checks y revisión; nunca cambia la etapa.

Antes de invocar una skill comprobar si el runtime la expone. Cambiar profile/composición invalida los hashes y requiere revisar/compilar un workspace nuevo; no hay update automático V1.

## Feedback de capacidades

Registrar observación local (útil/parcial/falló), tarea, versión, evidencia y límites en DECISIONS. Revisar/anonimizar antes de proponer un case o ajuste al Foundry; nunca subir datos ni promover estados automáticamente.
