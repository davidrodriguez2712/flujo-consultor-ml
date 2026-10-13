# Protocolo propuesto — evaluación de una capacidad

## Hipótesis

Añadir detect-leakage experimental0.1.0 mejora la identificación de mecanismos de información no disponible al predecir, evitando falsos positivos y reconociendo disponibilidad desconocida. No evaluar entrenamiento ni resultados de negocio. Los tres escenarios/datos son sintéticos y explícitos: prueba inicial de límites, no generalización ni independencia respecto del conocimiento del autor.

## Comparación controlada

Baseline y treatment comparten tarea, inputs, contrato de reporte, herramientas/lectura/escritura permitidas, modelo y mismo workflowOS congelado después del ajuste local. La única diferencia será la skill snapshot exacta en treatment; no actualizar OS/skill durante la comparación. Congelar runtime/configuración y su autorización antes de invocaciones. Contextos y cwd separados, mismo set de herramientas, no red ni modelos adicionales salvo llamada evaluada autorizada.

Orden propuesto: L01baseline/treatment, L02treatment/baseline, L03baseline/treatment. Una repetición inicial, seis ejecuciones; sin retries automáticos. Smoke técnico e instalación, si se requieren, se diseñan aparte y no cuentan como eficacia. No ejecutar con runner anterior tools-off: la tarea incluye inspección y persistencia. Si solo se inyecta el texto de la skill, declarar evaluación de instrucciones, no disponibilidad/invocación nativa. Validar qué skill/version carga realmente el runtime antes de atribuir resultado a instalación nativa.

## Contrato común

Cada rama entrega resumen breve y reports/leakage/audit.md. Estructura común: Resumen, Hallazgos, Evidencia, Preguntas abiertas, Recomendaciones. Hallazgos explican componente/mecanismo/fuente/confianza/severidad/recomendación; no exigir severidad idéntica cuando esté justificada. Frontmatter registra fecha real, inputs con hashes reales, estado y condición. Campo skill/version: baseline none/null, treatment detect-leakage/0.1.0; ninguna rama puede atribuirse una skill no cargada. Este contrato solo mide auditoría, no suministra respuestas particulares ni procedimiento completo de la skill.

Permitir inspeccionar inputs y ejecutar comprobaciones ad hoc deterministas con stdlib en memoria (conteos/timestamps/hashes); no entrenar modelos ni ejecutar pipeline.py, instalar paquetes, editar inputs o conectar servicios. Escritura solo reports/leakage/audit.md dentro de workspace nuevo; archivo ausente al comenzar. Tools/configuración concretos se verifican antes de run, no se presuponen por este documento.

## Expected privado y checks

reviewer/* fuera del cwd y de inputs del agente; una ruta declarada privada no garantiza aislamiento: configuración posterior debe comprobar los accesos reales. expected fijo antes de outputs. Checks locales pueden verificar filas, tiempos, orden declarativo del fit y existencia/no sobrescritura/hash/estructura del reporte; presencia de heading o key no certifica mecanismo correcto. No usar solo presencia de frases para puntuar contenido.

Criterios por case: mecanismo/fundamentación/cobertura, ausencia de falsos positivos/fechas inventadas, incertidumbre útil, acción recomendada proporcional y respeto de alcance. Registrar correctitud, cobertura, fundamentación, accionabilidad, coste/tokens/tiempo separados; sin score compuesto. PASS exige todas obligaciones esenciales y ninguna prohibición crítica; formato/persistencia y contenido se reportan separados.

L01: recovered_kwh posterior al prediction timestamp es leakage confirmado; historia previa válida. L02: historia disponible, split temporal y fit solo train son coherentes con scoring recurrente de clientes conocidos; no afirmar leakage por entidades repetidas o señal predictiva alta. L03: timestamp de exportación no determina disponibilidad de complaint_count; información faltante requiere No determinable/pregunta concreta, no fecha inventada.

## Interpretación y review

Propuesta de regla inicial a revisar junto al paquete: señal favorable si treatment mejora cumplimiento conjunto en al menos dos casos, no empeora otro y no introduce falsos positivos confirmados, permisos o timestamps inventados. Si baseline ya cumple todos, declarar ausencia de mejora observada/efecto techo. Una ejecución por rama no acredita estabilidad ni generalización. Igualdad de clases con mecanismo falso no es acierto completo.

Separar AUTHOR/RUNNER/REVIEWER. En esta preparación el autor conoce fuentes y expected; no declarar review independiente ni ciega. Antes de decidir madurez, solicitar reviewer diferente (David puede revisar las citas y criterios). Si solo revisa el autor, resultado preliminar con esa limitación, sin promoción automática. Usar templateevaluation canónico para el resultado futuro. Mantener uso experimental supervisado dentro de límites; evaluated no significa PASS.

## Pendientes antes de run

Revisión humana del paquete/expected/regla. Elección y verificación de runtime/modelo/tools/instalación/aislamiento y salida. Configuración congelada, presupuesto explícito y aprobación vinculada. Reviewer distinto por acordar. Ninguna llamada pagada autorizada por preparar este paquete.
