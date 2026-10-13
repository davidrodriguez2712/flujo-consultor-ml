# Ejemplo sintético: activación de tarjetas

> **Ficción para mostrar el flujo.** Aurora, sus procesos, nombres y cifras de este documento son inventados; no describen un cliente ni resultados reales. Los números de ejemplo ilustran cómo anotar cálculos y no deben reutilizarse como benchmark. No son evidencia de un efecto causal.

Este caso demuestra un proyecto pequeño de activación de tarjetas con una ruta inicial de `ANALYSIS`. No requiere una UI nueva, modelo predictivo ni candidate del Foundry para responder la primera pregunta.

## 1. Intake y límites

- **Proyecto:** Aurora — activación de tarjetas (sintético).
- **Problema declarado:** el equipo observa tarjetas que no registran compras durante los primeros días.
- **Decisión:** determinar si hay una brecha descriptiva accionable y qué revisar con operaciones.
- **Owner de negocio:** ficticio, equipo de Operaciones Aurora.
- **Criterio de aceptación:** definición acordada de activación, cohortes comparables, tasa descriptiva reproducible, limitaciones y siguiente decisión sugerida.
- **Fuera de alcance inicial:** atribución causal, recomendación automatizada, comunicación a tarjetahabientes, build de producto.
- **Datos:** solo un extracto sintético, sin datos personales reales.
- **Ruta:** `ANALYSIS`; revisar `EXPERIMENT` únicamente si el owner plantea después una intervención causal evaluable.

La pregunta se acota antes de extraer datos. “No registra compras” no equivale automáticamente a error, falta de intención ni resultado de una campaña.

## 2. Contrato mínimo de tarea

| Campo | Acuerdo sintético |
|---|---|
| Objetivo | Medir la activación descriptiva en una cohorte definida. |
| Unidad | Tarjeta emitida, identificada por una clave ficticia única. |
| Activación | Al menos una compra aprobada dentro de 30 días calendario desde emisión. |
| Cohorte | Tarjetas emitidas en abril del año ficticio, con 30 días completos de observación. |
| Exclusiones | Registros duplicados del extracto; tarjetas sin fecha de emisión válida, reportadas por separado. |
| Inputs | Tablas sintéticas `cards` y `transactions`; definición anterior pendiente de confirmación del owner. |
| Output | Consulta reproducible, tabla con numerador/denominador y nota de limitaciones. |
| Aceptación | Otra persona puede reconstruir el total desde la fuente y la definición confirmada. |
| Parada | Si la fecha de emisión o el estado de transacción no son confiables, detener el cálculo y pedir aclaración. |

## 3. Comprender y validar datos

Antes del cálculo, registrar:

- `cards`: grain esperado = una fila por tarjeta; verificar key única y fecha de emisión.
- `transactions`: grain esperado = una fila por intento; distinguir intentos aprobados/rechazados y reversas.
- Relación: una tarjeta puede tener muchas transacciones; agregar al nivel de tarjeta antes de unir cohortes.
- Tiempo: usar la zona horaria acordada y una ventana de 30 días, con regla explícita para el día de emisión.
- Madurez: excluir del denominador de la tasa principal las tarjetas sin ventana completa; reportar cuántas son.
- Calidad: revisar duplicados, nulls, estados desconocidos, transacciones repetidas y rango temporal.

**Supuesto de demostración:** el extracto ficticio contiene 1,000 tarjetas maduras y 610 tienen al menos una compra aprobada dentro de la ventana. La tasa ilustrativa sería `610 / 1,000 = 61%`. Este valor solo ejercita el formato: no es una medida de negocio.

Guardar la definición, query, versión del extracto y checks con el [contrato de datos](../../templates/data-and-validation.md). Si la unidad/grain o el estado de aprobación no se sostienen, volver al entendimiento de datos; no continuar con una métrica aparentemente precisa.

## 4. Interpretar sin exceder evidencia

Hallazgo sintético:

> En el extracto de demostración, 610 de 1,000 tarjetas con ventana completa cumplen la definición operativa de activación a 30 días (61%). El cálculo es descriptivo. Por sí solo no identifica la causa de no activación ni estima cuántas tarjetas cambiarían con una intervención.

Antes de comparar segmentos, confirmar que las cohortes tienen exposición suficiente, definiciones estables y denominadores pertinentes. Evitar seleccionar cortes solo porque muestran diferencias; registrar el análisis exploratorio y validar una hipótesis antes de recomendar una acción.

## 5. QA y decisión

Revisión mínima del ejemplo:

- [ ] Owner confirma la definición de activación y la ventana.
- [ ] Numerador/denominador se pueden reconstruir desde query y extracto.
- [ ] Fechas/cohortes están maduras y duplicados/rechazos/reversas tratados.
- [ ] El texto mantiene la interpretación descriptiva.
- [ ] Limitaciones y universo excluido aparecen junto a la cifra.

