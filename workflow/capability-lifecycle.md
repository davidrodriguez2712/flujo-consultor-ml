# Ciclo de vida de capacidades reutilizables

Este módulo conecta el trabajo de consultoría con David Skill Foundry. El Foundry conserva las plantillas, casos, evaluaciones y autoridad para promover capacidades. El OS no mantiene una segunda copia del catálogo ni decide sus estados.

## Qué puede derivarse al Foundry

Primero clasificar el aprendizaje:

| Tipo | Qué es | Destino habitual |
|---|---|---|
| Conocimiento | Información, principio, decisión o aprendizaje que conviene recordar. | Contexto o registro de decisiones del proyecto; conocimiento genérico en la documentación apropiada. |
| Procedimiento puntual | Pasos útiles para una sola situación/proyecto, sin evidencia suficiente de repetición. | Nota del proyecto o handoff. No convertirlo automáticamente en skill. |
| Skill candidata | Hipótesis sobre cómo ejecutar una capacidad que podría reaparecer. | `candidates/` del Foundry, usando su `templates/candidate.md`; revisar el candidate gate antes de pasar a experimento. |
| Agent candidato | Hipótesis de una responsabilidad especializada que requiere objetivos y límites de autoridad propios. | `candidates/` del Foundry; distinguir el rol de la secuencia completa de una skill. |

Una skill describe principalmente **cómo hacer** una capacidad. Un agent describe principalmente **quién asume una responsabilidad**, qué decisiones puede tomar, qué herramientas/skills puede usar y con qué límites. No toda tarea repetida necesita un agent.

## Disparador y candidate gate

Registrar una observación cuando haya evidencia o una fuente que describa un problema que podría volver a ocurrir. Puede documentarse como candidate con evidencia limitada y decisión pendiente; no equivale a aprobar un experimento. Antes de pasar a experimental, responder las seis condiciones canónicas del Foundry:

1. ¿Existe un problema real?
2. ¿Puede volver a aparecer?
3. ¿Existe un procedimiento o responsabilidad identificable?
4. ¿Pueden definirse inputs?
5. ¿Puede definirse un output?
6. ¿Existe alguna forma de verificar el resultado?

Si no pasa el gate, conservarlo como conocimiento/patrón, reformularlo o rechazarlo. Un buen resultado puntual no es evidencia suficiente para crear una skill.

Al documentar el candidate en el Foundry, usar `templates/candidate.md`. No cambiar ni copiar allí el KPI, los resultados o los datos del cliente sin autorización. Cuando no se pueda reutilizar evidencia real, formular el problema sin detalles identificables y preparar cases sintéticos. El Foundry mantiene también los templates canónicos `SKILL.md`, `agent.md`, `case.md`, `expected.md` y `evaluation.md`; este playbook no los duplica.

## Flujo en el Foundry

```text
problema o fuente
  → candidate y candidate gate
  → capacidad experimental
  → cases y expected separados
  → baseline y treatment comparables
  → checks deterministas
  → review independiente
  → evaluation y decisión humana
  → mejorar / rechazar / validar / promover
```

El runner no recibe `expected.md` durante la ejecución cuando el procedimiento de evaluación exige mantenerlo oculto. No se modifican los criterios tras ver el resultado para favorecer una capacidad. La evidencia registra el nombre y versión exactos evaluados. Si una falla real reaparece, puede originar un nuevo case sin borrar los anteriores. El Foundry Reviewer puede recomendar; no promociona a `stable`.

Consultar `AGENTS.md` y los templates vigentes del Foundry para el proceso formal, thresholds y estructura actual. Los ejemplos de este módulo no reemplazan esas reglas.

## Uso por estado

Esta tabla establece una política de consumo del OS; el significado formal y la transición de estados pertenecen al Foundry.

| Estado del Foundry | Uso operativo en proyectos |
|---|---|
| `candidate` | Hipótesis pendiente; no invocarla como una capacidad confiable. |
| `experimental` | Probar solo en alcance controlado, con supervisión y revisión del output. Declarar que es experimental si afecta una decisión de trabajo. |
| `evaluated` | Consultar cases, evaluation, fallos y decisión. El estado dice que fue evaluada; no implica que la hipótesis se confirme. |
| `validated` | Probar en adopción supervisada y dentro de contextos/dominios respaldados por evidencia. Registrar fallos fuera de ese ámbito. |
| `stable` | Uso normal de la versión evaluada, respetando límites y condiciones de uso. Un cambio relevante requiere la reevaluación que determine Foundry. |
| `rejected` | No usar como capacidad; mantener el registro y su justificación. |
| `deprecated` | No iniciar nuevos usos; completar o migrar usos vigentes de acuerdo con la decisión del Foundry. |

No interpretar `evaluated` como PASS: abrir el resultado y leer si la hipótesis se confirmó, parcialmente confirmó o no se confirmó. Una versión posterior no hereda automáticamente la evidencia de una versión evaluada antes.

## Madurez, instalación y adopción

Son tres hechos distintos:

1. **Madurez Foundry:** estado y versión de la fuente canónica.
2. **Disponibilidad del runtime:** si el harness actual realmente expone la skill/agent y qué versión carga.
3. **Adopción del proyecto:** si los límites, herramientas y datos autorizados permiten usar esa capacidad aquí.

Antes de invocarla, comprobar el nombre y la versión visibles en el runtime. Una distribución a Codex, Claude Code u otro entorno debe conservar la referencia a la fuente canónica y la versión; no editar una copia instalada como si fuera el original. Una instrucción Markdown de `procedures/` o `playbooks/` no es una skill nativa salvo que esté instalada y el runtime la reconozca.

Si no se conoce el estado, versión o instalación, declararlo como no determinado y no asumir que está disponible. Una skill `experimental` puede servir como apoyo de una prueba revisada; no puede ser la única garantía de un entregable sensible.

## Registro en el proyecto

Cuando la observación proviene de un proyecto:

- registrar en la retrospectiva, `STATE` o decisión del proyecto una frase sin información confidencial: problema observado, fecha/contexto general y por qué podría repetirse;
- registrar el ID/ruta del candidate del Foundry y su decisión cuando se documente; no asumir que su metadata implica haber pasado el gate;
- mantener en el proyecto las consultas, resultados, fixtures y evidencia específicos del cliente;
- usar únicamente un case sanitizado/sintético para evaluación general cuando la evidencia original no pueda transferirse;
- actualizar el estado de proyecto por su tracker/`STATE`, nunca con estados `candidate` o `stable`.

No registrar el camino absoluto a la carpeta personal del Foundry en documentos compartidos con clientes. Resolver su ubicación en el entorno local del usuario o abrirla de forma explícita cuando se trabaje en Foundry.

## Revisión y autoridad

Separar, cuando sea práctico, `AUTHOR`, `RUNNER` y `REVIEWER`. Priorizar checks deterministas y usar juicio semántico después. Toda promoción —en especial a `stable`— permanece bajo autoridad humana. Crear, rechazar, deprecar y retener evidencia sigue las reglas de autorización definidas por el Foundry.
