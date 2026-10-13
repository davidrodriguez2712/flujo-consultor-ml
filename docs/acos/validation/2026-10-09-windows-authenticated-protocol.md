# Protocolo — runtime autenticado de Windows

## Autorización y alcance

David autorizó US$1 total para comprobar Claude Code y Codex en Windows x64 y
ARM64, con prioridad en reducir el gasto. Secrets verificados por nombre; sus
valores no se consultan ni se copian a archivos locales.

Se asignan US$0.25 por runtime y arquitectura. Primero ejecutar x64 y revisar
su evidencia; ejecutar ARM64 únicamente después. Sin reintentos automáticos.
Una ejecución fallida detiene el siguiente runtime de la misma arquitectura.

Esto comprueba integración de runtime y recuperación desde archivos de ACOS.
No es una evaluación baseline/treatment ni autoriza promociones en Foundry.

## Caso y checks definidos antes de ejecutar

- Workspace de churn sintético generado por el compiler de ACOS.
- Snapshot de `design-validation` 0.1.0, **experimental**, idéntico al archivo
  canónico leído el 2026-10-09. SHA-256:
  `70883c3b75b07334fc95bad1b5c6749fd7b5e623b648f6b48fb6c14b2d32b8f9`.
- El harness añade el snapshot a los directorios nativos de ambos runtimes.
  Esta prueba no vuelve a evaluar la selección de skills del resolver.
- Estado canónico: `validation / BLOCKED`; objetivo con identificador aleatorio;
  bloqueo por fecha de disponibilidad de labels sin confirmar.
- STATE/MANUAL conservan sus vistas iniciales. No hay dataset, labels reales,
  entrenamiento ni aprobaciones de gates.

Dos ejecuciones independientes por runtime:

1. Solicitud guiada: cargar la skill nativa y producir un checklist breve,
   declarando el objetivo canónico, estado y bloqueo.
2. Sesión nueva con mensaje exacto `continuemos`: recuperar objetivo y bloqueo
   desde los archivos, sin depender del historial de la ejecución anterior.

Checks: exit code, identificador canónico en la respuesta, bloqueo y disponibilidad
de labels reconocidos; lectura exitosa de SKILL.md en la traza Codex o llamada
a la herramienta Skill en Claude; comparación SHA-256 del workspace completo
antes y después. No se acepta una afirmación del modelo como única prueba de
invocación. El checklist se devuelve en la conversación; la restricción explícita
de solo lectura impide persistir el reporte habitual de la skill.

No se comprueba `resume` de conversaciones persistidas ni permisos de escritura.
La lectura de una skill y una respuesta apropiada en este caso no acreditan su
eficacia general.

## Reducción y control de consumo

- Codex 0.160.0 con `gpt-6-luna` en la revisión actual, reasoning bajo y salida máxima 1024 tokens.
- Claude Code 2.1.294 con `claude-haiku-4-5-20251001`, salida máxima 1024 tokens,
  seis turns por solicitud y `--max-budget-usd 0.25` adicional.
- Proxy localhost que permite únicamente el modelo elegido y su endpoint de
  generación, máximo dieciséis solicitudes por runtime; sin herramientas remotas de
  pago, imágenes, audio, contexto remoto previo ni retries HTTP del proxy.
- El proceso del agente recibe una clave local ficticia. El proxy conserva la
  clave real en memoria y solo la envía al proveedor correspondiente por HTTPS.
- Antes de enviar cada request, reservar una estimación conservadora basada en
  bytes UTF-8 del payload más 16384 de margen y el máximo de tokens de salida.
  Bloquear antes de enviar si la reserva excede la partida disponible.
- Liberar la diferencia únicamente tras recibir usage completo. Con usage
  ausente se conserva toda la reserva. Si una estimación supera su reserva,
  bloquear solicitudes posteriores y registrar la anomalía.

Tarifas de la revisión actual: Luna standard input US$0.10/output US$0.50 por
millón de tokens, cache writes US$0.125 y cache reads US$0.01; Haiku input
US$1/output US$5, cache writes US$1.25 o US$2 y cache reads US$0.10. El proxy
  reserva al precio de cache write, y separa usage de cache al liquidar. Los
intentos iniciales usaron gpt-5.3-codex (US$1.75/US$14) y conservaron una
estimación conservadora sin descuento de cache. No hay fallback automático
a otro modelo si el seleccionado falla.

Los importes son estimaciones operativas, **no una factura ni un límite de
facturación garantizado por los proveedores**. No incluyen minutos de GitHub
Actions ni otra actividad de las cuentas.

