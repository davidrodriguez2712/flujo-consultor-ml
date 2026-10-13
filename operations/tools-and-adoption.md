# Herramientas y adopción

Este módulo describe adaptadores opcionales para ejecutar el OS en distintos proyectos y runtimes. El proceso consultivo debe poder comenzar con archivos Markdown, las herramientas ya autorizadas y revisión humana; ninguna integración listada aquí es requisito general.

Consultar [`../workflow/capability-lifecycle.md`](../workflow/capability-lifecycle.md) para distinguir madurez en David Skill Foundry de instalación o disponibilidad local. Las reglas de acceso y fuentes canónicas están en [`../workflow/isolation-and-context.md`](../workflow/isolation-and-context.md).

## Comprobación antes de usar una capacidad

Antes de solicitar o depender de una skill/agent:

1. Confirmar que el nombre aparece en el runtime/harness activo y que se puede invocar.
2. Revisar su fuente y versión disponible, si el entorno las expone; consultar el Foundry como fuente canónica para su estado de madurez.
3. Confirmar que su alcance y precondiciones coinciden con la tarea y que los accesos requeridos están autorizados.
4. Acordar qué output se espera y cómo se revisará. Tratar resultados experimentales como borradores sujetos a verificación.
5. Si no está disponible, continuar con un procedimiento manual documentado o declarar la limitación; no simular su ejecución.

`stable` en Foundry indica madurez según ese sistema. No garantiza que la capacidad esté instalada, visible, habilitada o autorizada en todos los proyectos. De igual forma, un archivo Markdown que explique un procedimiento no se convierte por eso en una skill nativa invocable. Un `runbook` especifica pasos que una persona/agente puede seguir; su automatización requiere implementación y verificación aparte.

## Adaptadores posibles

Activar solo los que resuelvan una necesidad real y estén permitidos en el entorno:

| Adaptador | Uso posible | Comprobación/límite |
|---|---|---|
| Harness de agente y skills | Leer contexto, ejecutar tareas y usar capacidades instaladas. | Verificar disponibilidad, versión, permisos y contexto que puede consultar. |
| Linear u otro tracker | Estado, owner, dependencias y fechas. | El tracker puede reflejar el estado operativo, pero no sustituye los artifacts metodológicos o su evidencia. |
| Orca u otro gestor de worktrees | Aislar cambios de código y facilitar revisión. | Una carpeta o worktree no es una barrera de seguridad ni concede acceso al repositorio. |
| MCP y conectores | Consultar fuentes o aplicaciones desde el agente. | Revisar identidad, scopes, datos expuestos y permiso del cliente antes de conectar. |
| Superpowers / OpenSpec | Apoyar diseño, planificación o ejecución de cambios de software. | Usar cuando el problema requiera desarrollo; no exigirlos para análisis o consultoría documental. |
| Python, SQL y notebooks | Extraer, perfilar, analizar y validar datos. | Usar entornos aprobados, reproducibilidad, control de acceso y evidencia de consultas/código. |
| MLflow u otra plataforma ML | Registrar runs, modelos, métricas o artifacts. | Activar si existe flujo ML y plataforma aprobada; no asumir que es necesaria para análisis. |
| Figma, Figma MCP, shadcn, 21st.dev | Explorar, inspeccionar o implementar experiencias de producto. | Ver [`../playbooks/product-ui-and-prototyping.md`](../playbooks/product-ui-and-prototyping.md); stack y conectores dependen del cliente. |

Una herramienta puede cambiar la forma de ejecutar un paso, pero no elimina sus gates de método, revisión, acceso o aprobación.

## Inicio mínimo en un proyecto

1. Confirmar el repositorio/espacio autorizado y las reglas del cliente.
2. Leer este OS y adaptar solo las instrucciones que deban ser visibles en ese entorno.
3. Crear el brief y los artifacts requeridos por la primera decisión; no generar carpetas ni placeholders sin uso.
4. Registrar fuentes canónicas, límites de acceso, owner, objetivo, aceptación y siguiente gate.
5. Comprobar las herramientas y capacidades disponibles; mantener manual cualquier paso sin soporte.
6. Al cierre, preservar decisiones, evidencia, límites y handoff en el espacio del proyecto.

### Instrucción de bootstrap adaptable

Usar como punto de partida y completar según el cliente/harness. No pegar secretos, permisos amplios ni contenido de otros clientes.

> Aplica el Agentic Consulting OS de este repositorio al proyecto actual. Antes de crear o modificar archivos, identifica el objetivo, la decisión que debe habilitarse, el scope, los artifacts existentes, el owner y las restricciones de acceso. Conserva el contenido existente y consulta los módulos pertinentes según la etapa y ruta; no dupliques fuentes canónicas ni crees placeholders innecesarios. Verifica qué herramientas y skills están disponibles en este runtime. Ejecuta solo acciones autorizadas dentro del write scope acordado, conserva evidencia suficiente para revisar tus conclusiones y declara supuestos, limitaciones y trabajo pendiente. Detente y escala si faltan permisos, datos o una decisión humana necesaria.

## Adopción gradual

Adoptar el OS por etapas, con un ejemplo sintético primero:

1. **Orientación:** leer el mapa y ubicar ciclo, módulos y plantillas.
2. **Práctica sintética:** recorrer un caso ficticio, sin credenciales ni información de clientes.
3. **Piloto autorizado:** aplicar el flujo mínimo en un proyecto de bajo riesgo, con consultor responsable y revisiones proporcionales.
4. **Retrospectiva:** identificar pasos útiles, fricción, omisiones y artifacts redundantes.
5. **Mejora:** corregir el playbook; si aparece una capacidad reusable, registrar la observación y evaluar el `candidate gate` del Foundry.
6. **Automatización:** considerar automatizar solo después de observar valor en un procedimiento manual recurrente, acotado y verificable; conservar control humano y fallback.

Un piloto no convierte automáticamente un procedimiento en skill ni autoriza transferir evidencia sensible al Foundry. Aplicar el ciclo y los límites definidos en [`../workflow/capability-lifecycle.md`](../workflow/capability-lifecycle.md).

## Señales para evaluar adopción

Primero establecer una línea base comparable; luego acordar metas apropiadas al tipo de trabajo. Posibles señales:

- tiempo desde intake hasta la decisión acordada;
- proporción de entregables que pasan revisión sin correcciones sustantivas;
- errores/retrabajo atribuibles a definiciones, datos o handoffs incompletos;
- proporción de afirmaciones con fuente, cálculo o evidencia trazable;
- tareas detenidas/replanificadas por acceso, scope o acceptance ambiguos;
- comprensión y uso del delivery por parte de su audiencia/owner;
- pasos repetidos donde una capacidad reusable reduciría carga sin bajar calidad.

Definir para cada medida alcance, numerador/denominador, fuente, período y exclusiones. No inferir impacto causal del OS a partir de una comparación simple antes/después si cambiaron equipo, dificultad, herramientas o volumen. No anunciar porcentajes de productividad sin evidencia comparable.

## Prácticas de operación

- Usar tracker, repositorio, Figma o plataforma como fuente canónica solo para el tipo de información que realmente controla.
- Evitar copiar un estado a múltiples lugares; enlazar el artifact responsable.
- Mantener instrucciones específicas del cliente y permisos dentro de su espacio autorizado.
- Declarar fallos de integración y continuar manualmente solo si el método sigue siendo válido y autorizado.
- Revisar si el runtime cambió antes de afirmar que una skill o herramienta está disponible.
- Retirar o ajustar adaptadores cuando ya no sean necesarios; el OS no depende de un vendor.
