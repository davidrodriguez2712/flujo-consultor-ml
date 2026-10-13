# Ajustes del workflow y preparación de evaluación Foundry

## Alcance aprobado

David aprueba el diseño acotado mediante «aprboado»: actualizar pautas, template y manual generado, y preparar tres cases para detect-leakage experimental0.1.0. Cero llamadas y coste adicionalUS$0. No se modifica la skill canónica ni se cambia su madurez.

## 1. Ajustes aplicados

- Outputs futuros: al menos un artefacto del trabajo posterior con contenido específico, sin contar el propio borrador; títulos solos no bastan.
- Revisión: criterios observables de fuentes/método/corte/límites, separados de métricas o thresholds de rendimiento pendientes. Se acepta contenido distribuido en fields/bullets.
- Formato: Markdown conserva todos los headings requeridos y estado dentro de su sección; JSON conserva campos/tipos sin wrappers. El contrato concreto gobierna el formato.
- Estado: READY/MUST_CORRECT/NOT_DETERMINABLE se refieren a la acción solicitada y sus definiciones del contrato. Una propuesta autorizada puede estar READY con permisos posteriores pendientes. No cambia status del tracker ni autoriza ejecución/gates.
- Dependencias: dato o decisión pendiente → acción concreta limitada.

Archivos actualizados: workflow/execution-and-qa.md, templates/project-and-task.md, contenido del manual en src/acos/render.py y las dos copias correspondientes en src/acos/resources/os. No nueva lógica de estado/schema/checker.

## Comprobación local

Ejemplos del autor de tarea forecast, seguimiento sin task y Markdown con status correcto; contraejemplos de borrador incompleto, output vacío, threshold inventado, prefacio y estado ligado a otra acción. Los tres ejemplos positivos pasan el checker de formato, no se considera prueba semántica automática ni eficacia del agente.

Compilación en directorio temporal: status y nextexit0, integridadOK; template generado idéntico al canónico y manual actualizado revisado. validateexit4BLOCKED por owner/metric/unit/horizon pendientes del perfil fraud inicial. La expectativa inicial de exit3NEEDS_REVIEW fue incorrecta y se corrigió después de inspeccionar el resultado, sin modificar producto para hacerlo pasar. Estado y stdout conservados.

No suite de tests nueva ni cambios en su código. Ejemplos de escenarios expuestos no se presentan como inéditos. Recursos sincronizados para nuevas compilaciones desde este checkout; wheel anterior no se reconstruyó y pilotos existentes no se actualizan automáticamente.

Freeze local17archivos: evaluations/os-workflow/2026-10-10-local-refinement-03/change-manifest-03.json. SHA256 f8980870da4d6a55b4df541bf6a3f0f32866b8201152693f103665bc62a8339b. 564archivos previos intactos. Control local, sin anclaje externo.

## 4. Evaluación Foundry preparada, todavía no ejecutada

Paquete local: evaluations/foundry/2026-10-10-detect-leakage-01/. Usa templates canónicos case/expected/evaluation y snapshot de la única skill existente. No crea candidate nuevo, no duplica una fuente canónica editable ni registra todavía una nueva evaluation en Foundry.

| Caso | Contexto sintético | Pregunta evaluada |
|---|---|---|
| L01 | Cuatro suministros, recupero posterior al scoring incluido entre features | ¿Detecta mecanismo post-event confirmado y conserva historia previa válida? |
| L02 | Seis filas de suscripciones, scoring recurrente de tres clientes, fit solo train | ¿Evita falsos positivos por entidades repetidas o señal predictiva y respeta disponibilidad temporal? |
| L03 | Tres clientes, conteo de reclamos con ventana/disponibilidad desconocidas | ¿Distingue exportación de disponibilidad y plantea preguntas que resuelvan la incertidumbre? |

Conteos/timestamps y ausencia de disponibilidad de L03 comprobados localmente. Orden del preprocessing de L02 inspeccionado, código no ejecutado. Tres fixtures claros iniciales no cubren todas familias de leakage ni demuestran generalización.

Baseline/treatment compartirán el mismo workflowOS snapshot actualizado, tarea, inputs, contrato de reporte y herramientas. Treatment añadirá solo detect-leakage0.1.0. Ambos deben inspeccionar y persistir reporte; runner anterior tools-off no sirve para evaluar esa capacidad completa. La instalación/invocación nativa debe verificarse, no se acredita copiando SKILL.md ni llamando a un modelo con su texto.

cases/* es público para el agente; reviewer/* contiene expected separado. Esa separación de carpetas es preparación, no garantía de aislamiento: el runtime concreto debe limitar accesos antes de run. Protocolo/rúbrica se revisan antes de cualquier output; no se enviará expected al evaluado.

Regla inicial propuesta: mejora conjunta en al menos dos cases, sin regresión ni nuevos fallos críticos. Aciertos de baseline pueden mostrar efecto techo; ninguna regla concede promoción. Autor conoce los expected; revisión independiente pendiente de una persona distinta. Uso experimental supervisado permitido según política del OS; evaluated no significa PASS.

Freeze27archivos: evidence-manifest-01.json. SHA25654f53b2be59f6485f6f7736e57fd291ac78c4c730f5e578b89129b7cfe4fded5. No agente evaluado, APIUS$0, eficaciaNOT_EVALUATED, Foundry canónico intacto.

## Pendientes concretos

1. Revisar y aceptar paquete/expected/regla de detect-leakage.
2. Configurar y verificar runtime, tools, instalación nativa, lectura privada y write scope del reporte. Preparar configuración reproducible con fuente exacta.
3. Acordar reviewer diferente del autor y presupuesto explícito contra esa configuración antes de paidcalls.
4. Ejecutar/revisar comparaciones y decidir si mejorar la capacidad o ampliar cobertura. No promover por preparación o por tres resultados aislados.

Las evaluaciones previas de design-validation0.2.0/0.3.0 no se atribuyen al archivo actual0.1.0; reconciliar versiones es otro pendiente antes de evaluar esa capacidad. No se modificó en este alcance.
