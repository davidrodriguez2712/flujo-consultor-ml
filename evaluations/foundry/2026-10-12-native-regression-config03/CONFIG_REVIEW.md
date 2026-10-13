# Revisión de configuración 03 frente a preparación 02

Fecha: 2026-10-12. Reviewer: agente Codex `/root/native_real02_review`, distinto del autor/runner. Conoce y revisó real-01 de preparación 02; esta revisión no es ciega ni humana. No se modifican paquetes, reportes anteriores, criterios, skill, autorización financiera ni estados de promoción. No se consultan claves ni se realizan llamadas API/red, entrenamiento o delegación.

## Resultado de comparación

**Cambio operativo acotado confirmado, con una inconsistencia de metadata presupuestaria.** La comparación byte por byte de los archivos fuente de ambos paquetes encuentra únicamente cuatro archivos modificados: `RUNBOOK.md`, `config.json`, `execution-manifest-01.json` y `snapshots/scripts/evaluations/foundry_native_transport.py`. No hay archivos fuente añadidos ni eliminados. Los archivos derivados `__pycache__` no se usan como evidencia de identidad del código fuente.

En `foundry_native_transport.py`, el único diff es una línea añadida a la construcción del prompt común: instrucción literal de conservar `---` inicial y final de metadata, seguida del esquema de seis claves y las cinco secciones ya exigidas. No cambia lógica de ejecución, guards, permisos, transporte, detención, validación, retry ni límites. El prompt realmente emitido para L01 de configuración 03 contiene la instrucción literal. El esquema presenta placeholders, no hashes, fecha o conclusiones inventadas; requiere sustituirlos con datos autorizados.

Sin cambios byte por byte:

- Cases e inputs públicos de L01, L02 y L03.
- Los tres expected privados.
- `skill/SKILL.md` (detect-leakage experimental 0.2.0), SHA-256 `c2a2440477d9985489b71f4d8c50380ccd7985635d02eab330cfee0f7e5856c4`.
- Workflow común y snapshots de `runtime_budget.py`, `foundry_input_facts.py` y `foundry_study.py`.

Config mantiene modelo `claude-haiku-5-5`, CLI 2.1.296, output cap 8192, ocho requests por invocación, schedule L01–L03 treatment, máximo real 24 requests, reporte 500 palabras, final 80 y cero retries automáticos. Que el prompt muestre un esquema no flexibiliza la condición de frontmatter real al inicio físico, los campos por hallazgo ni la revisión semántica. No repara retroactivamente el fallo contractual L02 observado en preparación 02.

## Metadata y presupuesto

Manifest cambia ID y hashes/tamaños correspondientes a RUNBOOK, config y transporte modificado. Se recomputaron readonly sus 23 entradas: todas coinciden en tamaño y SHA-256 con los archivos presentes. El approval liga el nuevo manifest a la ronda; no se interpreta aquí como una nueva autorización.

El prior 0.10135322 USD y available 0.04864678 USD suman 0.15 USD. RUNBOOK y `approved-real-01.json` declaran techo acumulado 0.15 USD, saldo máximo nuevo 0.04864678 y cero retries automáticos. **Reserva de severidad media de documentación/metadata:** `package/config.json` todavía conserva `budget_ceiling_usd: 0.1`. Esa clave contradice el techo acumulado declarado en los otros dos archivos. No se cambia silenciosamente ni se afirma que todo el presupuesto esté uniformemente documentado. Este review no determina que esa clave gobierne el límite runtime ni rechaza la autorización preexistente; distingue la inconsistencia documental del approval explícito. La revisión de calidad no aumenta presupuesto ni autoriza gasto adicional.

## Límites de verificación

El coordinador informa suite de 262 PASS en 18 segundos y prueba de transmisión literal RED→GREEN. No se volvieron a ejecutar tests en esta revisión; esas cifras se registran como información del coordinador, no como observación independiente de sus logs. La evidencia propia aquí es comparación de fuente, recomputación de manifest y presencia del esquema en el prompt emitido.

Al completar esta revisión solo había metadata L01 y no summary final. No se emite todavía dictamen de resultados para esta ronda ni se contabilizan L02/L03. Se espera aviso del coordinador para revisar outputs terminados contra expected. La comparación futura será tratamiento-only, con conocimiento de ronda 02: no aislará efecto causal del formato ni de la skill, no probará superioridad y no promoverá la capacidad.

## Addendum tras aclaración del coordinador

Se conserva arriba la reserva original y su momento de observación. La lectura posterior de `snapshots/scripts/evaluations/foundry_study.py:28–51,101,114` aclara que 0.10 es la cota fija de verificación/aceptación por paquete; el Proxy recibe el `amount` devuelto desde `approved.total_budget_usd`, aquí 0.04864678. Por tanto, la diferencia numérica con el techo acumulado 0.15 no demuestra límites financieros contradictorios del runtime: queda una ambigüedad de denominación/documentación entre cota por paquete y techo del estudio. No habilita gastar 0.10 nuevos en esta ronda.

`launch.json` declara budget_usd 0.04864678 y el mismo manifest que approval; approval declara prior 0.10135322 y techo acumulado 0.15. Su suma verifica aritméticamente. El coordinador informa que el launcher calculó el prior desde ledgers y comprobó la suma antes de leer la clave; esos pasos no están detallados en launch.json y se atribuyen al coordinador, no a un log independiente. No se leyó la clave. La ligadura de historial/saldo depende de coordinación secuencial y snapshot de aprobación; no se afirma un tracker global automático. El summary final ya existe y los tres casos terminados son objeto de `REVIEW-REAL-01.md` separado.
