# ACOS Project Compiler — Plan de implementación

> **Para agentes ejecutores:** SUB-SKILL REQUERIDA: usar `superpowers:executing-plans` para ejecución nativa o `superpowers:subagent-driven-development` si el usuario elige delegación. Ejecutar tarea por tarea; los pasos usan checkboxes para registrar avance.

**Estado:** aprobado e implementado localmente; verificación macOS/Python 3.13.2 y Linux en Docker/Python 3.11. Integración básica real de ambos harnesses verificada en macOS; Windows y piloto con escritura pendientes. Véanse los informes en `docs/acos/validation/`.  
**Goal:** entregar una CLI instalable que compile un workspace portable de consultoría a partir de un perfil confirmado, con selección contextual de artefactos y guía diaria.

**Architecture:** aplicación Python con contratos versionados, catálogo declarativo empaquetado y reglas locales. El inventario Foundry se inspecciona en tiempo de inicialización y el resolver produce un plan explícito antes de escribir. El compiler conserva snapshots y procedencia relativa; los comandos de seguimiento leen el proyecto sin avanzar etapas.

**Tech Stack:** Python >=3.11, `argparse`, `pathlib`, `hashlib`, `importlib.resources`, `subprocess` de la biblioteca estándar; Pydantic >=2,<3, PyYAML >=6,<7 y platformdirs >=4,<5. Packaging con setuptools >=68 y wheel; pytest solo como dependencia de desarrollo para la verificación futura del software.

**Spec:** [diseño aprobado del compiler](../specs/2026-10-04-acos-project-compiler-design.md), integrado con [Agentic Consulting OS modular](../specs/2026-10-04-agentic-consulting-os-design.md). Leer también la [revisión actual de Foundry](../analysis/2026-10-06-acos-foundry-integration.md).

## Global Constraints

- «La necesidad determina el artefacto.» No producir una skill por cada concepto ni activar ML/UI por defecto.
- «macOS, Linux y Windows son objetivos V1»; Codex y Claude Code son runtimes objetivo.
- «Por defecto crea subcarpeta nueva dentro de la ubicación actual.» `--here` debe ser explícito.
- «No se crean carpetas vacías solo por estar en un catálogo.»
- «La persona confirma la composición final.» Una respuesta EOF/cancelación nunca equivale a confirmar.
- «El perfil, y no el texto conversacional ni el LLM, es la entrada reproducible al Module Resolver y Project Compiler.»
- «Usar una skill experimental no la promueve, valida ni modifica.»
- «AGENTS.md es la fuente compartida de instrucciones del proyecto.» Skills nativas en `.agents/skills/` y `.claude/skills/` según selección.
- «No hay promoción ni sincronización automática.» No escribir Foundry desde esta CLI ni exportar feedback automáticamente.
- «acos validate nunca mueve automáticamente el proyecto a la etapa siguiente.» `status`/`next` tampoco escriben estado.
- Español para documentación y flujo; términos, IDs y campos técnicos en inglés.
- No seleccionar archivos de `experiments/scratch/`, `evals/`, candidates o snapshots como skills operativas. Actualmente nueve skills `experimental 0.1.0`; 18 fichas como conocimiento y seis diferidas. No codificar ese conteo como requisito de ejecución.
- Sin iniciar Git, configurar remotos, publicar en PyPI ni crear infraestructura cloud durante implementación. Si posteriormente existe un repo autorizado, commits por tarea; en el workspace actual registrar avance en este plan sin comandos Git.
- Este documento propone pruebas futuras del producto; en esta fase solo se escriben/revisan documentos. Las pruebas se añaden/ejecutan al autorizar implementación y su verificación.

