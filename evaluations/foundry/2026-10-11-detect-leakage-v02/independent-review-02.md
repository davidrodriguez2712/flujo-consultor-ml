# Revisión independiente 02 — detect-leakage 0.2.0

Fecha de revisión: 2026-10-12. Alcance: lectura y comprobaciones locales, sin API, red, entrenamiento ni modificación de cases, expected, outputs o canonical. Se leyeron las reglas de David Skill Foundry y writing-skills. Este juicio se emitió sin consultar MICRO-REVIEW ni conclusiones de otros reviewers.

## Juicio

Recomiendo que el borrador pueda sustituir a 0.1.0 **exclusivamente como experimental supervisada**, conservando evidencia y límites explícitos. No recomiendo asignar evaluated, validated o stable ni presentar mejora causal demostrada. La decisión final corresponde al responsable humano; esta revisión no modifica el canonical.

El procedimiento 0.2.0 corrige reglas peligrosas de 0.1.0: solape de entidades e igualdad feature-target dejan de confirmar leakage por sí solos; se distingue historia de disponibilidad efectiva; fit global puede confirmarse por su mecanismo; la falta de artefactos conserva incertidumbre. La skill impone un contrato del caller y separa inspección de ejecución. Estas mejoras son defendibles por contenido y por las ejecuciones forward observadas. La evidencia nativa muestra incumplimientos de contrato y una regresión inconclusa por transporte, que impiden declarar despliegue totalmente verificado.

## Matriz de contenido, contrato y longitud

Conteo determinista: `len(text.split())`, archivo completo con frontmatter. “Cumple observable” no implica que todos los pasos del runtime estén auditados. El cap explícito de los cases N es 700; los cases legacy forward no contienen cap, aunque los ocho reportes quedan bajo 700.

| Reporte | Contenido contra expected privado | Contrato observable del reporte | Palabras / límite |
|---|---|---|---|
| N01 baseline | Cumple: 3/3 accesos 19 h posteriores, ventana pasada distinta, target retrospectivo válido, remedio condicionado | Campos requeridos, cinco secciones, fuentes y persistencia presentes | 516 / 700; cumple |
| N01 treatment | Cumple: mecanismo de disponibilidad confirmado, no basta period_end, sin fuente alternativa inventada ni certificación de fit/split | Cumple observable | 453 / 700; cumple |
| N02 baseline | Cumple: cartera conocida, identidad legítima, fit solo train y labels maduros; sin GroupKFold obligatorio ni performance | Cumple observable | 539 / 700; cumple |
| N02 treatment | Cumple: mismo diagnóstico, distingue ejecución real y año de entrenamiento no escrito expresamente | Cumple observable | 507 / 700; cumple |
| N03 baseline | Cumple: fit_transform global contamina por evaluación futura; amount no es intrínsecamente ilegítimo; remedio correcto | Cumple observable | 478 / 700; cumple |
| N03 treatment | Cumple: mismo mecanismo confirmado y remedio, CV condicional; no inventa métricas | Cumple observable; párrafo de contrato redundante, sin defecto material | 486 / 700; cumple |
| L02 regression forward | Cumple: historia y labels disponibles, recurrencia válida, fit train-only, alcance documental y señal fuerte no prueban leakage | Cumple observable | 564 / sin cap en case; también bajo 700 |
| L03 regression forward | Cumple: No determinable, exportación distinta de disponibilidad, pide ventana y disponibilidad conjunta, escenarios condicionales | Cumple observable | 531 / sin cap en case; también bajo 700 |
| L01 treatment nativo | Mecanismo esencial correcto: recovered_kwh posterior incluida en features; historia válida; no acusa señal como prueba ni inventa entrenamiento | Parcial: falta clave exacta `version`, usa `skill_version`; H2/H3 incompletos frente a campos por hallazgo | 528 / 500 configurado; no cumple |
| L02 treatment nativo | No evaluable: no hay reporte; invocación y lectura no prueban resolución | No completado: report_persisted=false, returncode=1 | No hay reporte |
| L03 nativo | No ejecutado | No evaluable | No hay reporte |

Los ocho forward incluyen skill/version apropiadas a su condición, fecha, estado, condicion y hashes reales; las cinco secciones están presentes y los hallazgos materiales contienen mecanismo, fuente, confianza, severidad y acción. Fechas de labels, diferencias de disponibilidad, recurrencia y orden de código concuerdan con el expediente. N02 treatment y N03 treatment explicitan la ausencia del año del entrenamiento en el contexto: esto es cautela sustentada, no un timestamp inventado, y no invierte el diagnóstico esperado.

No existen respuestas finales o trazas de conversación forward en las carpetas revisadas. Por tanto, no certifico el límite de resumen final de 80 palabras, la ejecución de utility declarada, la fecha exacta de ejecución, ausencia de lecturas no autorizadas ni ausencia histórica de sobrescritura. Sí verifico los artefactos actuales, sus hashes, las condiciones en report-context y los inputs emparejados. La fecha forward 11/12 de octubre no presenta contradicción manifiesta con el expediente, pero no sustituye metadata temporal independiente.

## Checks y fundamentación

