# Manual — Forecasting de volumen semanal para capacidad retail

## Decisión del proyecto

Proponer una previsión semanal de facturas positivas registradas como proxy de carga para planificar preparación.

Métrica de éxito: WAPE y MAE del forecast de una semana; sesgo y error por período como diagnósticos.
Restricciones: Datos públicos reales; contexto y decisión de negocio simulados., Caso inicia en validation para ensayar conjuntamente pautas ya definidas; ninguna etapa anterior se declara aprobada., Forecast de facturas positivas, no demanda latente, unidades físicas, horas, staffing óptimo ni impacto causal., Sin API de pago, servicios externos ni cambios al Foundry o pilotos anteriores.

## Situación al inicializar

Etapa: validation
Objetivo: Revisar solidez metodológica y utilidad para la decisión.

Esta sección es una vista inicial. Leer `.acos/state.yaml` o ejecutar `acos status` y `acos next` para la situación vigente.

## Tu siguiente trabajo

1. Revisar PROJECT, profile y estado canónico; resolver preguntas abiertas.
2. Acordar un contrato de tarea y usar las pautas seleccionadas en `workflow/` y `playbooks/`.
3. Producir outputs con fuentes, supuestos y límites; no llenar campos sin evidencia.
4. Ejecutar `acos validate`; corregir bloqueos y obtener revisión humana.
5. Registrar evidencia, reviewer y decisión en `gate_reviews` del state. Solo después de aprobación explícita modificar etapa y registrar el cambio en DECISIONS.
6. Al cerrar sesión, actualizar STATE, MANUAL y TASKS como vistas del estado vigente.

## Preguntas de la etapa inicial

- ¿Se evita leakage o inferencia causal no identificada?
- ¿Qué límites cambian la decisión?

## Outputs requeridos en esta etapa

- analysis/analysis_plan.md
- analysis/forecast_plan.md
- delivery/storyline.md

## Capabilities disponibles

- Pautas/templates del OS; ninguna skill operativa seleccionada.

Ver CAPABILITIES para cobertura parcial y límites. Una skill experimental no es garantía de un entregable.

## Evidencia e historial

Separar documentos vivos (STATE, MANUAL, TASKS y planes actualizables), evidencia congelada y aprobaciones humanas. Antes de solicitar un gate, conservar copias históricas de los documentos vivos que sustentan la decisión y registrar rutas relativas, versión y SHA-256 en un manifest de evidencia. Excluir el estado y sus vistas actualizables del paquete congelado.

Verificar los hashes antes de revisar y entregar. Guardar la aprobación fuera del paquete, vinculada a la ruta, versión y SHA-256 del manifest exacto revisado; referenciarla en `gate_reviews` y DECISIONS. Una corrección conserva el original y registra nueva versión, motivo e impacto sobre la aceptación previa; no hereda automáticamente su aprobación.

Consultar `workflow/execution-and-qa.md` y `templates/delivery-and-handoff.md`. `.acos/manifest.yaml` describe la composición inicial; no sustituye el manifest de evidencia de negocio. Estas pautas requieren ejecución y revisión explícitas: `acos validate` no verifica automáticamente paquetes históricos.

## Reproducción de resultados

Cuando el resultado depende de cálculos o modelos, registrar entorno/dependencias, código/configuración, comandos e inputs versionados. Documentar el recorrido inputs → transformaciones → escrituras → lecturas → cálculo/fit → outputs, con formatos, tipos, precisión, fechas, nulos y orden cuando importen. Respetar las fronteras de serialización originales; no sustituir artifacts leídos por objetos en memoria sin verificar equivalencia.

Acordar antes del nuevo run las keys de comparación, outputs exactos y tolerancias numéricas justificadas. Comparar también métricas y selección/ranking final: datos cercanos no garantizan la misma decisión. Reproducir en un destino nuevo autorizado, conservar originales e intentos fallidos, e investigar la primera frontera discrepante antes de cambiar tolerancias. No reabrir un holdout para seleccionar estrategias durante la reproducción.

Usar el registro de `templates/delivery-and-handoff.md` y el procedimiento en `workflow/execution-and-qa.md`. `acos validate` no ejecuta ni reproduce el análisis automáticamente.

## QA de cifras y etiquetas

Antes de aceptar o entregar una afirmación material, vincular su cifra a las keys de métrica, método, población y período/cutoff del artifact fuente, con unidad y denominador. Contrastar títulos, leyendas, tablas, texto y logs; un valor existente puede estar atribuido al resultado equivocado.

Identificar períodos por fechas y keys explícitas. Definir “último” dentro del método/población y los períodos elegibles y completos; declarar la fecha concreta y no elegir por posición de fila. Comprobar ventanas, límites y madurez cuando afecten la interpretación. Resolver keys duplicadas o ambiguas antes de aceptar el resultado. Conservar el original y registrar correcciones con fuente, motivo e impacto sobre la aceptación.

Usar `templates/findings-and-qa.md` y `workflow/execution-and-qa.md`. `acos validate` no interpreta automáticamente las etiquetas de los entregables.

## Continuidad

`acos status`: estado, bloqueos y siguiente gate. `acos next`: objetivo, preguntas y outputs del stage actual. `acos validate`: checks y revisión; nunca cambia la etapa.

Antes de invocar una skill comprobar si el runtime la expone. Cambiar profile/composición invalida los hashes y requiere revisar/compilar un workspace nuevo; no hay update automático V1.

## Feedback de capacidades

Registrar observación local (útil/parcial/falló), tarea, versión, evidencia y límites en DECISIONS. Revisar/anonimizar antes de proponer un case o ajuste al Foundry; nunca subir datos ni promover estados automáticamente.

Ensayo de actualización de vista: paquete técnico preparado; aceptación humana pendiente.

## Paquete preparado para tu revisión

Leer PILOT_REPORT.md, decision/recommendation.md y reports/validation/integrated-review.md. El state continúa en validation, IN_PROGRESS; no hay gates aprobados. Las pruebas técnicas son evidencia para tu aceptación, no la reemplazan. El handoff está preparado para inspección.

## Cierre vigente

David aceptó el paquete técnico con límites mediante «Aprobado seguimos». State COMPLETED; validation, delivery y handoff completos desde la entrada acordada. No repetir el análisis ni retunear final como siguiente tarea. La sección anterior de revisión pendiente es histórica; consultar reports/closure/closure.md y handoff/human-approval.json. Uso operativo requiere un alcance nuevo.
