# Ronda02 manual — ejecución pendiente de aprobación

## Alcance y presupuesto

Configuración01 y ronda01 intactas. Ronda02 usa un smoke con plantilla literal y el mismo schedule de ocho casos. Ningún otro input, criterio, runtime, prompt neutral o checker cambia. La plantilla comprueba transporte/formato; no mide eficacia.

El límite acumulado de task-draft-01 es US$0.10. La ronda01 consumió US$0.000241 por usage conocido; el máximo nuevo es US$0.099759. No hay retries automáticos ni transferencia de saldo de estudios anteriores. Verificar hash de la ronda01 y ledger (una entrada, coste conocido exacto) antes de fijar el proxy a US$0.099759. Este presupuesto solo se habilita tras aprobación de ejecución vinculada al manifest02; aprobación de preparación no autoriza paidcall.

## Preflight antes de credencial/proxy

Verificar preparation39, configuration01 y02, run01 y snapshots listados contra código activo; excluir pycache. CLI/version/flags exactos; cualquier cambio detiene. Aprobación humana de paquete39 válida; nueva aprobación de ejecución y presupuesto vinculada al SHA256 de execution-manifest-02.json mediante require_approval. No usar approval de configuration01.

Leer solo ANTHROPIC_API_KEY mediante parser seguro de.env, sin source, imprimir, copiar/hash de secreto. CLI usa placeholder; proxy local la credencial. Guardar raw sin alteración y escanear secreto exacto solo en memoria antes del freeze.

## Schedule y parada

Validar ocho celdas únicas D01–D04×baseline/treatment y order idéntico a configuration01. Una única invocación smoke + ocho respuestas; guard explícito len(proxy.budget.entries)<9 antes de cada invoke; no solicitudes10–13 aunque helper tenga ceiling13. Proxy max_requests9, cap8192, presupuesto US$0.099759. invoke configura un request adicional por invocación. Prompt TRANSFER_SYSTEM común explícito.

Smoke debe cumplir runtime_success, usage conocido, un request, end_turn y checker Markdown READY sin refs. Si falla, parar sin retry. Benchmark: errores de formato se conservan/puntúan, sin repair/retry; infraestructura, modelo, usage, presupuesto o truncación detienen. Persistir ledger/metadata cada call. Procesos/cwd nuevos sin tools/MCP/settings/skills. No se crea sandbox OS nuevo.

## Revisión y cierre

Expected privados solo al checker local después de respuesta. Revisar obligaciones/citas semánticamente sin exigir frases o claves exactas; formato separado, no aceptar gate ni promocionar Foundry. Comparación por cuatro pares con regla congelada y revisión del autor no independiente/ciega. Pares incompletos no producen señal favorable completa. Registrar coste nuevo +US$0.000241 del estudio y +US$0.04153488 de otros estudios separados. Freeze e integridad sin retocar ronda01 ni documentos históricos.
