# Runbook — Piloto sintético de churn y retención

**Fecha:** 2026-10-07.  
**Estado:** preparado para revisión del gate handoff; cierre pendiente.  
**Responsable de conservar el laboratorio y reviewer:** David Rodríguez.  
**Usuario de negocio:** rol ficticio de retención; no existe una operación real desplegada.

## 1. Qué recibes

Un workspace ACOS con contexto, contratos, approvals, datos sintéticos reproducibles, baseline, evaluación temporal, decision memo y snapshots de tres skills experimental. Delivery está aprobado; handoff requiere su propia revisión.

Resultado del holdout julio–diciembre de 2025: Precision@50 media 10,67%, Recall@50 11,02% y Lift@50 2,52. Se seleccionaron 300 observaciones cliente-mes y 32 fueron positivas. No hubo contactos ni retención causada por el modelo.

## 2. Primera lectura y continuidad

Desde la carpeta del piloto:

1. Leer [decision memo](../decision/recommendation.md) y [contrato de entrega](../delivery/delivery_contract.md).
2. Consultar [evaluación final](../validation/model_validation.md) y [feedback de capabilities](capability_feedback.md).
3. Leer .acos/project-profile.yaml, .acos/state.yaml, .acos/modules.yaml, PROJECT.md, MANUAL.md y CAPABILITIES.md. El perfil conserva el intake; framing y approvals registran acuerdos posteriores. State es canónico para el avance.
4. Con ACOS instalado, ejecutar los comandos siguientes. No cambian etapa ni archivos.

```bash
acos status
acos next
acos validate --gate handoff
```

El resultado actual esperado de handoff es NEEDS_REVIEW (exit 3), porque la revisión humana de este runbook está pendiente. Si hay hallazgos de integridad o archivos faltantes, corregir su causa antes de pedir cierre.

La instalación local de ACOS está documentada en [installation](../../../docs/acos/installation.md). Requiere Python 3.11+; no está publicado en PyPI. El workspace contiene los snapshots seleccionados y no necesita consultar el Foundry para leerlos. ACOS instalado es necesario para sus comandos; los scripts de datos/modelo usan la biblioteca estándar de Python.

## 3. Mapa de evidencia

| Qué necesitas | Dónde está |
|---|---|
| KPI, unidad, horizonte y capacidad | framing/framing.yaml y framing/metrics.md |
| Protocolo temporal aprobado | validation/validation_design.md |
| Datos vigentes, v2 | data/raw/ y data/raw/manifest.json |
| Diccionario y contrato | data/dictionaries/README.md y data/data_contract.yaml |
| Diagnóstico y leakage | reports/dataset/ y reports/leakage/ |
| Baseline y nueve folds de desarrollo | analysis/baseline.py y analysis/outputs/baseline-development/ |
| Modelo final fijo | analysis/outputs/baseline-development/final-model.json |
| Evaluación final y scoring | analysis/evaluate_holdout.py y analysis/outputs/holdout-final/ |
| Checks de entrenamiento y holdout | analysis/outputs/baseline-audit.json y analysis/outputs/holdout-audit.json |
| Inventario del delivery aprobado | delivery/delivery-manifest.json |
| Aprobaciones y rationale | evidence/approvals/ y DECISIONS.md |
| Comparación exploratoria de skill | evaluation/design-validation/review.md |

Los directorios data/interim/generator-draft-v0 y generator-v1-before-diagnosis son archivos históricos con defectos documentados, no fuentes vigentes. Conservarlos para trazabilidad, sin mezclarlos con data/raw.

## 4. Reproducir datos y desarrollo

Requisitos: Python 3.11+ y destinos nuevos. En algunos sistemas el ejecutable se llama python3 o py; los ejemplos usan python. Ejecutar desde la carpeta del piloto, reemplazando las rutas por destinos vacíos locales:

```bash
python analysis/generate_synthetic_data.py --output /ruta/a/datos-reproducidos
python analysis/baseline.py --output /ruta/a/desarrollo-reproducido
```

El generador usa seed 20261007. Comparar los cuatro CSV con los hashes de data/raw/manifest.json. El baseline usa data/raw v2 del workspace, no automáticamente el destino del generador. Comparar los cinco JSON de desarrollo con analysis/outputs/baseline-audit.json. Las reproducciones anteriores fueron idénticas byte a byte. Una diferencia requiere revisar Python, código, archivos y hashes antes de confiar en resultados; no sustituir originales para forzar coincidencia.

