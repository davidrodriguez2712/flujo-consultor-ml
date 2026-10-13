# Producto, UX, UI y prototipos

Esta ruta se consulta únicamente cuando la solución necesita una interacción de usuario nueva o modificada. No se activa por producir un modelo, un reporte o una presentación. Sus pautas adaptan un workflow frontend especializado a un contexto consultivo Data & AI: primero la tarea y la decisión; después el nivel de diseño necesario.

El recorrido general del OS está en [`../workflow/project-lifecycle.md`](../workflow/project-lifecycle.md); autoridad y QA, en [`../workflow/execution-and-qa.md`](../workflow/execution-and-qa.md).

## Gate de activación

Antes de diseñar, responder:

1. ¿Quién usará el resultado y qué tarea necesita completar?
2. ¿Qué decisión o acción habilitaría la interfaz?
3. ¿El canal actual (CRM, hoja, dashboard, reporte, API o proceso manual) ya permite esa tarea con calidad suficiente?
4. ¿La nueva interfaz reduce un problema concreto de adopción, tiempo, error o riesgo?
5. ¿Hay owner, datos, reglas, permisos y entorno suficientes para ponerla en uso?

Si no hay una tarea/interacción nueva, volver a la ruta apropiada: `ANALYSIS`, `MODEL`, `RESEARCH` o `DELIVERY`. Un score en CSV no exige dashboard. Una interfaz sin owner, dato disponible ni siguiente acción no está lista para diseño.

## 1. Aclarar experiencia y alcance

Para una UI que pasa el gate, acordar un brief proporcional con:

- problema actual y proceso existente;
- usuario principal y roles secundarios, tareas y permisos;
- acción principal, outcome esperado y criterio de éxito;
- decisión que ayuda a tomar y quién conserva autoridad;
- información/data dependencies, frescura y calidad;
- reglas de negocio, restricciones de seguridad y access;
- scope dentro/fuera y open questions.

Separar requisitos, supuestos y preguntas abiertas. No inventar actores, endpoints, datos o decisiones. Si el cambio es trivial dentro de un flujo establecido, basta un task brief y criterios de aceptación; no generar una especificación UX completa.

## 2. Planificar la UX cuando el cambio lo necesita

`ui-planning` puede apoyar cambios no triviales: feature nueva, pantalla nueva, cambios importantes de flow/navegación, nuevos roles o una interacción principal que aún no está estructurada. Produce, en la profundidad adecuada:

1. user flows primarios, alternativos y de error;
2. Information Architecture y relación con navegación/producto actual;
3. screen inventory, con justificación de cada pantalla en un flow;
4. screen specifications (purpose, contenido, acciones, reglas y jerarquía);
5. states relevantes: loading, empty, error, success y parciales;
6. data dependencies y disponibilidad (existe/no existe/no determinable);
7. wireframes estructurales de baja fidelidad si ayudan a revisar la estructura;
8. supuestos y preguntas abiertas consolidadas.

Una pantalla sin propósito ni paso de flow que la justifique se cuestiona. Los wireframes estructurales no fijan colores, tipografía, tokens o estética. No producir la misma documentación para una pantalla pequeña y un producto completo.

Estado observado en el Foundry: `ui-planning`, `experimental`, versión `0.1.0`. Es una ayuda en prueba, no autoridad de producto. Revisar su output y pedir decisión humana sobre preguntas que afecten scope, negocio o permisos.

## 3. Decidir qué prototipo o diseño hace falta

Usar el artifact mínimo que permita tomar la siguiente decisión:

| Incertidumbre pendiente | Artifact apropiado |
|---|---|
| No está claro si una interfaz hace falta | Mapa del proceso actual y alternativa de uso del canal existente. |
| No está claro el orden de pasos o información | User flow, Information Architecture o wireframe low-fidelity. |
| Hace falta acordar apariencia, componentes o navegación con stakeholders | Figma/prototipo visual en el nivel necesario para revisión. |
| La implementación debe seguir un Design System del proyecto | Diseño aprobado y handoff con tokens/componentes existentes. |
| Solo hace falta confirmar un cálculo o regla | Tabla, ejemplo de salida o acceptance criteria; no construir un prototipo visual completo. |

Figma es opcional. High-fidelity se justifica cuando aporta una decisión visual real, facilita revisión con stakeholders/usuarios o reduce ambigüedad de implementación. No es requisito para probar el concepto ni para todo proyecto de datos.

### Gate humano de diseño

Registrar el estado del artifact de diseño como `DRAFT`, `REVIEW` o `APPROVED`, con owner/fecha cuando se utilice Figma como autoridad visual. Solo una referencia aprobada sirve como fuente para un handoff definitivo. Anotar decisiones, feedback pendiente y versiones; no implementar una exploración como si estuviera aprobada.

La aprobación visual no autoriza uso de datos, instalación, despliegue ni publicación. Estos permisos siguen el contrato de proyecto.

## 4. Pasar de Figma a implementación

`figma-handoff` guía la traducción del diseño aprobado hacia tokens, Design System, componentes y código existentes. Úsala solo cuando se puedan inspeccionar los inputs necesarios:

- referencia Figma identificable (aprobada para un handoff definitivo);
- repo de implementación accesible y autorizado;
- Design System/tokens existentes, aunque sean parciales;
- operación delimitada: pantalla, componente, token, variant o auditoría.

