# Contrato de registro de ejecución

Versión documental: `0.1.0`. Estado: propuesto, local, no ejecutado. [Alcance compartido](README.md).

## Propósito

Conservar información suficiente para auditar una comparación y distinguir consistencia de archivos de precedencia temporal. Los hashes actuales no prueban por sí solos que expected se fijó antes de ejecutar.

## Antes de ejecutar

El preregistro debe identificar hipótesis, versiones de los contratos, cases y tratamientos, condiciones, repeticiones, orden, modelo/configuración, checks y política de fallos de infraestructura. Fijar criterios de fallo y regla de decisión; no seleccionar repeticiones o scores después de ver resultados.

Conservar case, inputs, expected, pautas, payloads y checker con versiones y hashes. Expected y soluciones del reviewer quedan fuera del payload y del acceso del agente evaluado. Si inputs explicitan el resultado conceptual del caso, registrar que se mide ejecución guiada; no atribuir al suplemento todo el acierto.

Registrar `frozen_at` y aprobación del protocolo antes de `started_at`. Para acreditar precedencia de forma independiente, conservar un anclaje previo verificable, por ejemplo un registro revisado y firmado externamente o un commit publicado con fecha verificable. No crear Git ni publicar nada automáticamente. Si solo hay timestamps locales, declarar `precedence_evidence: local_only`; la precedencia está registrada, no acreditada externamente.

## Registro por invocación

| Grupo | Datos requeridos |
|---|---|
| Identidad | `run_id`, case/versión, rama, repetición, author, runner, reviewer |
| Entorno | OS/arquitectura, versión CLI/runtime, ejecutable y directorio de trabajo |
| Petición | argv exacto como lista, payload exacto, hashes, system prompt y contexto adicional |
| Configuración | Modelo solicitado, parámetros solicitados y configuración efectiva comprobable |
| Tiempo | Inicio/fin en UTC, duración de pared y duración del proveedor en campos separados |
| Respuesta | stdout/raw, texto del resultado, stderr, exit code, session ID e indicador de error |
| Uso | Modelo resuelto, tokens, coste reportado y fuente de esas magnitudes, o `null` si no existen |
| Evaluación | Checker/versión/hash, comando, resultados, juicio semántico y revisión separada |

Distinguir configuración solicitada de efectiva. Si el runtime no expone un parámetro, registrar `effective: unknown` y la limitación; un argv demuestra lo solicitado, no que el proveedor lo aplicó. No atribuir efecto al suplemento si también cambian modelo, permisos, herramientas o inputs sin análisis explícito.

Los campos no disponibles permanecen `null` con motivo. Un plan de ejecución no contiene resultados ni timestamps ficticios presentados como reales. Registrar datos necesarios sin persistir credenciales; una redacción que impida auditar el payload debe constar como límite.

## Forma documental de una ronda futura

```text
<ronda-nueva>/
├── protocol.md
├── frozen-inputs.json
├── provenance.json
├── cases/<case-id>/
│   ├── case.md
│   ├── inputs.json
│   └── expected.json           # acceso solo de runner/reviewer
├── runner/                    # código y comando reproducibles
├── checker/                   # código, dependencias y versión
├── runs/<case-id>/<rama>/<repetición>/
│   ├── request.json
│   ├── payload.txt
│   ├── stdout.txt
│   ├── raw.json
│   ├── result.txt
│   ├── stderr.txt
│   ├── metadata.json
│   └── checks.json
├── review.md
└── evidence-manifest.json
```

Este árbol es una propuesta documental, no una carpeta ya generada. La separación física no basta para proteger expected: el runner debe controlar lo enviado y los archivos/herramientas accesibles. Adaptar la estructura al runtime conservando la información, sin duplicarla innecesariamente.

## Checks y formato

Para una tarea que pide JSON puro, validar el texto del resultado del modelo, no confundirlo con el envelope JSON del CLI. `strict_format_pass` requiere un único JSON válido, sin fences ni texto adicional, claves duplicadas o números no finitos. La validación de schema/campos y la correctitud de contenido se reportan por separado.

Si se extrae JSON de fences para diagnosticar contenido, registrar `diagnostic_parse_used: true` y conservar `strict_format_pass: false`. Los aciertos diagnósticos no convierten un incumplimiento de formato en conformidad. El protocolo decide antes cómo afecta cada check al resultado de la tarea; no inventar un score compuesto retrospectivo.

Cada comparación conserva todos los intentos. Un error de red no equivale a una respuesta válida incorrecta; un output malo no se etiqueta como infraestructura para reintentarlo. Aplicar la política de reintentos fijada, archivar intentos y distinguir exclusión técnica de selección favorable.

## Criterios de aceptación para otra ronda

- El checker recalcula conteos, métricas y formato desde outputs conservados, sin editar originales.
- Verificar que las ramas solo difieren en el tratamiento declarado y que expected no llega al agente.
- Hashes y correspondencia raw/texto/metadata comprobables; sesiones y contextos registrados según el harness.
- Registrar precedencia y su grado de acreditación; no confundir integridad actual con preregistro verificable.
- No sustituir tiempos de pared por tiempos del proveedor ni costes ausentes por cero.
- Separar author, runner y reviewer cuando sea posible; declarar coincidencias de actor. Revisión por agente no es revisión humana externa.
- Presentar aciertos, fallos y límites por criterio y repetición; ninguna comparación promueve automáticamente una capacidad.

Los checks anteriores deberán implementarse y comprobarse en una ronda aprobada. No son funcionalidades actuales de `acos validate`.