Para tests del piloto, con pytest disponible:

```bash
python -m pytest -q analysis/test_baseline.py analysis/test_holdout.py
```

Estos 13 tests cubren comportamiento analítico y del runner; los 92 tests del producto residen en el checkout original, no forman parte del workspace portable del piloto. La suite combinada de 105 pasó en macOS. No se ejecutó este piloto completo en Windows ni Linux; no inferir compatibilidad nativa comprobada por tener scripts portables.

## 5. Preservar el test final

El modelo final se entrenó con 26.839 filas disponibles al 1 de julio de 2025. El holdout de julio–diciembre se evaluó una vez, sin refit ni tuning. Metadata conserva hashes del modelo, policy y runner; enero 2026 no se evaluó porque sus labels siguen pendientes en la extracción simulada del 15 de enero.

La evaluación autorizada está preservada en holdout-final. Auditar sus scores, resultados y hashes no crea una nueva reserva ni autoriza elegir otro modelo usando esos outcomes. Para una reproducción técnica explícita en destino nuevo, el runner disponible es:

```bash
python analysis/evaluate_holdout.py --output /ruta/a/evaluacion-reproducida
```

Verifica artefactos congelados antes de puntuar y rechaza sobrescritura. Una reproducción técnica no es una evaluación independiente y no se debe usar para tuning. El cierre no requiere volver a ejecutar el test observado. Nuevas mejoras guiadas por sus resultados necesitan otro protocolo y datos reservados.

## 6. Integridad y resolución de problemas

- **Hash distinto:** detener interpretación, identificar el archivo que cambió y contrastar con manifests/audits. Conservar evidencia original; no editar hashes para saltar gates.
- **Destino existente:** usar carpeta nueva; los scripts rechazan sobrescritura.
- **Pending o features posteriores:** revisar fuentes y disponibilidad; no completar target con cero ni retirar checks.
- **STATE/MANUAL contradictorios:** usar .acos/state.yaml y actualizar vistas tras revisión autorizada.
- **Skill ausente en el runtime:** comprobar snapshots y disponibilidad nativa. No afirmar que se invocó una skill al aplicar sus pautas manualmente.
- **Necesidad de cambiar negocio, datos o módulos:** revisar un nuevo contexto/protocolo. V1 no tiene actualización automática del perfil/composición; seguir instalación y flujo de inicialización, sin modificar el perfil firmado para forzar PASS.

[Inventario de handoff](handoff-manifest.json) registra hashes del runbook, feedback y evidencias de approvals/estado incluidas al preparar revisión. No es backup completo ni incluye futuros cambios de state al aprobar cierre. Copiar el workspace completo, incluyendo .acos, .agents y .claude, si se necesita mover el laboratorio. No depender de rutas temporales de las comprobaciones como única copia.

## 7. Pendientes y próximos proyectos

| Pendiente | Responsable propuesto | Condición de inicio |
|---|---|---|
| Aprobar handoff y registrar cierre | David, reviewer | Revisar runbook, evidencia y límites |
| Review técnico independiente | Reviewer a designar | Acceso autorizado a artefactos, criterios previamente definidos |
| Piloto con datos reales | Owner operacional a designar con negocio | Contexto, permisos, target, disponibilidad y protocolo nuevos |
| Evaluar efecto de una intervención | Negocio y equipo analítico a designar | Intervención definida y diseño causal viable y autorizado |
| Revisar feedback Foundry | David | Anonimizar, comparar otros casos y revisar catálogo existente |

No hay mantenimiento de producción ni compromiso de SLA, presupuesto o campaña. Los pendientes de un futuro proyecto real no bloquean la entrega del laboratorio cuando su alcance y límites se aceptan.

## 8. Criterios de cierre de este laboratorio

- Delivery aprobado y evidencia accesible.
- Datos, policy, modelo y outputs originales conservan hashes.
- Instrucciones de lectura/reproducción, límites y responsables claros.
- Feedback local distingue uso manual, prueba comparativa y aprobación humana; no promociona skills automáticamente.
- Revisión humana explícita del runbook; registrar evidencia antes de cerrar .acos/state.yaml y actualizar vistas.

Este handoff no certifica generalización real, ROI, causalidad ni producción. La revisión actual es del laboratorio; no se ha publicado ni enviado a terceros.
