# Protocolo propuesto — revisión menos guiada de las pautas del OS

Versión 0.1.0 · Preparación autorizada; **ejecución no autorizada todavía**.

## Pregunta y alcance

¿Añadir las pautas de freeze, reproducción y correspondencia cifra/etiqueta ayuda a revisar expedientes nuevos sin aumentar falsos bloqueos?

Se evalúa revisión y propuesta sobre seis engagements hipotéticos mediante payloads de texto. El agente recibe el objetivo, contexto y artifacts; no recibe la solución, los criterios particulares del reviewer ni un checklist de respuestas por caso. Ambas condiciones reciben el mismo contrato de tarea y formato. Es menos guiado que un ensayo que entrega el error y su corrección, pero el contexto sí contiene definiciones materiales; no es una tarea abierta de consultoría autónoma.

No se evalúa escritura real de archivos, ejecución de pipelines, gates automáticos, ni eficacia de una skill del Foundry. No se ejecutan calls durante preparación.

## Casos y respuestas privadas

| ID | Familia | Engagement | Situación evaluada |
|---|---|---|---|
| E01 | Freeze | Consumo de una flota | Manifest aprobado apunta al plan vivo que cambió; existe copia original recuperable. |
| E02 | Freeze | Consumo de otra flota | Manifest apunta a copia histórica intacta; plan vivo actualizado legítimamente. |
| E03 | Reproducción | Tiempos de atención | Omitir writer/reader cambia casos derivados, aunque valores cumplen tolerancia. |
| E04 | Reproducción | Tickets diarios | Distintos bytes por whitespace JSON; mismo recorrido y resultados semánticos. |
| E05 | Etiquetas/períodos | Entregas puntuales | Cifra de Sur atribuida a Norte; existen fila incompleta y fechas desordenadas. |
| E06 | Etiquetas/períodos | Entregas puntuales | Borrador correcto para Norte; filas posteriores no pertenecen al período elegible. |

Este protocolo y `reviewer/` no se envían al agente evaluado. Los registros de owner/aprobación de los inputs son fixtures: no decisiones reales del usuario. Los cases no contienen datos de clientes ni datos personales.

## Condiciones comparables

- **Baseline:** workflow actual con ablación exclusiva de las tres secciones nuevas. No se presenta como release histórica completa.
- **Treatment:** el mismo workflow con esas tres secciones. No se añaden templates, MANUAL, hints particulares ni outputs esperados.
- Lo demás —tarea, contexto, artifacts, formato, runtime/modelo, configuración y herramientas— debe ser idéntico.
- El treatment aporta más texto; medir tokens/costo como consecuencia del suplemento. El tratamiento conjunto no permite aislar cuál sección causó una diferencia.

`conditions/source.json` registra la procedencia. `verify_preparation.py` comprueba que eliminar el suplemento del treatment produce exactamente baseline y que los payloads se ensamblan solo desde inputs públicos.

## Diseño propuesto de ejecución

Seis cases × dos condiciones × **una repetición propuesta = 12 invocaciones**. Orden por caso alternado: E01 baseline/treatment, E02 treatment/baseline y así sucesivamente. Cada celda usa contexto fresco e independiente; no continuar sesiones ni compartir outputs de otra condición.

La preparación no fija aún runtime, modelo, configuración efectiva o presupuesto. Esos campos están en null en `preparation.json`. Antes de ejecutar se requiere:

1. Aceptar este paquete concreto y sus expected; fijar runtime/modelo, parámetros, presupuesto y límites de output en un registro de ejecución separado que referencia el manifest congelado.
2. Verificar un transporte compatible con la salida común. Los runners temporal/selección existentes usan otros contratos; no se consideran compatibles por existencia.
3. Verificar herramientas deshabilitadas y entrada solo de payload, sin acceso al filesystem, directorio reviewer, expected, protocolo, payload hermano o historial de esta conversación.
4. Registrar argv/payload exactos, versiones, configuración solicitada y efectiva conocida, tiempo UTC y raw outputs. No persistir credenciales. Tokens/costo desconocidos se guardan como null con motivo, no como cero.

No se reutiliza una autorización de gasto de otro trabajo. La ejecución requiere su autorización y presupuesto. Un eventual smoke debe identificarse y conservarse aparte, sin contar como respuesta de eficacia ni reutilizar estos casos como “inéditos” después de mostrar sus outputs al modelo.

## Evaluación prevista de cada respuesta

Formato común: un único JSON, sin fences ni texto extra; `status` en READY/MUST_CORRECT/NOT_DETERMINABLE, `findings` con statement/evidence_paths, `proposed_actions`, `next_step` y `limitations`. READY no aprueba un gate.

Reportar por separado:

1. **Transporte:** runtime correcto, salida nativa disponible, sin acceso no autorizado o mezcla de contextos.
2. **Formato:** JSON estricto, sin keys duplicadas/no finitos, tipos y campos adecuados. No reparar la respuesta para hacerla pasar.
3. **Decisión:** estado esperado del case; registrar falsos bloqueos sobre E02/E04/E06 y errores omitidos sobre E01/E03/E05.
4. **Contenido:** cuatro obligaciones semánticas por case y dos acciones/conclusiones prohibidas, definidas en `reviewer/expected/`. Verificar identidad/valores y soporte de references; existencia de ruta no prueba soporte semántico.
5. **Alcance:** ausencia de aceptación inventada, cambios de criterio o autoridad, extrapolación causal/operativa y promoción de madurez.

Los checks de preparación recomputan el oracle de los fixtures, no evalúan una respuesta de modelo. La implementación de un checker de outputs y una revisión semántica están pendientes antes de ejecución. Equivalentes semánticos se aceptan; no exigir wording exacto ni una solución textual copiada.

Un caso es correcto en contenido si su estado y las cuatro obligaciones están respaldados, sin acciones prohibidas. Formato y contenido permanecen métricas distintas; un diagnóstico tolerante no convierte formato inválido en PASS. No inventar un score compuesto a posteriori.

## Regla de interpretación predefinida

Presentar matriz emparejada por case: baseline/treatment, formato, decisión, cuatro obligaciones y violaciones. Una señal favorable exploratoria requiere más cases correctos en treatment, mejoras en al menos dos familias, ningún nuevo falso bloqueo en los cases coherentes y ninguna nueva violación de alcance. Si no se cumplen esas condiciones, describir resultado mixto, sin ventaja o evidencia insuficiente según los pares; no ocultar fallos bajo un promedio.

Con seis cases y una repetición no se estima variabilidad ni se prueba eficacia general. Si ambas ramas aciertan, el resultado no demuestra beneficio incremental. Antes de recomendar una skill o promoción, obtener evidencia adicional y revisión separada del autor. La preparación/revisión actual la realiza el mismo agente nativo, sin independencia acreditada.

## Fallos, correcciones e integridad

Sin reintentos automáticos. Conservar raw y logs de cada intento. Un error de infraestructura queda separado de una respuesta incorrecta; no reemplazar outputs malos por otra respuesta. Una pareja incompleta se reporta como no comparable; no recalificarla como acierto.

Si se detecta un defecto del case/expected, detener la comparación afectada, conservar versión e intentos y proponer nueva versión con motivo. No modificar expected tras observar outputs ni declarar el mismo case corregido como completamente inédito.

Manifest congelado de inputs/pautas/expected/checks; aprobación y configuración de ejecución fuera del paquete. Precedencia solo registrada localmente, no anclada externamente. No publicar, crear Git, modificar Foundry o llamar modelos por la existencia de este protocolo.