**Salida demostrativa:** entregar la tabla y pedir al owner decidir si una investigación operativa de causas está justificada. No recomendar contacto, oferta o priorización individual con este análisis aislado.

Si la pregunta futura es “¿qué acción aumenta activación?”, formular una hipótesis y explorar diseño experimental o cuasi-experimental apropiado. Si es “¿qué tarjetas tienen mayor propensión?”, evaluar si existe decisión, intervención, datos temporales válidos y valor incremental respecto a una regla simple; el score no prueba impacto causal. Consultar [`experiments-and-models.md`](../../playbooks/experiments-and-models.md).

## 6. ¿Se necesita producto/UI?

En este alcance no: un resumen de análisis para el owner responde la pregunta. No producir dashboard por el solo hecho de que haya datos.

Una extensión hipotética sí podría activar `PRODUCT_UI` si un proyecto define que analistas deben revisar y gestionar una cola de casos, necesita una interacción nueva, existe owner y se acuerdan permisos/datos/acciones. Primero se probarían proceso y wireframe; Figma/handoff y validación visual dependerían de sus gates y herramientas disponibles. Ese supuesto ilustra el caso Boreal en la siguiente cartera, no añade interfaz a Aurora. Ver [`playbooks/product-ui-and-prototyping.md`](../../playbooks/product-ui-and-prototyping.md).

## 7. ¿Se deriva una capacidad al Foundry?

No por defecto. Este análisis aplica procedimientos conocidos y no demuestra una capacidad recurrente que justifique un candidate.

Un candidate solo sería razonable si aparecen tareas repetidas (por ejemplo, estandarizar comprobaciones de madurez y denominadores para múltiples proyectos), con inputs/outputs delimitados, casos de evaluación y evidencia que se pueda compartir sin revelar datos de clientes. Capturar la observación de forma segura y ejecutar el `candidate gate` del Foundry; la decisión de avanzar no pertenece a este proyecto. Ver [`workflow/capability-lifecycle.md`](../../workflow/capability-lifecycle.md).

## 8. Ejemplo de cartera de seis proyectos

Los seis proyectos son engagements independientes. Este árbol muestra organización local solamente; acceso y almacenamiento deben configurarse por separado según el cliente. Copiar solo directorios necesarios.

```text
consulting-portfolio/                   # padre común no es frontera de seguridad
├── aurora-card-activation/              # ANALYSIS descriptivo; este caso
│   ├── PROJECT.md
│   ├── analysis/
│   └── delivery/
├── boreal-retention-prioritization/      # modelo potencial + PRODUCT_UI condicional
│   ├── PROJECT.md
│   ├── model/
│   ├── product-ui/                      # solo si score requiere cola para analista
│   └── delivery/
├── cumbre-campaign-incrementality/       # diseño/estimación de incrementalidad
│   ├── PROJECT.md
│   ├── experiment/
│   └── delivery/
├── delta-data-quality/                  # contratos, profiling y controles
│   ├── PROJECT.md
│   ├── data-contracts/
│   └── delivery/
├── estrella-demand-forecast/             # pronóstico; reporte como salida inicial
│   ├── PROJECT.md
│   ├── model/
│   └── delivery/                         # sin interfaz por defecto
└── faro-market-research/                 # research de mercado/documental
    ├── PROJECT.md
    ├── sources/
    ├── findings/
    └── delivery/
```

| Repo | Pregunta ejemplo | Routing inicial | Artifact de salida posible | ¿PRODUCT_UI? |
|---|---|---|---|---|
| Aurora | ¿Qué proporción cumple definición madura de activación? | `ANALYSIS` | Tabla y brief de hallazgos | No, reporte basta. |
| Boreal | ¿Qué casos requieren atención según reglas/score y cómo los gestiona el analista? | `ANALYSIS` → `MODEL` si aporta → `PRODUCT_UI` si hace falta cola | Validación de score + interacción con estados/override | Sí, condicional a que la cola resuelva tarea real. |
| Cumbre | ¿Qué efecto incremental tuvo la campaña bajo diseño válido? | `EXPERIMENT` | Estimación, incertidumbre y límites | No implícito. |
| Delta | ¿Son confiables las fuentes y métricas críticas? | `ANALYSIS` | Contrato y controles de calidad | No implícito. |
| Estrella | ¿Qué rango de demanda se espera y con qué error? | `MODEL` solo si baseline simple no basta | Forecast y evaluación en reporte | No por defecto. |
| Faro | ¿Qué evidencia externa informa la decisión de mercado? | `RESEARCH` | Síntesis trazable y opciones | No implícito. |

El árbol enseña separación de repositorios de proyecto; no sustituye identidades, permisos, cifrado, políticas de retención ni segregación de infraestructura.
