---
skill: detect-leakage
version: 0.2.0
date: 2026-10-12
model: "claude-haiku-5-5 para API; subagents de Codex para comprobaciones suplementarias"
cases: [L01, L02, L03, N01, N02, N03]
---

# Hipótesis

Una guía más compacta y generalizable puede mejorar el respeto del contrato y evitar inferencias incorrectas sobre disponibilidad, clientes recurrentes y preprocessing. La evidencia no se transfiere automáticamente desde 0.1.0.

# Configuración

Tres modalidades distintas, cuyos resultados no se mezclan en una tasa de eficacia:

- Microprueba textual: misma tarea mínima, Haiku 5.5, cinco repeticiones por condición sin guía / 0.1.0 / 0.2.0. Guía en contexto, sin instalación ni herramienta Skill. Máximo 180 palabras. Quince solicitudes reales.
- Regresión nativa: Claude Code 2.1.296, plugin local 0.2.0, tres treatments previstos L01–L03, output cap 4096, reporte máximo 500 palabras. L01 completado; L02 truncado y detención; L03 no ejecutado. No nuevo baseline comparable.
- Comprobación suplementaria: tres pares nuevos en contextos de subagents separados y dos regresiones treatment. Guía textual, sin invocación nativa. No equivale al modelo Haiku controlado ni al transporte evaluado. Los agentes de las dos regresiones habían resuelto antes un caso distinto.

Expected privados, separados de los agentes que resolvieron. Los cuatro bloqueos de preparación se corrigieron antes de producir outputs; también se aclaró antes de N03 qué aprende el scaler. No se repararon reportes ni criterios tras observar los resultados.

# Casos utilizados

| Caso | Mecanismo o escenario |
|---|---|
| L01 | Recupero posterior a inspección como feature; historia previa legítima |
| L02 | Clientes conocidos, labels maduros y preprocessing train-only |
| L03 | Conteo de reclamos sin ventana ni disponibilidad verificables |
| N01 | Pagos del día anterior que llegan 19 horas después del scoring |
| N02 | Identidad como feature legítima en cartera recurrente |
| N03 | Scaler aprende parámetros globalmente antes de particionar |

# Resultados

Microprueba, según reviewer distinto del autor:

| Condición | Contenido aceptable con reservas | Dentro de 180 palabras |
|---|---:|---:|
| Sin guía | 0/5 | 5/5 |
| 0.1.0 | 5/5 | 0/5 |
| 0.2.0 | 5/5 | 5/5 |

Las cinco muestras sin guía desatienden información explícita del expediente. La brevedad mejora frente a 0.1.0 en esta tarea; cinco repeticiones no son cinco escenarios. Todos retuvieron campos adicionales: no hay evidencia aquí de mejora diferencial en esos campos. Doce salidas tienen fences exteriores; se conserva esa ambigüedad sin imponer retroactivamente un parser.

Los ocho informes suplementarios tienen entre 453 y 564 palabras. Los tres baselines nuevos también identifican los mecanismos centrales: no hay superioridad semántica demostrada. La adjudicación detallada está en `independent-review-02.md` del paquete de evaluación.

L01 nativo persiste e invoca Skill, pero tiene 528 palabras frente a 500, usa `skill_version` en lugar del campo solicitado `version` y omite componentes del contrato en hallazgos secundarios. Runtime completo no significa contrato PASS. L02 termina en `max_tokens` sin reporte persistido. No se presenta L03 como ejecutado.

# Correctitud, cobertura y fundamentación

La guía distingue ventana, cálculo y disponibilidad; recurrencia frente a generalización a nuevas entidades; y fit global frente a valores intrínsecamente futuros. Las comprobaciones iniciales apoyan esas distinciones en los escenarios examinados, no una certificación universal. Hay reservas sobre severidades de incertidumbres y cobertura de hallazgos secundarios.

