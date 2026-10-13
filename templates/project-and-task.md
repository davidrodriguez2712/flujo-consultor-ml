# Plantillas de proyecto y tarea

Copiar solo lo que el trabajo requiera. Completar los campos conocidos, marcar lo pendiente y borrar instrucciones entre corchetes antes de compartir. No guardar credenciales en estos documentos.

## Brief de proyecto

Usar en intake cuando haga falta acordar encargo, decisión y límites. Para una tarea pequeña dentro de un proyecto activo, basta el contrato de tarea.

```markdown
# PROJECT — [nombre corto]

## Control
- ID:
- Cliente/equipo:
- Owner de negocio:
- Consultor responsable:
- Fecha / versión:
- Estado operativo:

## Contexto y necesidad
- Situación actual:
- Problema u oportunidad:
- Usuarios/áreas afectadas:
- Por qué ahora:

## Decisión que se debe habilitar
- Decisor:
- Decisión/acción:
- Fecha o cadencia en que se necesita:
- Qué cambiará según el resultado:

## Objetivo y aceptación
- Objetivo:
- Medida de éxito y definición:
- Criterios de aceptación:
- No-objetivos:

## Scope y restricciones
- Incluido:
- Excluido:
- Fecha objetivo / hitos:
- Presupuesto o recursos relevantes:
- Restricciones legales, privacidad, seguridad o política del cliente:
- Nivel de riesgo/revisión:

## Datos, fuentes y entorno
- Fuentes potenciales / owners:
- Datos disponibles confirmados:
- Datos o accesos pendientes:
- Entorno/repositorio autorizado:
- Retención/eliminación aplicable:

## Ruta inicial
- Rutas candidatas: [RESEARCH / ANALYSIS / EXPERIMENT / MODEL / BUILD / PRODUCT_UI / DELIVERY]
- Hipótesis o preguntas abiertas:
- Próximo gate y responsable:

## Artefactos y enlaces
- [enlace o ruta] — [qué controla]
```

## Contrato de tarea

Usar cuando se asigna una unidad de trabajo a una persona o agente, especialmente si hay ejecución, cambios o revisión delegada.

Un borrador de tarea puede prepararse dentro de un mandato de revisión/propuesta, declarando las dependencias pendientes para ejecutarlo. La evolución de un plan vivo no invalida un paquete histórico íntegro ni exige congelar cada propuesta. Separar impedimentos de trazabilidad, decisiones de alcance pendientes y autorización de ejecución.

Si el encargo pide un borrador, devolver una tarea redactada y revisable con los campos pertinentes, no instrucciones para redactarla después. Los outputs y criterios todavía no acordados se identifican como propuestas; lo desconocido se marca pendiente sin inventar valores. Respetar el formato de salida: un contrato JSON incorpora el borrador en los campos permitidos, sin anexar Markdown fuera del objeto.

Al completar el borrador, incluir al menos un output futuro con contenido específico y criterios verificables, distintos de una métrica/umbral de rendimiento pendiente. El borrador no cuenta como output del trabajo futuro. Asociar cada dependencia con la acción que limita. El estado de respuesta se refiere al encargo actual según su contrato, no a la disponibilidad para ejecutar después. En Markdown conservar encabezados/orden/ubicación del estado exigidos; en JSON conservar campos/tipos sin texto externo.

```markdown
# TASK — [ID: título]

- Proyecto:
- Owner / ejecutor / reviewer:
- Estado:
- Fecha límite o ventana:
- Acción de esta tarea: propuesta / revisión / ejecución / aceptación humana
- Dependencias que impiden ejecutar, si existen (dato/decisión → acción afectada):

## Objetivo y decisión
- Resultado que se necesita:
- Decisión que informa:

## Inputs y fuentes canónicas
- Artefactos/rutas/versiones:
- Datos y fecha de extracción:
- Incertidumbres conocidas:

## Alcance
- Incluye:
- Excluye:
- Write scope permitido:
- Herramientas/accesos autorizados:

## Outputs propuestos
- Artefacto(s) futuros que producirá esta tarea y formato (sin contar este borrador):
- Contenido mínimo esperado:
- Relación con la decisión que se necesita:
- Estado del acuerdo: propuesto / acordado con evidencia

## Restricciones y riesgos
- Privacidad/seguridad:
- Método/supuestos que no deben cambiarse sin aprobación:
- Condición de parada/escalamiento:

## Aceptación
- Estado de estos criterios: propuestos / acordados con evidencia
- [ ] Criterio observable 1:
- [ ] Criterio observable 2:
- Métrica/umbral de rendimiento todavía pendiente, si aplica:
- Evidencia que se adjuntará:

## Contrato de salida
- Consumidor: persona / proceso / ambos
- Formato acordado:
- Campos/tipos obligatorios o referencia al esquema, si corresponde:
- Texto adicional permitido fuera del artifact: sí / no
- Check de formato y resultado:
- Revisión de contenido y resultado:

## Handoff
- Artefacto final/ruta:
- Limitaciones y trabajo no realizado:
- Siguiente owner/acción:
```

Si el formato es JSON puro y no permite texto adicional, la salida es un único objeto sin fences ni prefacio. Los ejemplos Markdown de este template no cambian ese contrato. Conservar cualquier output inválido y registrar una corrección como versión nueva autorizada; no reparar silenciosamente el original ni repetir llamadas de pago sin autorización. Completar solo los campos pertinentes; este contrato no añade campos al schema de profile o state de ACOS.

## Mapa de proyecto para seis engagements

Ejemplo organizativo; crear cada repo bajo el control de acceso correspondiente. El directorio padre agrupa localmente, pero no aísla datos ni constituye una barrera de seguridad. La estructura real se adapta a políticas, volumen, stack y artifacts necesarios.

```text
consulting-portfolio/                 # Agrupación local únicamente
├── aurora-card-activation/            # Repo/espacio aislado de Aurora
│   ├── PROJECT.md
│   ├── decisions/
│   ├── data/
│   ├── analysis/
│   └── delivery/
├── boreal-retention-prioritization/    # Repo/espacio aislado de Boreal
│   ├── PROJECT.md
│   ├── decisions/
│   ├── data/
│   ├── model/
│   ├── product-ui/                    # Solo por cola de trabajo para analistas
│   └── delivery/
├── cumbre-campaign-incrementality/     # Repo/espacio aislado de Cumbre
│   ├── PROJECT.md
│   ├── experiment/
│   └── delivery/
├── delta-data-quality/                 # Repo/espacio aislado de Delta
│   ├── PROJECT.md
│   ├── data-contracts/
│   ├── analysis/
│   └── delivery/
├── estrella-demand-forecast/           # Repo/espacio aislado de Estrella
│   ├── PROJECT.md
│   ├── data/
│   ├── model/
│   └── delivery/                       # Reporte; no UI por defecto
└── faro-market-research/               # Repo/espacio aislado de Faro
    ├── PROJECT.md
    ├── sources/
    ├── findings/
    └── delivery/
```

No crear todos los directorios vacíos en cada repo. Mantener datos, instrucciones y credenciales separados según los controles del cliente.