Las elecciones de dependencias permiten contratos con [modelos Pydantic](https://docs.pydantic.dev/latest/concepts/models/), YAML cargado con `safe_load` según [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) y configuración por usuario mediante [platformdirs](https://platformdirs.readthedocs.io/en/latest/). Usarlas para estructura y rutas no certifica calidad de negocio.

## Review Focus

1. Contexto insuficiente o ambiguo: conservar `null`/preguntas abiertas y pedir confirmación; no deducir labels, métricas ni software. Tareas 1/2/7.
2. Foundry con metadata inválida, recursos fuera de la raíz o archivos archivados: excluir/documentar y continuar con cobertura parcial. Tareas 3/4/5.
3. `--here`, nombres Windows y cancelación/error en mitad de escritura: preservar contenido previo y no dejar proyecto aparentemente completo. Tareas 1/5/7.
4. Estado desactualizado, saltos de etapa o human review sin evidencia: informar bloqueo/revisión sin avanzar ni presentar archivos existentes como gate aprobado. Tarea 6.
5. Ambos runtimes, recursos de skill y proyecto movido a otra laptop sin Foundry: snapshots iguales, sin rutas personales, manual/comandos locales utilizables. Tareas 5/8.

## Decisiones técnicas que concreta este plan

### Contratos y fuentes de verdad

Todos los YAML usan `schema_version: 1`, UTF-8, carga segura y rechazo de keys duplicadas. Los modelos rechazan campos desconocidos; no hacer coerción silenciosa de bool/number a texto. Fechas, cuando existan, se almacenan como texto ISO-8601 explícito. IDs de arquetipo son los ocho del spec; runtimes: `codex`, `claude_code`. Stage IDs: `discovery`, `framing`, `diagnosis`, `execution`, `validation`, `delivery`, `handoff`.

| Modelo/archivo | Campos requeridos y ownership |
|---|---|
| `ProjectProfile` / `.acos/project-profile.yaml` | `schema_version`, `project` (slug, name, client nullable, industry/market/role nullable), `engagement` (decision/problem/success_metric/decision_owner/users nullable, archetypes[], delivery_modes[], current_stage, open_questions[]), `data` (sources[], characteristics{}), `constraints[]`, `deliverables[]`, `runtimes[]`. Confirmado antes de compilar; el texto libre no autoriza side effects. |
| `ModuleSelection` / `.acos/modules.yaml` | `schema_version`, `catalog_version`, `profile_sha256`, `modules[]`, `capabilities[]`, `gates[]`, `excluded[]`, `gaps[]`, `reasons[]`. Snapshot de composición confirmada, no backlog Foundry. |
| `ProjectState` / `.acos/state.yaml` | `schema_version`, `current_stage`, `status` (`NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`), `objective`, `completed_stages[]`, `blockers[]`, `open_decisions[]`, `gate_reviews{gate_id: {decision, reviewer, evidence[], profile_sha256}}`. Editable por humano/agente bajo autoridad del proyecto; fuente canónica de etapa y revisión. |
| `Manifest` / `.acos/manifest.yaml` | `schema_version`, `acos_version`, `catalog_version`, `profile_sha256`, `modules_sha256`, `source_os_version`, `artifacts[]` (path, ownership, initial_sha256), `skills[]` (name, status, version, source_ref, tree_sha256, files[{relative_path,sha256}], runtime_paths[]), `initialization: complete`. Se escribe al final. Sin rutas absolutas al Foundry. |
| `UserConfig` / fuera del proyecto | `schema_version`, `foundry_path` nullable y `llm_adapter_argv[]` opcional. Ruta de `platformdirs.user_config_path('acos') / 'config.yaml'`. No guardar secretos ni contexto del cliente. |

`STATE.md` y la sección «Situación al inicializar» de `MANUAL.md` son vistas generadas al inicio, no la autoridad dinámica. `acos status`/`acos next` calculan la situación vigente desde state/profile/selection; instrucciones compartidas obligan al agente a leer esos archivos y actualizar la vista Markdown al cerrar una sesión autorizada. Ningún comando read-only regenera archivos. `TASKS.md` es el backlog humano NOW/NEXT/LATER/BLOCKED; no se duplica en YAML. `DECISIONS.md` conserva rationale y el log de aprobaciones.

El cambio de etapa se registra manualmente en state y decisions tras aprobar el gate; no hay comando de avance V1. Si una proyección Markdown contradice state, se declara obsoleta y se usa state. Un cambio posterior del perfil o composición que invalide los hashes exige revisar/recompilar en un workspace nuevo; no ofrecer actualización automática ni reinterpretar snapshots en silencio.

### Catálogo inicial y composición

Catálogo empaquetado `catalog_version: 0.1.0`; contenido derivado del OS 2.0 existente. Declarar cada módulo con ID/version, triggers, dependencias explícitas, capability IDs, artifacts, template IDs y gate IDs. Reglas permitidas: `equals`, `contains`, `is_true`, `any`, `all` sobre campos declarados; nada de `eval`, expresiones Python o scripts del catálogo.

- `consulting_core`: siempre; contexto, framing, evidencia, decisión/delivery/handoff básicos. No obliga a ejecutar etapas previas si se inicia en validación.
- `data_analysis`: fuentes tabulares o trabajo de datos confirmado; contratos/diccionario, análisis y calidad.
- `research`: research confirmado o comparación de alternativas con fuentes; no inferir disponibilidad de datos.
- `supervised_model`: solo con intención predictiva confirmada y tarea/target definidos o pendientes visibles. Labels ausentes impiden gate de entrenamiento, no se fabrican.
- `forecast`, `selection`, `optimization`, `intervention`, `segmentation`, `recommendation`: módulos separados activados por arquetipos explícitos. Reusar artifacts de evidencia/decisión del core.
- `genai_solution`, `software_ui`, `operationalization`: solo por forma de entrega y necesidad explícita. `software_ui` admite API/software sin UI; exige interacción nueva/modificada para activar skills UI. Figma/stack/herramientas siguen siendo preconditions independientes.
- `business_case`, `executive_delivery`: por entregables confirmados; deck/memo son pautas/templates, no archivos PPTX inventados.

Usar carpetas semánticas relativas (`context/`, `framing/`, `evidence/`, `analysis/`, `modeling/`, `validation/`, `decision/`, `delivery/`, `handoff/`, `solution/`) sin numeración obligatoria; generar solo artifacts seleccionados y directorios padres. No crear modelos, datasets, notebooks ni tests de cliente vacíos. Un artifact compartido se genera una vez; rutas duplicadas con contenidos distintos son conflicto del catálogo.

El catálogo usa requerimientos semánticos y listas de skills compatibles, no match por keywords del nombre. Cada propuesta debe explicar su regla, preconditions verificadas/desconocidas, límites y fallback. H07/H09/H12 se expresan como pautas de revisión de outputs en los playbooks del OS; no como skills operativas. H06/H19/H20 no seleccionan versiones archivadas. No copiar el registro de 24 candidates a proyectos de cliente.

### Conflictos, snapshots y CLI

- `acos init [nombre] [--here] [--profile-file PATH] [--llm]`: perfil de archivo es entrada canónica alternativa al wizard; no es un preset. `--here` no permite nombre posicional. No incluir flags que omitan confirmación.
- Nombre de carpeta: slug conservador ASCII, minúsculas/dígitos/guiones, max 64 caracteres; bloquear `.`/`..`, separadores, rutas absolutas y nombres reservados Windows. Nombre visible puede conservar Unicode. Ante slug inválido proponer uno y exigir aceptación.
- Carpeta nueva: rechazar cualquier destino existente, incluso vacío; componer en staging vecino y renombrar al final sin reemplazar destino.
- `--here`: preservar archivos ajenos, bloquear colisiones de archivos generados/`.acos/manifest.yaml`; no ofrecer overwrite V1. Escritura exclusiva de archivos tras revisar el plan; manifest al final. En fallo retirar solo archivos/directorios creados por esta ejecución que no hayan cambiado, nunca contenido ajeno. Si la reversión es incompleta, informar rutas y no declarar proyecto listo.
- Bloquear rutas absolutas/`..`, symlinks y escapes de raíz en artifacts y bundles. Reservar `.acos/init.lock` con creación exclusiva durante escritura; no borrar lock ajeno ni reanudar una operación desconocida.
- Copiar bytes de todo el bundle seleccionado, incluidos recursos, sin ejecutar scripts ni reescribir `SKILL.md`. Hash de árbol: SHA-256 de JSON canónico de pares ordenados `(relative_posix_path, file_sha256)`. Comprobar bytes antes/después de copia y detectar cambios del Foundry entre preview y commit. Releer inventario/decisión de cada skill seleccionada antes de escribir; un cambio de metadata, decisión o bundle exige nuevo preview y confirmación. El Foundry root vive solo en memoria del plan, no se incluye en los YAML del proyecto.
- Para Claude generar `CLAUDE.md` mínimo que remite a `AGENTS.md`; para ambos, dos rutas nativas con mismos bytes/hashes. No depender de symlinks ni asumir que instalación equivale a eficacia.
- Codes CLI: `0` lectura/compilación exitosa o gate `PASS`; `2` input/perfil inválido; `3` gate `NEEDS_REVIEW`; `4` gate/conflicto `BLOCKED`; `130` cancelación. Errores de I/O muestran acción/ruta pertinente sin traceback normal.
- `--llm` utiliza solo un adapter explícito configurado por el usuario: executable argv, `shell=False`, JSON por stdin/stdout y timeout 30 s. Mostrar payload exacto, destino ejecutable y advertencia de que el adapter puede transmitirlo; consentimiento para esa invocación, no reutilizable. Sin adapter, rechazo, timeout o salida inválida: continuar clasificación local con limitación visible. No instalar un proveedor ni transmitir archivos de datos.

## Estructura de archivos prevista

| Archivos | Responsabilidad |
|---|---|
| `pyproject.toml`, `src/acos/__init__.py`, `src/acos/__main__.py` | Paquete `agentic-consulting-os`, versión inicial `0.1.0`, entry point `acos = acos.cli:main`; build/ejecución. |
| `src/acos/contracts.py`, `src/acos/yaml_io.py`, `src/acos/config.py` | Modelos compartidos, lectura YAML y preferencias locales. |
| `src/acos/catalog.py`, `src/acos/classifier.py`, `src/acos/resources/catalog.yaml` | Catálogo versionado y reglas explicables. |
| `src/acos/resources/os/`, `src/acos/resources/templates/` | Subconjunto empaquetado del OS y templates instanciables; sin rutas hacia checkout original. |
| `src/acos/foundry.py`, `src/acos/resolver.py` | Inventario operativo, decisiones/dependencias y composición propuesta. |
| `src/acos/render.py`, `src/acos/compiler.py` | Render Markdown/YAML, snapshots y escritura transaccional. |
| `src/acos/project.py`, `src/acos/gates.py` | Lectura, próximos pasos y checks del workspace. |
| `src/acos/intake.py`, `src/acos/llm_adapter.py`, `src/acos/cli.py` | Wizard adaptativo, adapter opt-in y comandos públicos. |
| `tests/` y `tests/fixtures/` | Casos de software del compiler; no evaluaciones de skills Foundry. |
| `docs/acos/installation.md`, `docs/acos/project-usage.md`, `docs/acos/release.md` | Instalación, operación, mantenimiento y release manual. |
| `AGENTIC_CONSULTING_OS.md` | Añadir enlace a uso del compiler cuando exista; no reemplazar método por instrucciones técnicas. |

## Tarea 1: Contratos, configuración y paquete ejecutable

**Archivos:** crear `pyproject.toml`, `src/acos/{__init__,__main__,contracts,yaml_io,config}.py`, `tests/test_contracts.py`, `tests/test_config.py`; entry point definitivo se conecta en tarea 7.

**Interfaces:**
- Producir los cinco modelos de la tabla, `ArtifactSpec(path: str, template_id: str, ownership: str)`, `Finding(code: str, message: str, paths: list[str])`, `AcosError(code: int, message: str)`.
- `read_yaml(path: Path) -> dict`, `write_yaml_bytes(model: BaseModel) -> bytes`, `canonical_sha256(model: BaseModel) -> str` (JSON ordenado, UTF-8; excludes ningún campo del modelo).
- `load_config(config_path: Path | None = None) -> UserConfig`, `save_config(config: UserConfig, config_path: Path | None = None) -> None`, `validate_slug(value: str) -> str`.

- [x] Definir `test_profile_schema_roundtrip`, `test_duplicate_yaml_key_rejected`, `test_unknown_schema_rejected`, `test_unknown_fields_rejected`, `test_missing_business_fields_remain_null`, `test_unsafe_slug_windows_reserved` (incluye CON/NUL/con.txt), `test_config_path_separate_from_project` y `test_config_invalid_does_not_get_overwritten`; afirmar roundtrip, rechazo y conservación del archivo anterior.
- [x] Ejecutar `python -m pytest tests/test_contracts.py tests/test_config.py -q`; comprobar fallo por contratos/módulos ausentes.
- [x] Implementar modelos y funciones con las invariantes de la tabla. Config write atómico en su propia carpeta, solo tras confirmar Foundry/adapter; no capturar contexto del cliente.
- [x] Configurar packaging `src/`, dependencias y package-data para YAML/Markdown/recursos; exportar `__version__ = '0.1.0'` y `python -m acos` delegando al entry point de tarea 7.
- [x] Repetir el comando de verificación; entregar contratos y preferencias que puedan revisarse independientemente.

## Tarea 2: Catálogo y clasificación local explicable

**Archivos:** crear `src/acos/{catalog,classifier}.py`, `src/acos/resources/catalog.yaml`, `src/acos/resources/os/`, `src/acos/resources/templates/`, `tests/test_catalog.py`, `tests/test_classifier.py`.

**Interfaces:**
- `Catalog(version: str, modules: list[ModuleSpec], templates: dict[str,str], capability_policies: dict)`; `ModuleSpec` contiene los campos de catálogo definidos arriba; `load_catalog() -> Catalog` desde package resources.
- `Classification(archetypes: list[str], proposals: list[dict], unresolved: list[str])` y `classify(profile: ProjectProfile, catalog: Catalog) -> Classification`. Cada proposal contiene `archetype`, `rule_id`, `signal`, `certainty` (`explicit`, `suggested`); no porcentajes inventados.
- `evaluate_rule(rule: dict, profile: ProjectProfile) -> bool` solo para operadores permitidos.

- [x] Definir `test_rules_use_explicit_signals`, `test_ambiguous_brief_remains_unresolved`, `test_no_ui_or_ml_from_report_delivery`, `test_missing_label_never_inferred`, `test_catalog_reference_integrity`, `test_overlapping_modules_deduplicate_artifacts`, `test_invalid_catalog_operator_rejected`; assertions de arquetipos, causas y ausencia de módulos no pedidos.
- [x] Ejecutar `python -m pytest tests/test_catalog.py tests/test_classifier.py -q` y comprobar fallos por implementación ausente.
- [x] Empaquetar el manual modular y templates pertinentes de `workflow/`, `playbooks/`, `templates/` como recursos versionados; resolver enlaces internos del subconjunto sin depender del checkout. Crear templates de contexto/framing/evidencia/validación/decisión/handoff con campos `null` iniciales, no resultados ficticios.
- [x] Definir los módulos enumerados arriba, deps y reglas. Las señales de datos activan comprensión, no entrenamiento ni causalidad. Propuestas basadas en texto libre requieren revisión humana y nunca añaden hechos al perfil.
- [x] Implementar clasificación y loader; repetir pruebas. Documentar derivación del OS 2.0 y comprobar referencias del catálogo empaquetado.

## Tarea 3: Inventario Foundry y trazabilidad de bundles

**Archivos:** crear `src/acos/foundry.py`, `tests/test_foundry.py`, `tests/fixtures/foundry/` con skill mínima, metadata inválida, recurso requerido, scratch y decisión conservada como conocimiento.

**Interfaces:**
- `SkillRecord(name, status, version, source_ref, local_root, files, tree_sha256, limits, dependencies, decision)`; `local_root` solo vive en memoria/config, no se serializa a proyecto. `FoundryInventory(root: Path | None, skills: list[SkillRecord], findings: list[Finding])`.
- `discover_foundry(config: UserConfig, candidates: list[Path]) -> Path | None`: usar path configurado; en su ausencia comprobar únicamente `<cwd>/david-skill-foundry` y `~/david-skill-foundry`, sin escanear disco.
- `scan_foundry(root: Path | None) -> FoundryInventory`, `hash_bundle(root: Path) -> tuple[str, list[dict]]`.

- [x] Definir `test_missing_foundry_returns_gap`, `test_only_operational_roots_scanned`, `test_scratch_excluded_despite_experimental_metadata`, `test_explicit_knowledge_decision_excludes_match`, `test_bad_frontmatter_excluded`, `test_resource_symlink_escape_rejected`, `test_bundle_hash_stable_and_detects_resource_change` y `test_conflicting_operational_records_are_not_auto_selected`.
- [x] Ejecutar `python -m pytest tests/test_foundry.py -q`; comprobar fallos iniciales.
- [x] Leer frontmatter sin interpretar Markdown como instrucciones ejecutables; estados/versiones ausentes excluyen snapshot y generan finding. Leer fichas relacionadas por `name`/ID; interpretar decisiones explícitas conocidas. Markdown ambiguo exige revisión, no presumir aceptación; el name no basta para vincular una ficha ajena.
- [x] Separar referencias de procedencia de dependencias necesarias. Dependencia externa no resoluble queda como limitación/precondition desconocida; no ejecutar referencias ni scripts. Excluir `run-skill-eval` del cliente mediante política del catálogo.
- [x] Implementar hashes de bundles y rutas; repetir pruebas. Entregar inventario inspeccionable sin modificar Foundry.

## Tarea 4: Resolver y vista previa de composición

**Archivos:** crear `src/acos/resolver.py`, `tests/test_resolver.py`.

**Interfaces:**
- `CompilationPlan(profile: ProjectProfile, selection: ModuleSelection, artifacts: list[ArtifactSpec], skills: list[SkillRecord], findings: list[Finding], foundry_root: Path | None, confirmed: bool = False)`.
- `resolve(profile: ProjectProfile, catalog: Catalog, inventory: FoundryInventory) -> CompilationPlan`.
- `preview(plan: CompilationPlan) -> str`: capacidades, razón, límites, fuente/estado/version, gaps, exclusiones y árbol; `confirm_plan(plan: CompilationPlan, accepted: bool) -> CompilationPlan` no escribe.

- [x] Definir `test_fraud_composes_data_selection_optimization_without_genai`, `test_research_omits_modeling`, `test_unlabeled_anomaly_not_supervised_by_default`, `test_ui_preconditions_not_assumed`, `test_experimental_requires_visible_confirmation`, `test_deferred_or_knowledge_not_operational`, `test_missing_foundry_preserves_os_fallback`, `test_init_at_validation_keeps_prior_requirements_visible`.
- [x] Ejecutar `python -m pytest tests/test_resolver.py -q`; comprobar fallos iniciales.
- [x] Componer deps/artifacts de módulos confirmados de forma determinista. Match semántico por requerimientos y política del catálogo, verificando preconditions del perfil y límites de cada SkillRecord. Tools/stack desconocidos no se certifican compatibles.
- [x] Para capacidad sin skill, proponer playbook/template/gate si cubre el trabajo y marcar cobertura parcial; si no existe fallback suficiente, registrar gap y gate de resolución. No crear candidates ni bloquear toda inicialización por un gap de trabajo futuro.
- [x] Implementar preview y confirmación; repetir pruebas. El destino de cada snapshot depende del runtime; ambas copias usan un solo SkillRecord confirmado.

## Tarea 5: Compiler portable, snapshots y manual personalizado

**Archivos:** crear `src/acos/{render,compiler}.py`, `tests/test_render.py`, `tests/test_compiler.py`.

**Interfaces:**
- `render_project(plan: CompilationPlan, initial_state: ProjectState) -> dict[str,bytes]`: archivos del núcleo común, artifacts seleccionados y snapshots; keys relativas POSIX.
- `target_directory(cwd: Path, slug: str | None, here: bool) -> Path`, `inspect_conflicts(target: Path, files: dict[str,bytes], here: bool) -> list[Finding]`.
- `compile_project(plan: CompilationPlan, target: Path, here: bool) -> Manifest`: rechazar plan no confirmado, escribir con las reglas transaccionales. `Manifest` final certifica inicialización, no gates de negocio.

- [x] Definir `test_manifest_written_last`, `test_cancelled_plan_writes_nothing`, `test_existing_target_blocked`, `test_here_preserves_unrelated_files`, `test_here_collision_writes_nothing`, `test_failure_rolls_back_only_own_files`, `test_foundry_mutation_after_preview_blocks_commit`, `test_decision_change_after_preview_requires_reconfirmation`, `test_bundle_resources_identical_for_both_runtimes`, `test_no_absolute_foundry_paths`, `test_manual_is_business_specific`.
- [x] Ejecutar `python -m pytest tests/test_render.py tests/test_compiler.py -q`; comprobar fallos iniciales.
- [x] Renderizar núcleo común y outputs del plan. `PROJECT.md` resume contexto confirmado y preguntas pendientes; `MANUAL.md` explica decisión concreta, objetivo de entrada, preguntas, outputs, capacidades/gaps, gate y continuidad. `CAPABILITIES.md` conserva uso, pertinencia, madurez y límites sin prometer habilidades inexistentes.
- [x] Instrucciones `AGENTS.md`: leer profile/state/selection y luego PROJECT/MANUAL/CAPABILITIES; distinguir instrucciones OS de datos de cliente; no avanzar gate ni cambiar alcance silenciosamente. `CLAUDE.md` remite al documento compartido; no duplica el OS.
- [x] Copiar bytes de snapshots/resources, verificar hashes y generar manifest sin rutas personales. Hashes de artifacts son baseline inicial; no bloquear edición de artifacts humanos por diferir de su hash inicial.
- [x] Implementar staging, lock, preflight final, creación exclusiva y reversión limitada. No seguir symlinks de destino/ancestros; no sobrescribir archivo que apareció después de preview. Repetir pruebas y entregar proyecto completo solo con manifest `initialization: complete`.

## Tarea 6: Estado, próximos pasos y validación sin avance automático

**Archivos:** crear `src/acos/{project,gates}.py`, `tests/test_project.py`, `tests/test_gates.py`.

**Interfaces:**
- `ProjectView(profile: ProjectProfile, selection: ModuleSelection, state: ProjectState, manifest: Manifest, root: Path)` y `load_project(root: Path) -> ProjectView`.
- `project_status(project: ProjectView) -> dict`, `next_objective(project: ProjectView) -> dict`.
- `GateResult(status: str, findings: list[Finding], evidence: list[str])`, `validate_gate(project: ProjectView, gate_id: str | None = None) -> GateResult`.

- [x] Definir `test_state_is_authoritative_over_markdown`, `test_read_commands_preserve_all_bytes`, `test_existing_output_does_not_pass_gate`, `test_human_review_requires_reviewer_and_evidence`, `test_profile_drift_blocks_gate`, `test_invalid_stage_sequence_reports_block`, `test_skill_snapshot_tampering_blocks_gate`, `test_removed_foundry_does_not_break_project`.
- [x] Ejecutar `python -m pytest tests/test_project.py tests/test_gates.py -q`; comprobar fallos iniciales.
- [x] Leer exclusivamente el workspace; no volver a consultar Foundry desde status/next/validate. Detectar manifest incompleto, schema desconocido, profile/modules cambiados y saltos de etapas sin revisión de gates correspondientes. Una entrada avanzada admite requisitos anteriores pendientes, no los marca completados.
- [x] Implementar checks de gate declarativos: presencia de artifacts, campos requeridos no null/no vacíos de contratos YAML, existencia de evidencias relativas y consistencia de hashes de snapshots/perfil/composición. No ejecutar scripts del proyecto ni código arbitrario desde YAML.
- [x] `BLOCKED` si faltan requisitos obligatorios o integridad; `NEEDS_REVIEW` si checks deterministas pasan pero falta revisión cualitativa; `PASS` si pasan checks y revisión registrada válida para profile/gate. La revisión es una declaración humana trazable, no proof de correctitud por algoritmo. Sin evidencia/reviewer no puede dar PASS.
- [x] next devuelve objetivo/preguntas/outputs/skills/gaps del stage actual, y condiciones para avanzar; no propone pasar de etapa como hecho cumplido. status calcula avance según stages relevantes completados válidos, no porcentaje por archivos presentes. Repetir pruebas.

## Tarea 7: Wizard, adapter opcional y comandos públicos

**Archivos:** crear `src/acos/{intake,llm_adapter,cli}.py`, `tests/test_intake.py`, `tests/test_cli.py`, `tests/test_llm_adapter.py`.

**Interfaces:**
- `collect_profile(initial: ProjectProfile | None, ask: Callable[[str],str]) -> ProjectProfile`, `review_classification(profile: ProjectProfile, classification: Classification, ask: Callable[[str],str]) -> ProjectProfile`.
- `llm_proposal(profile: ProjectProfile, argv: list[str], consent: Callable[[str],bool]) -> Classification | None`.
- `main(argv: list[str] | None = None) -> int`; `__main__` termina con ese code. Comandos y flags definidos en decisiones técnicas, help español.

- [x] Definir `test_wizard_core_questions_at_most_twelve`, `test_conditional_questions_only_when_relevant`, `test_profile_file_still_requires_review`, `test_eof_and_ctrl_c_never_confirm`, `test_default_init_creates_child`, `test_here_requires_no_positional_name`, `test_llm_no_consent_no_subprocess`, `test_llm_invalid_or_timeout_falls_back`, `test_llm_cannot_change_business_facts`, `test_four_commands_exit_codes`.
- [x] Ejecutar `python -m pytest tests/test_intake.py tests/test_cli.py tests/test_llm_adapter.py -q`; comprobar fallos iniciales.
- [x] Wizard: 12 prompts core como máximo: nombre, contexto (cliente/industria/mercado/rol), decisión, problema, éxito, decisor/usuarios, arquetipos propuestos, datos, restricciones, entregables, etapa y runtimes. Datos/ML/GenAI/software activan follow-ups pertinentes. Campos desconocidos se conservan como null/open question; identidad cliente opcional. Confirmaciones de clasificación/composición son revisiones, no nuevos formularios de intake.
- [x] Mostrar Foundry detectado y confirmar antes de guardar ruta; permitir continuar sin Foundry. Vista previa presenta límites/gaps/archivos y aceptación expresa. Tras generar mostrar ruta y pasos `cd`, `claude`/`codex` sin ejecutar esos programas.
- [x] Adapter: stdin JSON solo con decisión/problema/contexto no sensible aprobado; stdout `{archetypes: [...], reasons: [...], unresolved: [...]}` validado. No aplicar datos nuevos al perfil, ejecutar herramientas del LLM ni asumir sus propuestas confirmadas. No persistir payload/respuesta fuera del proyecto ni secretos en manifest. El adapter depende de una configuración explícita del usuario; no se distribuye un proveedor obligatorio.
- [x] Conectar init con tareas 1–5 y los tres comandos de lectura con tarea 6. Repetir pruebas; entregar CLI instalable localmente y help coherente con spec.

## Tarea 8: Integración E2E, distribución y guía operativa

**Archivos:** crear `tests/test_e2e.py`, `tests/test_distribution.py`, `tests/fixtures/profiles/{fraud,research,clv,uplift,unlabeled-anomaly,ui-handoff,inherited-model}.yaml`, `docs/acos/{installation,project-usage,release}.md`; modificar `AGENTIC_CONSULTING_OS.md` para navegación; revisar package-data en `pyproject.toml`.

**Interfaces:** usar únicamente `main`, modelos, catálogo y operaciones de tareas 1–7; no introducir otro resolver para fixtures.

- [x] Definir `test_seven_profiles_compile_only_selected_modules`, `test_installed_wheel_contains_catalog_and_templates`, `test_moved_workspace_runs_without_foundry`, `test_reproducible_plan_from_confirmed_profile`, `test_no_network_in_local_path` y `test_runtime_skill_paths_match_selection`. Afirmar módulos/archivos/snapshots, límites causales/sin labels y gates iniciales no aprobados.
- [x] Ejecutar `python -m pytest tests/test_e2e.py tests/test_distribution.py -q`; comprobar fallos faltantes y documentar qué plataformas se están verificando realmente.
- [x] Completar catálogo/render/CLI para los siete perfiles sin generalizar a partir de conteos ficticios. Siete fixtures prueban software del compiler; no validan skills ni reemplazan las 24 simulaciones de diseño.
- [x] Documentar instalación local `uv tool install .` / `pipx install .` y creación/continuidad manual de stages/gates con ejemplo realista sin datos de cliente. Explicar state canónico, actualización de vistas al cerrar sesión, uso provisional de experimental y revisión de gaps.
- [x] Preparar build wheel/sdist con `python -m build` (dependencia dev `build`), instalar wheel en entorno temporal y ejecutar help + init/status/next/validate sobre fixture. Comprobar recursos sin checkout original ni Foundry; correr `python -m pytest -q` tras autorización de verificación.
- [ ] Repetir instalación y recorrido local en macOS/Linux/Windows cuando haya entornos disponibles. Registrar evidencia/plataformas pendientes; no declarar compatibilidad probada solo por escribir código portable. No instalar runtimes en el equipo sin necesidad/autorización; revisión de rutas nativas no prueba que un harness cargó la skill.
- [x] Release manual: documentar metadatos de paquete, versión, build y verificaciones; separar preparación del paquete de publicación PyPI, que requiere revisión final concreta. Hasta publicar, los comandos de instalación por nombre del spec son experiencia objetivo, no distribución disponible.
- [x] Actualizar navegación del manual y resumen del plan con resultado/limitaciones observadas. Si existe repo autorizado, cerrar con revisión del diff y commits; si no, entregar archivos y evidencia sin inicializar Git.

## Cobertura del spec y orden de ejecución

| Secciones del spec | Tareas |
|---|---|
| 1–6: propósito, arquitectura, familias, intake y perfil | 1, 2, 4, 7 |
| 7–9: resolver, Foundry local, snapshots y feedback | 3, 4, 5; feedback documentado manualmente en 8 |
| 10–11: workspace, runtimes, manual y comandos V1 | 5, 6, 7 |
| 12–13: instalación, plataformas, consentimiento/privacidad | 1, 5, 7, 8 |
| 14–17: aceptación, límites e integración modular | 2, 5, 6, 8 |
| 18–19: inventario y simulaciones | 3, 4, 8, con decisiones vigentes del 6 de octubre |

Orden: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8. Dependencias: contratos comunes antes de componer; catálogo/inventario antes del resolver; snapshots/manifest antes de seguimiento; CLI final antes de distribución. No hace falta completar nuevos experiments del Foundry para iniciar.

## Revisión del plan y handoff

El usuario aprobó el plan y la ejecución nativa. Se implementaron las ocho tareas y se verificaron localmente los contratos, composición, snapshots, comandos, build y distribución. La revisión independiente encontró cuatro Important; todos se corrigieron con regresiones RED→GREEN. Suite local actual: 92 pruebas. Las limitaciones de plataformas/harnesses se conservan explícitas en la guía de release.

Ejecución **nativa** aprobada y realizada. No se inicializó Git ni se publicó el paquete. Los rulings incluyen reservar directorio con creación exclusiva en vez de rename POSIX y validar gates internos mediante GateSpec manteniendo las interfaces externas del plan.