La revisión independiente de 0.1.0 encontró errores de fundamentación adicionales al autorreview. Se conservan ambos juicios; no se reescribe la evaluación histórica para que concuerden.

# Accionabilidad

Las recomendaciones centrales son reconstruir features realmente accesibles al corte, conservar el escenario declarado y ajustar transformaciones con train antes de transformar evaluación. No se entrenaron modelos ni se aceptaron gates. Toda conclusión sobre producción requiere evidencia de proceso y supervisión.

# Eficiencia y coste

| Etapa | Solicitudes API | USD estimados |
|---|---:|---:|
| Cinco rondas 0.1.0 | 61 | 0.07056525 |
| Microprueba 0.2.0 | 15 | 0.01212650 |
| Regresión nativa parcial 0.2.0 | 7 | 0.00843473 |
| **Total del estudio** | **83** | **0.09112648** |

Saldo del techo US$0.10: **US$0.00887352**. Usage conocido; cifras estimadas por ledger, no factura. Estas llamadas son de Anthropic, no de OpenAI. No se atribuye coste API cero al servicio que ejecuta los subagents: no hicieron llamadas adicionales al proveedor del estudio, pero su consumo de Codex no está medido en este ledger.

No se continúa con API porque no cabe con margen una nueva secuencia nativa bajo las reservas. No se compara coste o latencia entre modalidades como efecto causal de la skill.

# Verificación local

- 233 pruebas PASS en 14.91 segundos, proveedor simulado, cero llamadas pagadas.
- La primera ejecución restringida tuvo 217 PASS y 16 fallos por bloqueo de sockets localhost; se conserva su XML junto al resultado con permisos adecuados.
- 541 referencias de archivos en manifests históricos verificadas sin diferencias.
- Inputs de los ocho workspaces suplementarios coinciden con sus cases; 36 hashes declarados en nueve reportes coinciden con los archivos.
- Metadata dinámica del plugin y report-context identifica la versión real; ya no hardcodea 0.1.0. Configuración permite caps explícitos 4096/8192 y límite de palabras, sin relajar los guards.
- `quick_validate` de Codex rechaza `status/version/domain` en root. Se preserva el template canónico del Foundry; no se afirma conformidad formal con ese validador. La ejecución nativa observada no resuelve la compatibilidad de todos los runtimes.

# Fallos encontrados

Contrato nativo todavía incumplido; truncación de L02; L03 nativo pendiente; efecto techo en nuevos baselines; pruebas suplementarias sin control de versión del modelo; revisión por agentes, no humana ni ciega. Ninguno se oculta o convierte en PASS por reformatear outputs.

# Resultado y decisión

La hipótesis se confirma parcialmente en la microtarea de brevedad y seguimiento del expediente. **No se confirma una mejora general de eficacia del runtime.** Mantener `experimental` y supervisión; no promover a evaluated, validated ni stable por estas tasas.

Después de la revisión independiente, se sustituyó la versión canónica 0.1.0 por el mismo hash evaluado de 0.2.0, manteniendo `status: experimental`. Se verificó el hash anterior antes de escribir y el nuevo después. No se cambiaron snapshots de proyectos existentes ni instalaciones globales. La versión anterior y sus resultados permanecen preservados.

# Próximo experimento

Antes de nuevas llamadas, preparar un contrato inequívoco y control de longitud/metadata que rechace resultados inválidos sin repararlos. Completar L02/L03 nativos y una comparación nueva con condiciones iguales requiere un presupuesto distinto explícito; el saldo actual no se convierte en autorización para exceder el techo. Después, evaluar escenarios menos guiados y revisar con un humano los desacuerdos de juicio.

# Evidencia

Paquete: `evaluations/foundry/2026-10-11-detect-leakage-v02/`; borrador, cases, expected, outputs originales, ledgers, configs, microreview, review independiente y checks. Registro de cierre y hash de la versión canónica, si se actualiza: `canonical-update-01.json`. Los snapshots históricos no se actualizan automáticamente.
