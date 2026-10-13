---
skill: detect-leakage
version: 0.1.0
date: 2026-10-11
model: claude-haiku-5-5
cases: [L01, L02, L03]
reviewer: autor de la preparación, no independiente ni ciego
---

# Hipótesis

La skill experimental mejora la detección de información no disponible al predecir, evita falsos positivos y reconoce disponibilidad desconocida. La regla congelada exige mejora conjunta en al menos dos casos, ninguna regresión ni falso positivo crítico nuevo. Una repetición inicial por rama no acredita estabilidad ni eficacia general.

# Configuración

Claude Code2.1.296, plugin local explícito solo en treatment; snapshot Foundry0.1.0 sin cambios. Baseline sin skill. Mismos cases, tools, permisos, modelo, reporte≤700palabras y respuesta≤80; cap8192, ocho solicitudes por sesión y56 por ronda. Contextos/workspaces/configdirs nuevos. Expected privado no entregado al agente.

**Comparación válida: round05 únicamente.** Workflow común: extracto literal de autoridad, Definition of Done y escalamiento del snapshot OS. Instrucción común obliga a invocar detect-leakage al inicio si está instalada; la rama sin plugin sigue sin skill. Esto evalúa contribución con invocación requerida, no adopción espontánea. Las rondas anteriores no se agrupan ni reemplazan sus outputs.

## Ajustes de infraestructura y rondas preservadas

| Ronda | Solicitudes al proveedor | Resultado | API estimada US$ |
|---|---:|---|---:|
| 01 | 1 | Smoke: Bash no permitido, detenido | 0.000689075 |
| 02 | 11 | Smoke y L01B completos; L01T max_tokens antes de reporte | 0.017535290 |
| 03 | 12 | Contexto común acotado; L01T entrega reporte sin invocar skill | 0.010598560 |
| 04 | 10 | Skill invocada; siguiente reserva no cabe | 0.008666675 |
| 05 | 27 | Smoke y los seis runs completos | 0.033075650 |
| **Total** | **61** | **Cinco rondas, tres pares válidos** | **0.070565250** |

El usuario autorizó las rondas necesarias dentro del techo originalUS$0.10. Cada ronda se congeló antes de API con aprobación registrada derivada de esa autorización. No retries automáticos pagados; tras cada fallo se detuvo antes de preparar una configuración nueva. El límite56 era por ronda, no61 acumuladas prohibidas por una autorización única: la instrucción posterior autorizó rondas adicionales.

Se explicaron comandos exactos, se añadieron diagnósticos de tools rechazadas y se redujo contexto común irrelevante. El proxy opt-in mantuvo la cota bytesUTF8+16384; reserva tarifa corta solo si esa cota≤100000 y larga si mayor. Detiene si uso observado excede cota, aunque coste sea inferior a reserva. Defaults anteriores intactos. No se aumentó cap, presupuesto, acceso ni skill.

