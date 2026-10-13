# Control del contrato de reportes nativos

Fecha: 2026-10-12. Alcance: transporte y coordinador local de las evaluaciones Foundry. Continuación autorizada del pendiente de contrato, sin nuevas llamadas pagadas ni cambios de madurez.

## Problema y causa

La regresión nativa anterior persistió L01 con 528 palabras frente a un límite de 500 y `skill_version` en lugar de la clave requerida `version`. El transporte reconocía ejecución, usage e integridad de inputs, pero no comprobaba el contrato del reporte. El coordinador avanzaba únicamente con `runtime_success`.

El contenido correcto de un diagnóstico y el éxito técnico del CLI no garantizan que el artefacto entregado cumpla su contrato. Las omisiones semánticas de hallazgos secundarios siguen requiriendo revisión independiente.

## Diseño aplicado

Cambio acotado al flujo existente: check mecánico readonly después de la ejecución, separado de runtime y revisión semántica. Persistir evidencia del prompt y del resultado de ese check; detener secuencia y presupuesto cuando falle, conservando el reporte original.

El checker comprueba:

- Frontmatter físico al inicio, YAML válido y sin claves duplicadas.
- Claves exactas `skill`, `version`, `fecha`, `inputs`, `estado`, `condicion`; identidad, versión y condición coinciden con report-context.
- Fecha con formato ISO y estado no vacío. **No certifica fecha real ni legitimidad del estado.**
- Inventario completo y hashes reales de case e inputs. No sigue symlinks de fuentes; no lee destinos externos nombrados por el reporte.
- Las cinco secciones ATX requeridas, una vez cada una, fuera de fences y comentarios HTML. No es un parser Markdown universal.
- Extensión por whitespace de todo el archivo, incluido frontmatter, y respuesta final completa de máximo 80 palabras, incluida su ruta.

Se admiten objetos `path/sha256` y las strings de hashes legacy ya observadas; no se impone retroactivamente un schema de inputs que el case histórico no exigía.

La nueva instrucción común explicita el formato y el conteo para ambas condiciones. El transporte guarda `prompt.txt`, su SHA-256 y `report-contract.json`. Se mantienen las herramientas, permisos, límites de requests y guards existentes.

## Estados y parada

| Campo o estado | Interpretación |
|---|---|
| `runtime_success` | CLI, persistencia, usage/modelo e integridad técnica |
| `contract_success` | Cumplimiento mecánico observado |
| `execution_success` | Runtime y contrato pasan conjuntamente |
| `semantic_review: REQUIRED` | La verdad y suficiencia de los hallazgos siguen pendientes |
| `STOPPED_RUNTIME_FAILURE` | El coordinador se detiene por ejecución fallida |
| `STOPPED_CONTRACT_FAILURE` | Se detiene por contrato fallido o comprobación ausente |

El presupuesto solo recupera su límite compartido si pasa `execution_success`. No hay reparación automática, reintento pagado ni sobrescritura de reporte. Un PASS del checker no acepta gates ni demuestra eficacia de una skill.

## Pruebas y revisión

Se observaron los fallos antes de implementar los checks y la parada. Las pruebas cubren versiones y condiciones incorrectas, campos ausentes, hashes falsos o incompletos, duplicados, fechas inválidas, YAML/JSON corrupto, límites exactos, secciones ocultas, código legítimo y symlinks.

La revisión independiente reprodujo un falso PASS inicial por headings dentro de fences. Se corrigió junto a dos errores de diagnóstico; se preservó la revisión original y se añadió seguimiento aprobado. También se reprodujo y cerró una lectura de destino symlink en el checker antes de calcular su hash.

**Suite completa final: 262 PASS, cero fallos, 17.43 segundos.** Claude Code real contra proveedor HTTPS simulado verifica:

- Reporte válido baseline: runtime, contrato y ejecución PASS.
- Reporte válido treatment con Skill 0.2 nativa: los tres PASS.
- Reporte inválido: runtime PASS, contrato y ejecución FAIL; archivo original conservado y presupuesto cerrado.

Los outputs del proveedor simulado prueban la infraestructura; no prueban la capacidad de un LLM para cumplir el contrato o resolver un engagement.

Como diagnóstico readonly, el checker detecta en el L01 real histórico `report:word_limit` y `missing:version`; respuesta final de 62 palabras. El hash del reporte permanece intacto. No sustituye ni altera la evaluación anterior.

## Integridad y coste

Los 222 archivos del cierre 0.2.0 conservan sus hashes. Canonical `detect-leakage` permanece 0.2.0 experimental con SHA-256 `c2a2440477d9985489b71f4d8c50380ccd7985635d02eab330cfee0f7e5856c4`.

**Cero llamadas nuevas a la API del estudio y coste API adicional US$0.** El acumulado estimado de detect-leakage permanece US$0.09112648 y el saldo US$0.00887352. No se mide aquí el consumo de Codex del coordinador/reviewer. No se utilizó una clave real en las pruebas simuladas.

## Pendiente

1. Congelar una configuración nueva con este transporte antes de otra evaluación real. Los paquetes históricos conservan sus versiones de código; no se actualizan automáticamente ni deben combinarse con el coordinador nuevo.
2. Completar L02/L03 nativos y comparar nuevamente condiciones iguales. El saldo actual no permite asegurar una secuencia completa bajo las reservas; no habrá llamadas de pago adicionales ni exceso del techo sin presupuesto explícito.
3. Revisar la semántica de los reportes, las acciones de reconstrucción y los escenarios menos guiados antes de considerar otro estado de madurez.
4. La compatibilidad formal del template Foundry con `quick_validate` de Codex permanece independiente de este cambio.

## Evidencia

Paquete `evaluations/foundry/2026-10-12-native-report-contract-01/`: XML RED/GREEN y suite final, `REVIEW.md`, `FOLLOWUP.md`, diagnóstico histórico, `verification.json`, tres trazas nativas simuladas y snapshot del código con manifest. Fuentes modificadas: `scripts/evaluations/foundry_native_transport.py`, `foundry_study.py` y sus pruebas.
