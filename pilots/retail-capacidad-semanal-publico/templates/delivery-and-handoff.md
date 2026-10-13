# Plantillas de delivery y handoff

Usar cuando hace falta identificar lo que se comparte, cómo se reproduce o quién lo opera después. Para una consulta puntual sin artifact persistente, basta el registro de decisión aplicable.

## Manifest de delivery

```markdown
# Delivery manifest — [proyecto/paquete]

- ID del paquete / versión / fecha / preparado por:
- Destinatario y owner:
- Decisión/acción habilitada:
- Canal y permiso de distribución:

## Contenido
| Artifact | Ruta/link y versión | Propósito | Evidencia/fuente | Owner |
|---|---|---|---|---|
| | | | | |

## Integridad e historial
- Manifest de evidencia (ruta relativa / versión / SHA-256):
- Archivos congelados: rutas relativas y SHA-256; para copias, indicar ruta de origen.
- Documentos vivos excluidos del freeze:
- Resultado de verificación de hashes / fecha / responsable:
- Paquete anterior, si existe una corrección:
- Motivo, archivos cambiados e impacto sobre la aceptación previa:

## Reproducción y límites
- Registro de reproducción (ruta / versión / resultado / límites):
- Cómo reproducir/actualizar:
- Datos, período y definiciones:
- Supuestos, exclusiones y limitaciones:
- Qué no incluye este paquete:
- Elementos no probados o pendientes:

## Operación (si aplica)
- Owner operativo:
- Cadencia / monitoreo / threshold:
- Acción ante error o drift:
- Revisión/override humano:
- Dependencias y costo recurrente:

## Cierre
- Registro de aprobación separado (ruta / reviewer / fecha / estado):
- Manifest exacto aceptado (ruta / versión / SHA-256):
- Alcance aceptado, límites y decisiones pendientes:
- Decisiones registradas en:
- Accesos retirados/transferidos si aplica:
- Retención/eliminación acordada:
- Próxima acción, responsable y fecha:
```

El manifest de evidencia enumera los archivos congelados; no se incluye a sí mismo ni incluye la aprobación. Cerrar el manifest antes de calcular su hash. Una corrección conserva el paquete original y registra una nueva versión; requiere revisar la aceptación afectada. Los documentos vivos pueden evolucionar sin cambiar las copias históricas. Procedimiento completo: [`../workflow/execution-and-qa.md`](../workflow/execution-and-qa.md).

### Registro de aprobación separado

```markdown
# Aprobación — [ID del paquete / versión]

- Manifest revisado (ruta relativa / versión / SHA-256):
- Verificación de hashes (resultado / fecha / responsable):
- Reviewer / decisión humana / fecha:
- Alcance aceptado y límites:
- Estado: pendiente / aprobado / requiere corrección / bloqueado
- Registro de decisión o gate relacionado:
```

Completar con una decisión humana observada; un template rellenado por un agente no constituye aprobación. Si el paquete cambia, conservar este registro vinculado a la versión original.

## Registro de reproducción

Usar para resultados que dependen de un proceso ejecutable. Completar solo las fronteras y checks pertinentes; preservar el run original y reproducir en un destino nuevo autorizado.

```markdown
# Reproduction record — [paquete / run]

- Pregunta/resultado que se reproduce:
- Run original / manifest y SHA-256:
- Código/configuración y versiones de inputs:
- Runtime / dependencias fijadas / plataforma:
- Seeds, recursos y fuentes conocidas de no determinismo:
- Comandos en orden / directorio de ejecución:
- Destino nuevo de outputs:

## Recorrido y fronteras de serialización
| Paso | Input consumido | Transformación/comando | Escritura → lectura | Formato, writer/reader y opciones | Esquema, precisión, nulos, fechas, keys y orden material |
|---|---|---|---|---|---|
| | | | | | |

## Criterios acordados antes del run
| Output/check | Keys y alineación | Comparación exacta o tolerancia con unidades | Motivo e impacto en la decisión |
|---|---|---|---|
| | | | |

## Resultado
- Integridad de fuentes/código y entorno:
- Comparación por frontera (esquema, keys, filas, valores):
- Comparación final (métricas, ranking/selección y desempates):
- Estado: reproducido / reproducido con límites / discrepancia / bloqueado
- Evidencia y logs de ambos runs:
- Primera frontera discrepante / causa identificada o pendiente:
- Corrección y nuevo run, conservando el intento anterior:
- Cambios de criterio justificados y decisión humana, si existen:
- Alcance reproducido, límites y pendientes / reviewer / fecha:
```

Respetar las escrituras y lecturas originales aunque los datos en memoria parezcan equivalentes. Definir la comparación según el uso: tolerancia numérica no reemplaza verificar la decisión final. El procedimiento está en [`../workflow/execution-and-qa.md`](../workflow/execution-and-qa.md).

## Nota de handoff de sesión

```markdown
# Handoff — [proyecto / fecha]

- Objetivo y etapa actual:
- Decisión pendiente:
- Estado y último gate alcanzado:
- Qué se completó (con links/versiones):
- Evidencia revisada (manifest / versión / SHA-256, cuando aplique):
- Registro de aprobación y límites de aceptación:
- Documentos vivos actualizados y copias históricas conservadas:
- Supuestos, límites y dudas:
- Cambios realizados y archivos afectados:
- No hacer / restricciones:
- Próxima acción concreta:
- Owner entrante:
```

No incluir secretos ni trasladar información a otro proyecto. Ubicar este handoff en el espacio autorizado del proyecto.
