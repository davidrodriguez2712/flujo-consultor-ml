# detect-leakage — revisión y propuesta de runtime

## Estado

Paquete revisado localmente por su autor, sin defectos de fixture identificados. Aceptación humana del paquete/expected/regla todavía pendiente. Configuración concreta documentada como DRAFT_NOT_EXECUTABLE_PENDING_TRANSPORT_DESIGN_APPROVAL: infraestructura anterior incompatible con herramientas y sesiones multipaso. No llamadas pagadas ni credencial cargada; eficaciaNOT_EVALUATED y Foundry canónico intacto.

## Descubrimiento nativo sin generación

Se ejecutaron tres pares de SDKinitialize en procesos/cwd/configdir temporales nuevos, sin mensajes user ni solicitud de generación. No credencial/APIkey cargada; baseURLlocalhost sin servicio como defensa adicional. Probes conservados fuera del freeze original.

1. bare+restricted+settingsourcesvacío: baseline sin detect-leakage, treatment tampoco la descubre. No se declara compatible.
2. Sinbare, setting_sourcesproject+restricted: mismo fallo de descubrimiento treatment. No se cambia el snapshot.
3. Plugin local explícito, sinbare/safe, settingsourcesvacío+restricted: baseline sin detect-leakage; treatment reconoce acos-eval:detect-leakage. SKILL.md idéntico al snapshot/Foundry0.1.0.

Eso acredita descubrimiento del comando por CLI2.1.296, no invocación del cuerpo, acceso correcto, hashes producidos por agente, escritura ni aislamiento efectivo. Nombres de comandos incorporados del runtime pueden aparecer pese a disableBundledSkills; restringir el toolSkill al nombre permitido y comprobarlo antes de paidrun. No inferir acceso a todas las skills por la lista initialize.

## Cambio necesario del transporte

- runtime_budget.prepare prohíbe tools para Haiku5.5; conservar el default y añadir opt-in con whitelist de tools locales validada.
- workflow_native_transport.invoke desactiva skills y exige un request; esta tarea requiere varios pasos con tools. Adaptación separada que reutilice proxy y controles multipaso del probe Windows, sin editar snapshots históricos.
- Registros de eventos permiten distinguir discovery de invocación real Skill y persistencia de reporte; output finalend_turn, tool_use intermedio permitido.
- Bash solo para utility fija readonly con hechos genéricos de inputs; permisos efectivos de lectura/escritura y aislamiento se prueban con controles negativos. No BashPython arbitrario, red, subagents ni expected disponible.

No se ha implementado el cambio. superpowers:brainstorming requiere aprobar este diseño acotado antes de modificar comportamiento del runner.

## Propuesta concreta de ejecución posterior

ClaudeCode2.1.296/Haiku5.5; misma tarea/inputs/workflow/tools/permisos ambasramas, único plugin treatment. Read/Write/Bash/Skill restringidos, configdir aislado, settings explícitos, restricted/dontAsk, sin MCP ni customizaciones no seleccionadas. Exactitud/aislamiento reales pendientes de verificación.

Presupuesto propuesto nuevoUS$0.10total, no autorizado ni tomado del saldo de otroestudio. Unsmokecomún+seis ejecuciones(L01B/T,L02T/B,L03B/T), máximo8requests por invocación y56globales, cap8192, sin retries. Cada request reserva presupuesto antes del proveedor; una sesión puede parar sin terminar si la siguiente reserva no cabe. No garantiza completar pares ni eficacia. Tarifas oficiales consultadas, todavía no config ejecutable congelada.

Runtime real/native invocación y ejecución pagada se autorizan después de implementar/verificar/configurar y vincular aprobación al nuevo manifest. Reviewer distinto del autor sigue pendiente; no se declarará independiente si revisa el autor.

## Evidencia

Paquete original27archivos intacto. Snapshot skill sin cambios. Manifest nuevo de revisión12archivos SHA256935bcf4ca23de74b9582a918e11157fb543525ec3b05b50cbacc7f91943ba4f8. Control local sin anclaje externo. La disponibilidad correcta por plugin resuelve descubrimiento, no la compatibilidad del proxy con tools; esta continúa pendiente.

Archivos concretos: evaluations/foundry/2026-10-10-detect-leakage-01/configuration-proposal-01/config-proposal.json y TRANSPORT-DESIGN.md. Próximo paso: aprobación del diseño de transporte y verificación local, antes de cualquier presupuesto de API.

Referencias oficiales consultadas: https://code.claude.com/docs/en/skills ; https://code.claude.com/docs/en/cli-reference ; https://code.claude.com/docs/en/permissions ; https://platform.claude.com/docs/en/about-claude/pricing .
