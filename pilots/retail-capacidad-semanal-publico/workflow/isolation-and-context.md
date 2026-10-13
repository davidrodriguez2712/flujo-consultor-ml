# Aislamiento y contexto del proyecto

Este módulo define cómo limitar el contexto de un proyecto y qué información debe persistir entre sesiones. Un nombre de carpeta, un prompt o un worktree ayuda a organizar, pero no constituye una barrera de seguridad.

## Separación por cliente y proyecto

- Mantener un repositorio/entorno por proyecto con identidad, recursos y permisos autorizados por el cliente/empleador.
- Iniciar el harness en el proyecto específico. No abrir por defecto una carpeta padre que exponga varios clientes o repositorios.
- Un worktree comparte el repo/origen y no separa clientes ni permisos.
- Aislar credenciales, conectores, bases, schemas, storage, tracking y destino de logs con alcance adecuado.
- No conectar memoria o búsqueda global de forma que una sesión de un cliente pueda recuperar material de otro.
- Reutilizar metodología genérica; no reutilizar consultas, datos, resultados o casos identificables de un cliente en otro sin autorización.
- No trasladar datos sensibles al equipo personal ni al Foundry para resolver una limitación de acceso.

## ACCESS.md cuando se usan datos o herramientas

Antes de acceder a fuentes reales, completar lo que corresponda:

| Elemento | Pregunta que debe responder |
|---|---|
| Clasificación | ¿Qué clase de información se procesará y qué reglas aplican? |
| Owner/aprobador | ¿Quién concede el acceso y acepta el uso? |
| Sistemas permitidos | ¿Qué fuentes, entornos, conectores y harnesses están autorizados? |
| Alcance | ¿Solo lectura? ¿Qué schemas, objetos, períodos o poblaciones? |
| Escritura | ¿Dónde puede guardar código, artifacts, logs y outputs? |
| Retención | ¿Qué se conserva, por cuánto tiempo y dónde? |
| Revisado | ¿Quién confirmó el contenido y cuándo debe revisarse otra vez? |

Una pseudonimización no implica automáticamente anonimato ni permiso para exportar. Si una acción cambia el nivel de exposición o alcance, detenerse y resolver el acceso primero.

## Cargar contexto de forma progresiva

Al iniciar una sesión, consultar en este orden y solo ampliar según la tarea:

1. instrucciones del proyecto (`AGENTS.md` y adaptadores realmente utilizados);
2. brief/`PROJECT.md`, ID del proyecto y solicitud activa;
3. `ACCESS.md` si hay datos o herramientas restringidos;
4. `STATE.md` y la tarea activa para retomar el trabajo;
5. contratos, métricas, validación, decisiones, findings y código que sean pertinentes.

No cargar todo el repositorio o todos los playbooks al contexto del agente. El ciclo y las rutas están en [`project-lifecycle.md`](project-lifecycle.md); cargar solo el playbook de la ruta seleccionada.

## Qué conservar y qué evitar

- Persistir decisiones, definiciones, supuestos de alto impacto, resultados aceptados, bloqueos y siguiente paso cuando deban sobrevivir a la sesión.
- Mantener consultas/código y evidencia del trabajo dentro del repositorio o sistema autorizado del proyecto.
- Referenciar documentos corporativos desde sus sistemas autorizados en lugar de crear copias innecesarias.
- No guardar secretos, credenciales ni datos sensibles en prompts, commits, logs, snapshots o artifacts sin autorización.
- Evitar mantener manualmente dos estados competidores. Si existe un tracker aprobado, su estado es canónico; si no, usar un índice local mínimo.
- El historial del chat puede ayudar, pero no es la única memoria del proyecto.

## Fuente canónica por tipo de información

| Información | Fuente canónica propuesta | Cuándo crear/persistir |
|---|---|---|
| Prioridad y estado de tarea | Tracker aprobado; si no existe, índice local mínimo. | Cuando hay varias tareas o coordinación que debe retenerse. |
| Pregunta, decisión, scope y acceptance | Brief/`PROJECT.md`. | En todo trabajo con alcance acordado. |
| Permisos, fuentes y herramientas | `ACCESS.md` más sistema de acceso autorizado. | Cuando se usan datos o herramientas del cliente. |
| Grain, definiciones, disponibilidad de datos | `DATA_CONTRACT.md` o documento equivalente. | Cuando análisis/modelado depende de semántica de datos. |
| Diseño de validación | `VALIDATION.md` o artifact de diseño relevante. | Cuando hay experimento o evaluación de modelos que requiera definición explícita. |
| Decisiones y supuestos materiales | Registro de decisiones/supuestos. | Cuando una decisión debe sobrevivir o un supuesto cambia el resultado. |
| Estado de ejecución/handoff | `STATE.md`. | Al pausar/cerrar sesión o cuando hay bloqueo/siguiente paso. |
| Código, consultas y evidencia | Repo y artifacts autorizados del proyecto. | Según el método y las reglas de almacenamiento. |
| Skills, agents, cases y evaluaciones | David Skill Foundry. | Solo para capacidades genéricas; el proyecto referencia IDs/versiones si corresponde. |
| Entrega publicada | Sistema de entrega aprobado. | Cuando se envía/acepta un deliverable. |

Los trackers referencian evidencia; no sustituyen el repo como fuente de código y artifacts técnicos. Los artifacts del cliente permanecen en el proyecto: el proceso de derivación de capacidades al Foundry está en [`capability-lifecycle.md`](capability-lifecycle.md).

## Separación del material Foundry

Las guías generales pueden indicar nombre, estado y versión de una capacidad y enlazar a la ubicación del Foundry configurada localmente. No registrar un path absoluto a la carpeta personal del Foundry en un repositorio compartido con cliente. Nunca copiar al repositorio del proyecto sus templates de candidates, skills, agents o evaluaciones como si fueran archivos del cliente.