Suite local final: **229 pruebas pasadas**, sin fallos. Son checks de infraestructura con proveedor simulado; no evidencia de calidad del razonamiento. La última ronda sí usa API Anthropic real. Tarifas contrastadas con [documentación oficial de Anthropic](https://platform.claude.com/docs/en/about-claude/pricing); costes estimados por usage, no conciliación de factura. Todos los61 requests tuvieron usage conocido.

# Casos utilizados

- **L01, utilities:** recovered_kwh disponible después de scoring; history_kwh_90d previa válida. Outcome retrospectivo separado de input predictivo.
- **L02, suscripciones:** historia temporal y labels train disponibles antes del fit; clientes conocidos recurrentes y scaler ajustado solo en train.
- **L03, churn:** complaint_count sin ventana ni disponibilidad; fecha de exportación no determina disponibilidad al predecir.

Datos sintéticos pequeños, explicaciones explícitas y autor conocedor de expected: evaluación inicial guiada, no engagement real ni generalización.

# Resultados

| Caso | Contenido baseline | Contenido con skill | Diferencia observada |
|---|---|---|---|
| L01 | PASS | PASS | Ambos detectan el mecanismo posterior y conservan historia válida |
| L02 | FAIL | PASS con observaciones | Baseline añade justificación temporal falsa; treatment la evita |
| L03 | PASS | PASS con observaciones | Ambos reconocen incertidumbre y solicitan evidencia relevante |

La evaluación es semántica, no una búsqueda de frases. La distinción feature/outcome de L01B se acepta implícitamente: limita el hallazgo a las dos features declaradas y no condena el target retrospectivo. L03B propone exclusión provisional pendiente de evidencia, no eliminación definitiva; su descripción de incertidumbre se acepta aunque no use literalmente «No determinable».

## Formato, trazabilidad y brevedad separados

Todos los seis reportes persistidos tienen hashes de inputs correctos y fecha real. Los tres treatments invocaron Skill; ningún baseline lo hizo. Ningún input se alteró, pipeline se ejecutó, modelo se entrenó ni gate se aprobó.

**Formato/trazabilidad del contrato original:** baseline3/3, treatment0/3. Los tres treatments omiten la condición baseline/treatment del frontmatter solicitada por case.md. Skill/version no sustituyen ese campo. Se aceptan el namespace y anotación de versión de L03T semánticamente; su snapshot real sí corresponde a0.1.0. En L02B, «Verificaciones y límites» cumple el papel de Evidencia: no se exige un título literal.

**Cumplimiento conjunto contenido + contrato original:** baseline2/3, treatment0/3. La regla favorable no se cumple. El campo ausente identifica un fallo de contrato de salida, no tres razonamientos de leakage incorrectos.

**Brevedad añadida al cohort:** conteo whitespace del archivo completo. Baseline683/763/705palabras; treatment839/917/792. Baseline1/3 y treatment0/3 dentro de700. Añadiendo ese criterio operativo al cumplimiento conjunto: baseline1/3, treatment0/3. Se reporta aparte para no confundir la restricción añadida con los criterios iniciales de eficacia.

# Correctitud y fundamentación

L01: ambos sustentan recovered_kwh con disponibilidad posterior en4/4filas y su inclusión en FEATURE_COLUMNS; distinguen historia previa válida y no inventan fit/split. Treatment añade la relación descriptiva con target sin convertir alta señal en prueba independiente. La relación es una observación de muestra, no una estimación poblacional.

**L02B, error material:** H5 afirma que el target de train (principios de mayo, hasta mayo8) no se solapa con la ventana de treinta días previa al scoring de evaluation (junio2). Esa ventana sí cubre parte de principios de mayo. No hace falta inventar límites incluidos/excluidos: días interiores como mayo4–7 pertenecen a ambas ventanas. El solape no demuestra leakage porque los labels estaban disponibles antes del entrenamiento y el escenario puntúa clientes conocidos. La clasificación final es razonable, pero esta justificación es falsa; una clase acertada no subsana evidencia incorrecta.

L02T cubre disponibilidad de features/labels, fit train-only y recurrencia esperada; no condena el split ni exige grupos para este escenario. Su cautela sobre identidad/features por cliente es demasiado general: esas features pueden ser válidas para scoring recurrente si están disponibles. Debe expresar la condición operacional sin convertir recurrencia en contaminación automática.

L03: ambos separan exportación de disponibilidad y piden ventana/snapshot/código; no inventan un timestamp disponible. Treatment reconoce el target futuro legítimo. Observación sobre L03T: «si se construyó hasta junio1, no hay leakage temporal» debe exigir también disponibilidad efectiva al scoring, ya solicitada en sus preguntas. La conclusión global sigue siendo desconocida; no certifica seguridad actual.

# Cobertura, alucinaciones y accionabilidad

Contenido baseline2/3, treatment3/3 con observaciones no críticas. No hay nuevos falsos positivos **confirmados** de treatment ni timestamps inventados para resolver L03. Persisten lenguaje genérico sobre solape de entidades, conclusiones de ausencia a partir de código faltante y la necesidad de distinguir riesgo de proceso de evidencia de contaminación.

Ambas ramas proponen acciones útiles y proporcionales: excluir la feature intrínsecamente posterior, conservar historia válida, verificar proceso real y obtener disponibilidad desconocida. El reporte más largo no constituye por sí mismo una mejora.

# Eficiencia y coste de la skill

Solo los seis runs comparables, sin smoke ni intentos fallidos:

| Métrica observada | Baseline | Treatment |
|---|---:|---:|
| Requests | 12 | 12 |
| API estimada US$ | 0.012935940 | 0.017738335 |
| Tiempo agregado s | 76.93 | 84.60 |
| Output tokens, thinking incluido | 16107 | 16963 |
| Input fresco + cache creation + cache read acumulados | 113312 | 201899 |

Treatment costó **37.1% más** en esta muestra, diferenciaUS$0.004802395. Los conteos de entrada acumulan contexto/cache leído en múltiples requests: no son tokens únicos de dataset ni costo equivalente entre clases. Orden/cache/latencia afectan las mediciones; una ejecución por rama no permite generalizar el incremento.

# Resultado y decisión

La hipótesis de **mejora conjunta no se confirma**. Hubo una mejora puntual de contenido enL02, insuficiente para la regla de al menos dos casos, y regresión de trazabilidad. No repetir hasta obtener un resultado favorable ni modificar expected tras observar outputs.

**Recomendación: mantener experimental supervisada y modificar antes de otro experimento.** No promover a validated/stable ni afirmar eficacia general. Evaluación registrada localmente con el template canónico; Foundry canónico y madurez no modificados automáticamente. Una revisión humana/independiente sigue siendo necesaria para una decisión formal de madurez.

# Cambios recomendados

1. **Skill existente, no nueva skill:** contrato del caller prevalece sobre su plantilla; incluir los campos adicionales pedidos, condición cuando corresponda y límite de extensión. No inventar valores o versión verificada.
2. **Skill detect-leakage:** reemplazar «IDs repetidos ⇒ contaminación» por análisis del escenario operacional, features, disponibilidad y objetivo de generalización.
3. **Skill detect-leakage:** condicionar «segura» a ventana válida **y disponibilidad efectiva**; distinguir ausencia de evidencia de evidencia de ausencia cuando no hay código/split.
4. **Template/validator:** checklist de frontmatter requerido y hashes, con contenido revisado semánticamente; un validador de formato no decide mecanismos de leakage ni acepta gates.
5. **Runner:** conservar las correcciones verificadas de contexto, invocación nativa, diagnósticos y reservas. Registrar calidad de invocación y costo aparte de contenido.

Estas necesidades pertenecen a artefactos existentes; no crear tres candidates duplicados de detect-leakage para subsanar su misma capacidad. Propuestas detalladas en `reviewer-followup-05/RECOMMENDATIONS.md` dentro del paquete local de evaluación.

# Próximo experimento

Tras revisar/modificar la capacidad, usar cases nuevos menos guiados que separen: agregación previa pero disponibilidad tardía; recurrencia válida frente a memorización ilegítima; preprocessing global frente a fit train-only; join posterior; target encoding/resampling antes del split. Reviewer diferente del autor, orden predefinido y repeticiones dentro de un presupuesto nuevo autorizado. Este estudio no autoriza gasto adicional fuera del techo restante ni promoción automática.

# Evidencia

`runs/round-05/author-review.json`: revisión por criterio; `observed-metrics.json`: hashes/fecha/coste/tiempo; stdout y tool events: invocación y checks reales; reportes originales sin reparación. Configuración05 SHA256 `4cea884942d97aa2fa10a5d771ef6af496c76d54780e45f64d7dac9e4f9b591c`. Las rondas01–04 y sus fallos se preservan separadamente.