El handoff verifica/recomienda correspondencias; no toma decisiones estéticas, no implementa ni modifica Figma. No inventa tokens, variants o componentes. Si el proyecto no tiene Design System/repositorio, la skill no aplica: documentar un handoff funcional ligero (reference, propósito, flows, estados, reglas, datos y acceptance), sin simular `PASS` de token/component mapping.

Estado observado en el Foundry: `figma-handoff`, `experimental`, versión `0.1.0`. Confirmar la versión disponible y revisar el handoff. Figma y el repositorio pueden ser autoridad sobre aspectos distintos: la referencia visual aprobada orienta apariencia; el repo define comportamiento y código real.

## 5. Implementación cuando esté en alcance

Separar diseño de ejecución. Antes del build confirmar:

- pantalla/flow aprobado o criterios funcionales suficientes;
- reglas y data dependencies aclaradas o marcadas;
- criterios de aceptación y manejo de estados definidos;
- repositorio, stack, design tokens, componentes y herramientas autorizados;
- write scope y reviewer acordados.

Usar el stack del cliente si está permitido. Claude Code, React/Next.js, Figma MCP, shadcn, 21st.dev y Orca pertenecen a posibles adaptadores del workflow frontend, no a requisitos del OS. Reutilizar componentes solo si el repo/design system los ofrece; no asumir que están instalados.

Si implementación no forma parte del encargo, entregar especificación/handoff y dejar explícito que no hay UI ejecutable.

## 6. Validar por separado

No usar un único PASS para afirmar cosas distintas:

| Validación | Pregunta | Evidencia posible |
|---|---|---|
| Uso/usabilidad | ¿Usuarios representativos pueden completar la tarea y entender qué hacer? | Observación de tarea, feedback y problemas; si no se prueba con usuarios, declararlo. |
| Funcional/reglas | ¿Los controles, permisos, cálculos, outcomes y errores obedecen criterios? | Acceptance, checks del contrato y resultados de interacciones. |
| Visual | ¿La UI implementada concuerda con la referencia/criterios y states/viewports declarados? | Capturas, viewport, estado, diferencias y re-chequeo tras correcciones. |
| Accesibilidad | ¿La interfaz puede ser percibida/operada con los requisitos pertinentes? | Evaluación accesible apropiada al alcance; visual QA no la sustituye. |
| Datos/modelo | ¿La cifra/score tiene semántica, calidad y validez de uso? | Contrato, validación técnica y límites del modelo; consultar playbooks analíticos. |

`visual-qa` se emplea después de implementar una UI y requiere app ejecutable, browser/tool disponible, pantalla/estados conocidos y referencia o criterio declarado. La skill actual está orientada a Orca Browser/Design Mode. Si Orca o el entorno faltan, no afirmar que la skill se ejecutó; declarar qué revisión sí fue posible y qué quedó pendiente.

Estado observado en el Foundry: `visual-qa`, `experimental`, versión `0.1.0`. Su revisión visual es asistida; el resultado no reemplaza revisión funcional, usabilidad con usuarios ni aceptación humana.

No exigir pixel-perfect. Revisar, en los viewports incluidos en alcance, layout, jerarquía, texto/truncamiento, overflow, componentes y estados reales; registrar lo no probado. Corregir y volver a revisar las áreas afectadas. No reportar console/network limpios si no se inspeccionaron.

## 7. Consideraciones para UI con resultados Data/AI

Aplicar lo que corresponda al modelo de uso y al riesgo:

- indicar qué significa el resultado, para qué población/período aplica y cuándo se actualizó;
- mostrar data freshness, incompletitud o no-result cuando esos estados alteren una decisión;
- no llamar `probabilidad`, `impacto`, `uplift` ni `recomendación` a algo que el modelo no estima;
- presentar uncertainty/calibration solo si existe evidencia adecuada y una explicación comprensible para el usuario;
- mostrar razones, límites o warnings solo cuando sean válidos, útiles y aprobados;
- definir revisión/override humano, quién es responsable y cómo escalar casos no soportados;
- evitar una decisión automática o una jerarquía oculta si el alcance solo autoriza decision support;
- aplicar permisos, minimización de datos, auditabilidad y requisitos del cliente.

Un ranking puede optimizar la carga de trabajo de una persona; no implica que la acción cambie el outcome. Consultar [`experiments-and-models.md`](experiments-and-models.md) para propensión, causalidad e incertidumbre.

## Artifact de salida y cierre

Persistir lo mínimo que permita avanzar:

- brief UX y preguntas abiertas si el problema/flujo no estaba definido;
- screen specs/wireframe/Figma si se acordó ese nivel;
- approval state, versión y link/node de referencia;
- handoff Figma-code solo cuando sus precondiciones existan;
- acceptance y matriz de estados/viewports para UI implementada;
- reporte de revisión que distinga probado, no probado y pendiente.

Usar templates del proyecto y no escribir en `reports/` o repos del cliente sin autorización. Actualizar `STATE` con artifact, gate alcanzado, limitación y siguiente acción. No convertir `ui-planning`, `figma-handoff` o `visual-qa` en candidates estables por usarlas; toda evolución sigue el ciclo de [`capability-lifecycle.md`](../workflow/capability-lifecycle.md).

## Idioma

Redactar la documentación del OS y los artifacts operativos (briefs, screen specs, wireframes anotados, handoffs y reportes) en español. Conservar en inglés nombres de skills, APIs, componentes, props, tokens y términos técnicos cuando mejoren precisión. El texto visible de una UI sigue el idioma/localización acordados para sus usuarios, que puede diferir del idioma de esta documentación.
