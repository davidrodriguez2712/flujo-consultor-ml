# Primer piloto supervisado de ACOS

Estado: piloto de churn/retención inicializado en `pilots/churn-retencion-sintetico/`. El usuario no dispone de datos y autorizó generarlos; los inputs son 100% sintéticos. Discovery requiere revisión humana y ningún gate está aprobado.

## Objetivo

Usar ACOS en un caso concreto de consultoría Data & AI para comprobar que el workspace permite avanzar con contexto, outputs reproducibles, revisión humana y continuidad entre sesiones. Evaluar por separado la utilidad de las capacidades experimental empleadas.

## Inputs necesarios para inicializar

Respuestas recibidas: churn/retención, sin dataset existente. Se creó un caso ficticio de suscripciones con generator reproducible. La empresa, capacidad de 50 contactos y KPI son propuestas de laboratorio para revisión, no datos de cliente.

- Caso y decisión de negocio que se quiere apoyar.
- Ruta de los datos o del proyecto existente; si no hay datos, registrar esa ausencia como bloqueo.
- Estado de entrada: problema inicial, datos disponibles o solución heredada.

Después de inspeccionar esos inputs, confirmar con el usuario KPI, unidad, horizonte, owner, entregable y restricciones que no se puedan deducir con evidencia. El nombre del cliente puede ser confidencial. No completar definiciones de negocio a partir de nombres de columnas.

## Recorrido

1. Inspeccionar únicamente las fuentes indicadas por el usuario y registrar disponibilidad, formato y límites.
2. Preparar el project-profile y mostrar composición, skills, versiones, preconditions y gaps para revisión.
3. Ejecutar `acos init` sobre una subcarpeta nueva; conservar las fuentes originales.
4. Leer MANUAL, STATE y contratos; definir una primera tarea acotada con input, output y aceptación.
5. Ejecutar la tarea y conservar evidencia reproducible. Si faltan datos o definiciones, dejar un bloqueo y la solicitud concreta.
6. Ejecutar `acos validate`, corregir los checks deterministas y presentar el contenido al reviewer humano. No registrar PASS humano antes de su revisión.
7. Tras aprobación del gate pertinente, registrar reviewer/evidencia/decisión y avanzar el estado explícitamente.
8. Cerrar la sesión actualizando vistas y pendientes; abrir otra sesión con `continuemos` y comprobar que retoma el estado vigente.
9. Entregar informe del piloto con resultados, fallos, gaps, feedback de skills y próximos pasos.

## Evaluación del flujo

| Criterio | Evidencia |
|---|---|
| Workspace pertinente | Módulos seleccionados y excluidos con motivo; profile/manifest |
| Trabajo guiado | MANUAL/next identifican una tarea ejecutable y sus outputs |
| Reproducibilidad | Inputs, método, parámetros y checks conservados |
| Bloqueos visibles | Estado canónico identifica qué falta y por qué afecta la decisión |
| Gates respetados | Checks, revisión humana y avance trazables; sin PASS por plantilla existente |
| Continuidad | Una sesión nueva retoma objetivo, bloqueos y siguiente acción correctos |
| Feedback útil | Fallo o mejora concreta ligada a tarea, versión y evidencia |

Una prueba inconclusa se registra como tal; no se convierte en éxito por existir el entregable.

## Evaluación de skills

Seleccionar una primera tarea que pueda compararse con inputs y aceptación iguales, por ejemplo entendimiento de datos o diseño de validación, según el caso confirmado. No dar por hecho qué skill corresponde antes de resolver el perfil.

- Baseline: sesión independiente con contexto del proyecto y pautas del OS, sin cargar la skill que se evalúa.
- Tratamiento: otra sesión independiente con los mismos inputs, tarea y aceptación, incorporando la skill seleccionada.
- Registrar runtime/modelo, versión de skill, inputs, outputs, tiempo, correcciones humanas y checks verificables. Conservar las diferencias de configuración o contexto que impidan una comparación justa.
- Comparar omisiones, errores, trazabilidad, utilidad para la decisión y esfuerzo de corrección. Un output más largo no implica mejora.
- Una sola comparación es evidencia exploratoria; requiere más casos para justificar una promoción. Mantener la madurez actual hasta seguir la evaluación canónica del Foundry.

El registro se conserva dentro del proyecto del piloto. Antes de trasladar evidencia al Foundry, revisar y anonimizar. No crear nuevas fichas ni reabrir las decisiones existentes solo por detectar una capacidad parcial en el catálogo.

## Cierre

El piloto puede concluir como útil, parcial, fallido o inconcluso, con evidencia. El informe separará comportamiento del compiler, operación del runtime, calidad de los outputs y utilidad de cada capacidad evaluada. Las conclusiones de negocio quedarán limitadas por los datos y la revisión disponible.
