# Propuestas para Foundry — detect-leakage 0.1.0

## Decisión recomendada

Mantener experimental supervisada. La evaluación está realizada y documentada localmente, pero no confirma mejora conjunta ni justifica validated/stable. No modificar expected ni buscar un PASS repitiendo los mismos cases. La aceptación formal/revisión independiente pertenece al consultor.

## Artefactos que corresponden

### Skill existente: detect-leakage

- Dar precedencia al output contract del caller. La plantilla base es extensible; respetar campos extra, fecha/hashes y límite de longitud sin inventar metadatos. La condición de evaluación no es obligatoria en todo engagement, pero sí cuando se solicita.
- Solape de entidades no implica contaminación automática: declarar escenario de scoring y objetivo de generalización; investigar identidad, features y disponibilidad. Disjoint groups es una estrategia para casos pertinentes, no una condición universal.
- Historia previa válida requiere ventana y disponibilidad efectiva al scoring. No usar export_at como sustituto de available_at ni certificar seguridad por ausencia de código.
- Priorizar familias aplicables y evidencia esencial; no repetir la skill o presentar riesgo por cada artefacto ausente. Reportes más largos no equivalen a mejor auditoría.
- Mantener reglas esenciales autocontenidas. Referencias a Foundry/AGENTS/candidates son procedencia o recursos opcionales; no depender de rutas inaccesibles en snapshots. Revisar referencias de cliente particular como EQUANS al generalizar.

No se crea un candidate duplicado: son correcciones de la misma capacidad experimental. No se editaron skill ni Foundry canónicos en este estudio. Un borrador futuro de versión debe seguir su proceso y ser evaluado antes de promoción.

### Template/contrato y checker determinista

Separar contrato de reporte del razonamiento de leakage. El checker puede validar frontmatter, campos requeridos por el caller, hashes, fecha, persistencia y extensión. No convertir presencia de frases en PASS semántico ni permitir que el checker acepte gates. Revisar citas/mecanismos manualmente.

### Runner

Retener prompts operativos explícitos, native Skill obligatorio cuando la comparación lo requiere, contexto seleccionado común, diagnósticos redactados y reservas por tier con cota. Los mocks son infraestructura, no eficacia. Registrar costo y native invocation por separado de contenido.

## Hipótesis del próximo estudio

1. Contrato del caller conserva trazabilidad incluso al cargar plantilla de skill.
2. Evita falso positivo en scoring recurrente legítimo; detecta memorización/contaminación cuando corresponde.
3. Feature que agrega solo hechos previos pero llega tarde no es usable al scoring.
4. Preprocessing global, encoding/resampling antes del split y join posterior requieren mecanismos verificables.
5. Mantiene correctitud con preguntas menos guiadas y extensión limitada.

Casos nuevos, expected congelado antes de outputs, orden predefinido, reviewer diferente del autor y repetición suficiente. Sin autorización de gasto fuera del límite del estudio actual. No agrupar con la única repetición de esta evaluación inicial.