- Los 32 SHA-256 de case e inputs consignados en los ocho forward coinciden con los bytes de sus respectivos workspaces. No se detectaron fakehashes.
- Los cuatro hashes de inputs/case de L01 nativo coinciden; el hash de reporte coincide con metadata. El stdout nativo contiene el resultado real de la utility y una escritura nueva con originalFile=null. La metadata registra invocación Skill, lecturas, utility y Write; no hay ejecución del pipeline, entrenamiento o acceso web entre las llamadas registradas.
- Draft, snapshot native-config, plugin instalado nativo y los cinco snapshots forward treatment/regression tienen el mismo SHA-256: `c2a2440477d9985489b71f4d8c50380ccd7985635d02eab330cfee0f7e5856c4`.
- N01–N03 baseline/treatment tienen idénticos case, workflow e inputs. Esto controla el expediente, pero no acredita por sí solo mismo modelo, aislamiento y parámetros de ejecución forward, que no tienen metadata de runner aquí.
- Los timestamps citados en las conclusiones proceden de CSV/contexto. L01 nativo fecha 2026-10-11 es consistente con started_at 2026-10-12T04:54:32 UTC convertido a America/Lima. No vi fechas operacionales, métricas o fuentes externas inventadas.
- La observación nativa recovered_kwh>0 coincide con target en cuatro filas es reproducible por lectura; se etiqueta como indicio. No equivale a performance ni prueba adicional independiente.

## Defectos materiales y límites

1. **Contrato nativo L01 incompleto.** `skill_version` comunica la versión pero no satisface la clave `version` requerida por el caller. H2 no declara todos los campos por hallazgo (en particular severidad y confianza explícita); H3 omite varios. El esquema de inputs son strings YAML con hashes, que permite trazabilidad pero es menos estructurado que forward; el case no exige objetos path/sha256, por lo que no lo trato como fallo autónomo.
2. **Longitud nativa.** 528 excede el límite 500 en config y RUNBOOK. La inspección del código congelado confirma que study pasa `report_word_limit` de config al transporte y que este añade al prompt “máximo 500 palabras” junto al resumen final de 80. El test local `test_real_cli_receives_explicit_common_tool_limits` utiliza CLI real con upstream simulado y comprueba esa transmisión; su resultado de ejecución lo reportó el coordinador y esta revisión leyó el test sin volver a ejecutarlo. Por tanto, hay respaldo de infraestructura para la transmisión del cap. El stdin completo de esta ejecución particular no está persistido, por lo que mantengo esa reserva observacional; el incumplimiento de extensión del artefacto es inequívoco.
3. **Remedio nativo ambiguo.** H1 combina excluir recovered_kwh con “reconstruir solo si hay fuente con corte histórico”. La exclusión inmediata es correcta, pero la misma recuperación post-inspección no puede existir retrospectivamente al scoring. Debe entenderse como una feature de historia de recuperos anteriores diferente, con fuente verificable, no como rescate de estos valores. No se inventa esa fuente; la ambigüedad requiere revisión supervisada.
4. **L02 nativo incompleto por truncamiento y parada local.** La última respuesta enviada al proveedor figura en `runs/native-01/ledger.json` con HTTP 200, `provider_stop_reason=max_tokens`, 4096 output tokens, de los que 2527 son thinking tokens; después consta un rechazo local “Solicitud anterior fallida; sin retry”. El guard registra “Respuesta sin usage/stop válido”. El `result.txt` presenta `Failed to authenticate. API Error: 403 request bloqueado antes de enviarlo`, pero ese 403 es la parada local del siguiente intento antes de otro envío: no demuestra credenciales inválidas ni un 403 upstream. Metadata report_persisted=false y summary STOPPED_RUNTIME_FAILURE confirman que no hubo reporte. Esta secuencia no prueba error semántico del diagnóstico ni PASS de la skill; sí muestra falta de completitud con el cap de salida. L03 carece de ejecución; no computar ni éxito ni fracaso semántico.
5. **Sin mejora semántica incremental demostrada en N.** Los tres controles ya resuelven correctamente los mecanismos esenciales. N01 treatment es 63 palabras menor, N02 32 menor y N03 8 mayor: no convertir esto en efecto robusto de eficiencia con una observación por condición ni sin datos de tokens/tiempo. Forward regression muestra conservación en dos casos legacy, no eficacia independiente ni generalización amplia.
6. **Compatibilidad formal y tamaño.** Draft conserva metadata Foundry plana (`status`, `version`, `domain`), necesaria para su lifecycle local. El rechazo del quick_validate estricto de Codex por estas claves no es prueba de semántica incorrecta ni puede ocultarse como validación formal exitosa. El draft tiene 719 palabras, por encima del objetivo general <500 de writing-skills; el objetivo no es cap del caller, pero hay margen de concisión. No certificar compatibilidad universal con AgentSkills.

## Decisión recomendada y uso

El balance favorece 0.2.0 para reemplazo experimental supervisado: elimina contradicciones de confirmación de la versión anterior y todos los forward mantienen el diagnóstico correcto con contrato observable adecuado. Esta recomendación admite expresamente el fallo nativo de formato/extensión, la falta de evidencia forward de ejecución y el corte nativo de L02/L03.

Registrar 0.2.0 como experimental con esta revisión adjunta; revisar manualmente cada reporte y su contrato, especialmente los campos exactos del caller y las acciones de reconstrucción. No aceptar gates, certificar producción ni afirmar eficacia superior, conformidad formal o batería nativa completa. Antes de cualquier cambio de lifecycle, completar la evidencia faltante de runtime, verificar transmisión de caps y obtener una comparación controlada que revele una mejora observable sin cambiar expected retrospectivamente. Una futura modificación del draft requiere nueva evidencia para el hash resultante; esta revisión corresponde únicamente al hash indicado.

## Precisión posterior de infraestructura

Tras emitir el juicio independiente inicial se leyó el ledger y el código congelado del transporte/study, a petición del coordinador, para precisar causalidad de L02 y transmisión del cap. Estas precisiones no cambian la recomendación, los expected ni la matriz de resultados; no se consultaron conclusiones de otros reviewers.
