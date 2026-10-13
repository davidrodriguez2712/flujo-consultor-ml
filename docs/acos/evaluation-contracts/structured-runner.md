# Runner temporal con salida estructurada

Runner `0.2.0`; schema `0.1.0`. Utilidad de evaluación desde el checkout: no añade comandos al paquete `acos` ni instala capacidades en el Foundry.

## Uso

```sh
.venv/bin/python scripts/evaluations/temporal_runner.py \
  --payload-file ruta/payload.txt \
  --output-dir ruta/nuevo-intento
```

Requiere Claude CLI autenticado y las dependencias del entorno del proyecto. El destino debe ser nuevo; un intento anterior no se sobrescribe. Antes del call comprueba que el schema versionado coincide con el validador. El payload debe estar aprobado y no contener expected. El runner no recibe ni consulta expected.

El schema común define campos, tipos y enums; no fija IDs particulares, respuestas correctas ni una aprobación de gate. Claude entrega `structured_output` separado del texto `result`, según su [documentación oficial](https://code.claude.com/docs/en/headless#get-structured-output). El schema usa draft-07, conforme a la [documentación de structured outputs](https://code.claude.com/docs/en/agent-sdk/structured-outputs).

## Tres comprobaciones independientes

- `runtime_success`: exit 0 y envelope nativo de éxito.
- `schema_conformant`: objeto nativo conforme al modelo Pydantic estricto. Incluye controles locales adicionales de IDs únicos, texto no vacío y Unicode válido; no equivale exclusivamente a conformidad con el JSON Schema nativo.
- `content_validation`: permanece `NOT_RUN`. El checker externo compara IDs, clasificación temporal y gate con expected privado. Razones y preguntas requieren revisión semántica separada.

También registra `model_matches`; una ejecución con modelo desconocido o diferente no satisface el check técnico. Código 0 exige runtime, validación local, modelo y versión CLI comprobados; 4 indica fallo de esos controles; 2, entrada u operación inválida.

## Evidencia y límites

Guarda payload, schema, request y argv, raw/stdout exactos, stderr, texto opcional, objeto estructurado y metadata con hashes, duración, modelo reportado, turns y coste reportado por CLI. Este coste no acredita facturación. La configuración solicitada queda registrada; lo no confirmado por el envelope se conserva como desconocido.

No sustituye un objeto ausente por `result`, no repara JSON y no reintenta calls. El runtime puede efectuar reintentos internos de generación estructurada; dos invocaciones CLI no prueban dos requests de API. Un objeto inválido se archiva sin alterarlo; escapes JSON permiten conservar Unicode inválido y registrar su rechazo. Si solo el texto opcional contiene Unicode inválido, se guarda en `result-escaped.json` con finding, sin invalidar un objeto estructurado válido.

Los hashes prueban integridad local; no dan un anclaje temporal externo. No ejecuta herramientas de consultoría, aprueba gates ni promueve capacidades. La reproducción requiere conservar los inputs y versiones antes de llamar y verificar su integridad después.

## Primer check nativo

Ver [informe del check técnico](../validation/2026-10-07-structured-runner-v02-report.md). Se reutiliza el case E de una ronda cerrada para comprobar transporte y validación, sin reinterpretar su eficacia.