Fuentes: [precios OpenAI](https://developers.openai.com/api/docs/pricing),
[precios Anthropic](https://platform.claude.com/docs/en/about-claude/pricing),
[configuración Codex](https://learn.chatgpt.com/docs/config-file/config-reference),
[límites CLI Claude](https://code.claude.com/docs/en/cli-reference).
Tarifa y soporte de function calling de la revisión actual:
[GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna).

## Evidencia

Workflow manual: `.github/workflows/windows-authenticated-validation.yml`.
Artifacts locales: `artifacts/windows-authenticated-2026-10-09/`.
Conservar resultados, trazas sintéticas, usage, reservas, metadata de GitHub y
hashes. No conservar auth.json, variables de entorno ni headers de autenticación.

Antes del primer dispatch: 137 tests locales pasan; 12 comprueban presupuesto, trazas y
fixture sin llamadas de pago. El resultado autenticado se informa por separado.

## Correcciones del harness registradas durante la ejecución

Primer intento: cero requests enviados al proveedor. Se corrigió la aceptación
de JSON schemas y namespaces locales de herramientas; se desactivó web search.
Se fijó el snapshot como binario en `.gitattributes` para preservar su SHA-256
en Windows. No cambió el contenido de la skill ni el expected de la prueba.

Segundo intento: un request OpenAI con usage completo, estimación US$0.029015.
Comando de lectura compuesto rechazado por política; siguiente request bloqueado
porque el proxy aún mantenía la reserva del anterior. Se corrigió la liquidación
para realizarla antes de entregar el evento terminal al CLI. Un test con proveedor
simulado mantiene abierta la conexión anterior y reproduce este orden.

El fixture añade ahora una pauta explícita para leer una ruta literal por comando
PowerShell; Codex utiliza sandbox nativo `unelevated` y conserva `read-only`.
Esto añade orientación al harness: no es evidencia de operación sin guía.
Se reduce la salida Codex a 1024 tokens. El siguiente intento x64 asigna US$0.22
por runtime: los US$0.029015 previos más US$0.44 potenciales quedan bajo US$0.50
para x64. La partida de ARM64 permanece en US$0.50. No hay retry automático.

Tercer intento: comandos de lectura ejecutados desde `C:\\Program Files\\PowerShell\\7`,
sin encontrar el archivo relativo. Consumo conservador US$0.0551355; total
acumulado US$0.0841505. Se añade `login=false`, workdir explícito y rutas
absolutas al fixture. Se permite leer varias rutas literales por comando para
reducir turns sin cadenas de comandos. La siguiente revisión cambia a Luna,
documentado con soporte de function calling y menor precio, y limita x64 a
US$0.20 por runtime. Antes de ejecutar: 140 tests locales pasan; 15 verifican el
probe y presupuesto sin APIs. Los fallos anteriores se preservan.

Cuarto intento: Luna funciona con la API, pero el token restringido no puede
leer el fixture bajo el directorio temporal privado. Usage estimado adicional
US$0.00269929; acumulado US$0.08684979. El fixture se traslada a un directorio
creado con `mkdir` bajo el checkout de CI, que hereda sus ACL, y se añade una
lectura offline mediante `codex sandbox` antes de las generaciones.

Quinto y sexto intentos: sin llamadas de modelo. El preflight requiere un perfil
nombrado; se utiliza `acos_read` heredado de `:read-only`. Su salida Windows
contiene bytes de consola no UTF-8; se conserva en binario y se verifica el
identificador ASCII antes de decodificar la vista textual. La revisión actual
también pide una lectura observable del archivo de skill para Codex y registrar
el identificador del objetivo al retomar. No se suministra su valor esperado al
agente: este debe leerlo del estado canónico. Son pautas explícitas del fixture.

Antes del séptimo intento: 141 tests locales pasan, incluyendo 16 tests del probe
y consumo. El preflight nunca llama a modelos. El protocolo sigue en solo
lectura, sin permisos de escritura ni red para comandos sandboxed.

Séptimo intento: Codex x64 pasa ambas ejecuciones y la lectura offline; workspace
sin cambios. Estimación Luna US$0.00772443. Claude recibe HTTP 400 y no completa
una generación: se conserva la reserva US$0.133524 por falta de usage. Total
estimado observado US$0.09457422; total conservador comprometido US$0.22809822.
Los importes no son equivalentes: una reserva de un request rechazado no acredita
un cargo de facturación.

Se añade selección individual de runtime para no repetir Codex x64. El proxy
preserva tipo y mensaje de error del proveedor, con la clave eliminada, cierra
el circuito ante un rechazo y devuelve denegaciones locales como HTTP 403 para
evitar que el SDK las interprete como rate limits reintentables. Claude fuerza
cache de cinco minutos: en la revisión actual su reserva usa US$1.25 por millón
de tokens de input. Se ejecuta diagnóstico Claude x64 con US$0.20 y Codex ARM64
con US$0.05, manteniendo US$0.47809822 como máximo conservador de esas partidas
y el consumo anterior. No se vuelve a ejecutar Codex x64.

Octavo intento (Claude x64): Anthropic identifica el problema del request:
`clear_thinking_20251015` requiere thinking activo, pero el proxy lo desactivó
para limitar consumo. No fue un resultado de consultoría ni una prueba fallida
de la skill. Se retiene otra reserva de US$0.08541125 por ausencia de usage;
el CLI declara coste cero para esta ejecución. Se elimina la estrategia de
context management dependiente de thinking; test de regresión rojo/verde.

Noveno intento (Codex ARM64): ambas ejecuciones y preflight pasan, en Windows 11
nativo. Usage estimado US$0.007780755. El total conservador previo a repetir
Claude es US$0.321290225, incluyendo las reservas de sus requests rechazados.
Se asignan US$0.20 para Claude x64 y otros US$0.20 para Claude ARM64 tras revisar
x64: máximo conservador US$0.721290225, bajo el dólar autorizado. Suite local
actual: 143 tests; 18 corresponden al probe/presupuesto, sin APIs.

Décimo intento (Claude x64): tres requests correctos, estimación US$0.03511705.
El runtime leyó el estado y la skill mediante Read, pero no invocó Skill; el
probe lo rechaza y no ejecuta continuidad. El workspace permanece sin cambios.
Esto tampoco demuestra calidad analítica: la respuesta atribuyó datos al fixture
que no contiene dataset. Se conserva el fallo.

La siguiente revisión usa instrucciones específicas por runtime, declara la
ausencia de dataset y exige un tool_result exitoso de la invocación Skill para
Claude. No se relaja el criterio. Suite local: 144 tests pasan; dos tests de
servidor simulado necesitan permiso para abrir localhost, sin APIs reales.
Antes del intento 11: estimación observada US$0.137472025, compromiso conservador
US$0.356407275. Se asignan US$0.20 a Claude x64 y, solo tras revisar su resultado,
US$0.20 a ARM64: máximo acumulado conservador US$0.756407275.
Commit 3b824c7; intento 11: GitHub Actions 37891296383.

Intento 11: Skill invocada correctamente, pero sin lectura del estado; el agente
inventa etapa/objetivo y se rechaza. Estimación US$0.02797065; no continuidad.
Intento 12: se pide leer AGENTS.md y .acos/state.yaml antes de Skill. Esto hace
la prueba guiada más explícita; no demuestra autoorientación sin guía. Commit
001e9fe, run 37891497677, partida US$0.20. ARM64 sigue condicionado a revisar x64.

Intento 12: guided PASS; continuidad lee objetivo/validation/BLOCKED/labels
correctamente, pero termina con error_max_turns (6), no respuesta final.
No se cuenta como PASS. Coste estimado US$0.0592314; acumulado US$0.224674075
y compromiso conservador US$0.443609325. Se amplía max-turns a 10, manteniendo
solo lectura, maxrequests16, salida1024 y partida US$0.20. Con otra partida
ARM64 de US$0.20 el máximo conservador sería US$0.843609325.

Intento 13 (run 37891756918 / db8e82d): Claude x64 PASS en guided y continuidad,
Skill exitosa y lectura de estado observables, workspace sin cambios. Usage
estimado US$0.05479895. No requiere repetir Codex ni x64. Antes de Claude ARM64:
estimación acumulada US$0.279473025; conservador US$0.498408275. Con partida
ARM64 US$0.20: máximo conservador US$0.698408275.

Intento 14 (run 37891953156 / db8e82d): Claude ARM64 PASS en guided y continuidad,
Skill exitosa y estado canónico recuperado, workspace sin cambios. Estimación
US$0.0667421. Total API estimado US$0.346215125; compromiso conservador
US$0.565150375. Se detienen las llamadas de pago. Matriz completa 4/4 runtimes
por arquitectura, ocho ejecuciones; informe final enlazado en la matriz de release.
