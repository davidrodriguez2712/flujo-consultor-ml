---
name: detect-leakage
description: >-
  Usar cuando se auditan features, targets, joins, pipelines, preprocessing,
  splits o cross-validation por posible data leakage, disponibilidad temporal
  incierta, entidades recurrentes o métricas inesperadamente altas. No sustituye
  data understanding ni entrenamiento de modelos.
status: experimental
version: 0.2.1
domain: data-science
---

# Propósito

Auditar qué información puede influir legítimamente en predicción, entrenamiento y evaluación. Un dato pasado puede llegar tarde; un cliente recurrente puede ser parte válida del escenario.

# Cuándo usar

Al revisar construcción de features, disponibilidad, particiones, transformaciones o resultados sospechosos de un problema supervisado.

# Cuándo NO usar

Para entrenar, optimizar modelos, eliminar features automáticamente o certificar producción. Si falta target, escenario o acceso, auditar lo disponible y declarar lo desconocido.

# Inputs

Obligatorios: objetivo de la auditoría, expediente autorizado y contrato de salida. Deseables: momento de predicción, ventana del target, disponibilidad efectiva, código de construcción/split/fit, escenario operacional y restricciones.

# Preconditions

Lectura, herramientas y escritura autorizadas. La capacidad no concede permisos ni acepta gates. Si una acción requiere información o permiso ausente, detener esa acción y completar la parte independiente.

# Workflow

1. **Delimitar:** identificar decisión, unidad, prediction timestamp, target/horizonte, momento de entrenamiento y población de scoring. Outcomes posteriores son legítimos para evaluar retrospectivamente; no para construir features indisponibles.
2. **Inspeccionar:** para cada feature, separar ventana de hechos, cálculo y disponibilidad. Consultar evidencia de proceso, no inferir fechas por nombres o por exportación.
3. **Rastrear:** revisar familias aplicables: target/post-event, temporal/agregaciones, joins, entidad, preprocessing, encoding, selección de features, resampling y cross-validation. Transformaciones aprendidas se ajustan con train/fold correspondiente. Revisar disponibilidad de labels al entrenar.
4. **Contrastar:** localizar un mecanismo y su fuente. Entidades repetidas no prueban contaminación: distinguir scoring recurrente de clientes conocidos de generalización a clientes nuevos, identidad/features usadas y disponibilidad. Ventanas solapadas tampoco prueban leakage por sí solas.
5. **Entregar:** clasificar Confirmado/Probable/Riesgo/No determinable; recomendar acción proporcional y persistir según el contrato. Mantener incertidumbre útil cuando falta evidencia. Confirmado identifica un mecanismo demostrado; No determinable identifica una brecha, sin declarar inválida o segura la feature. Severidad describe impacto potencial, no probabilidad ni confianza en existencia del mecanismo.

# Checks deterministas

Con herramientas permitidas: hashes, conteos, keys/duplicados, timestamps frente a disponibilidad y cutoff; ventanas y cardinalidad de joins; orden fit/transform, encoding/resampling y folds. Una feature previa es válida solo si también estaba disponible al scoring.

Solape de IDs, señal perfecta o igualdad feature-target son indicios; confirmar requiere mecanismo de construcción/uso ilegítimo. Ausencia de igualdad no descarta target leakage. Separar checks ejecutados de lectura de código y comprobaciones pendientes; no ejecutar pipelines ni entrenar sin mandato.

# Reglas

Ausencia de artefactos no certifica seguridad. No inventar timestamps, métricas, autoridad o checks. Conservar historia válida; retirar del scoring información intrínsecamente posterior y proponer reconstrucción histórica solo con fuente/corte verificables. Si ventana o disponibilidad faltan, pedir ambas: aumentar filas no resuelve esa falta de proceso.

# Incertidumbre y condiciones de decisión

Para una conclusión No determinable entregar: **hecho documentado → dato faltante → condición de confirmación → condición de posible validez → acción provisional**. Confirmar información posterior requiere demostrar hechos posteriores usados como feature o disponibilidad efectiva posterior usada ilegítimamente. Una exportación posterior, incluso de un conteo recalculado, solo fecha la exportación: puede conservar hechos y valores ya disponibles antes. Para posible validez temporal se necesitan conjuntamente ventana previa y disponibilidad efectiva al scoring, además del linaje aplicable.

La acción provisional responde a la falta de acreditación: pedir evidencia y proponer reserva de uso bajo autoridad del owner, sin concluir invalidez demostrada ni convertir una feature en outcome. Distinguir predictor de outcome retrospectivo legítimo. En resumen y respuesta final conservar la misma incertidumbre y condiciones. Comparaciones observables en la muestra pueden resolverse por lectura autorizada; su resultado no demuestra performance ni ausencia universal de leakage.

# Output

**El contrato del caller prevalece sobre esta plantilla.** Antes de redactar, listar sus campos, formato, ruta y extensión; entregar todos. Campos adicionales pedidos —como condición de evaluación— pertenecen a la salida. Usar valores suministrados; si faltan, declarar no especificado y solicitar aclaración, sin inventarlos. La versión de esta skill es 0.2.1; no afirmar verificación del runtime si no ocurrió.

Por defecto: archivo Markdown nuevo en `reports/leakage/`, sin sobrescribir; frontmatter con skill, version, fecha real, inputs/hashes y estado. Cuerpo: Resumen, Hallazgos, Evidencia, Preguntas abiertas, Recomendaciones. Cada hallazgo material usa estos slots: componente; conclusión; mecanismo demostrado o brecha; fuente; confianza en la conclusión; severidad del impacto potencial; acción. Observaciones válidas y limitaciones se distinguen de riesgos demostrados. Referenciar evidencia ya disponible y pedir solo su verificación o lo que realmente falta. Con límite de extensión, agrupar evidencia común y omitir familias ajenas al expediente; no duplicar el reporte en la respuesta final, que entrega resumen y ruta.

# Verificación final

- [ ] Contrato completo: campos, valores, formato, extensión y persistencia.
- [ ] Fuentes respaldan mecanismos; incertidumbre y checks pendientes visibles.
- [ ] No se confundieron exportación/disponibilidad, solape/contaminación o señal/mecanismo.
- [ ] Límites y autoridad respetados; reporte previo conservado.

# Modos de fallo conocidos

Plantilla omite campos del caller → cotejar lista de campos contra salida. Historia previa llega tarde → verificar disponibilidad separada. Recurrencia marcada como leakage → revisar escenario operacional. Señal alta o ausencia de igualdad usada como prueba → exigir construcción y uso. Auditoría extensa sin evidencia → priorizar mecanismos aplicables.

# Límites

No demuestra generalización, efectos estadísticos ni ausencia universal de leakage. La documentación puede discrepar de producción; identificar esa dependencia. La revisión humana de proceso sigue siendo necesaria.

# Referencias

El expediente autorizado es la fuente operacional. Esta skill es autocontenida: no requiere archivos del Foundry, otras skills ni rutas de un cliente para ejecutarse.
