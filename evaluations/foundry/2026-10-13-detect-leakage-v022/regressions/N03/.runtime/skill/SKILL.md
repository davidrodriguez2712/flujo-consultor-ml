---
name: detect-leakage
description: >-
  Usar cuando se auditan features, targets, joins, preprocessing, particiones
  o cross-validation por posible data leakage, disponibilidad incierta,
  entidades recurrentes o señal inesperadamente alta.
status: experimental
version: 0.2.2
domain: data-science
---

# Propósito

Auditar legitimidad de información en predicción, entrenamiento y evaluación.

# Cuándo usar

Revisión de construcción, disponibilidad, fit y particiones de problemas supervisados.

# Cuándo NO usar

Entrenamiento, eliminación automática de features o certificación productiva.

# Inputs

Obligatorios: objetivo, expediente autorizado y contrato de salida. Deseables: decisión, unidad, timestamps, target/horizonte, población, construcción y restricciones.

# Preconditions

Lecturas/herramientas/escritura autorizadas. Capacidad no concede autoridad ni acepta gates. Completar lo independiente y declarar bloqueos.

# Workflow

1. Delimitar scoring, entrenamiento, población y target. Outcomes posteriores pueden ser labels retrospectivos legítimos, nunca features indisponibles.
2. Separar ventana de hechos, cálculo y disponibilidad efectiva. Exportación solo fecha extracción; ni una extracción ni un recálculo posterior demuestran eventos o disponibilidad posteriores.
3. Rastrear familias aplicables: target/post-event, temporal, joins, entidad, preprocessing, encoding, selección, resampling y CV. Ajustar transformaciones con train/fold correspondiente; comprobar labels disponibles al entrenar.
4. Confirmar por mecanismo ilegítimo y fuente, no por solape, identidad o señal. Scoring de cartera conocida admite recurrencia; evaluar clientes nuevos es otro escenario.
5. Clasificar y entregar. Confirmado exige mecanismo demostrado. No determinable identifica una brecha; no declara feature inválida ni segura. Confianza en esa brecha difiere de confianza en leakage.

# Checks deterministas

Con tools autorizadas: hashes, conteos, keys, fechas/cutoffs, joins y orden fit/transform/folds. Igualdad en la muestra puede resolverse por lectura; igualdad o señal alta no prueban mecanismo, ni su ausencia descarta leakage. Distinguir ejecución, inspección y pendiente; no entrenar sin mandato.

# Reglas

Para No determinable explicitar dos condiciones:

- Confirmación: demostrar información posterior usada ilegítimamente, o disponibilidad efectiva posterior usada como disponible al scoring.
- Posible validez temporal: conjuntamente ventana previa y disponibilidad efectiva al scoring, con linaje aplicable. Esto no certifica otras familias.

Exportación no satisface ninguna condición. La acción provisional pide evidencia y reserva uso bajo autoridad del owner. No convierte el predictor en outcome ni certifica invalidez. Mantener la incertidumbre en resumen/final. Conservar hechos documentados y pedir solo lo faltante o corroboración de producción.

Severidad expresa impacto potencial fundamentado; sin evidencia de impacto, declarar no estimable. Exportación tardía no justifica gravedad ni probabilidad. Retirar información intrínsecamente posterior; una alternativa histórica necesita otra fuente/corte verificables, no adelantar el mismo valor futuro.

# Output

Prevalece contrato caller: campos exactos, valores, formato, ruta, persistencia y extensión. Versión0.2.2; no afirmar runtime verificado sin evidencia.

Default: Markdown nuevo en reports/leakage/, frontmatter skill/version/fecha real/inputs/hashes/estado; cinco secciones Resumen, Hallazgos, Evidencia, Preguntas abiertas, Recomendaciones.

Receta compacta: Resumen da estado; Hallazgos solo mecanismos/brechas materiales con componente, conclusión, mecanismo/brecha, fuente, confianza, severidad y acción; Evidencia agrupa fuentes y observaciones válidas; Preguntas pide datos faltantes; Recomendaciones reúne condiciones y acción provisional. Referenciar esas condiciones desde Hallazgos, sin repetirlas. Planificar palabras incluyendo metadata/títulos; una frase por idea, agrupar lo común. Final breve con ruta, sin duplicar reporte.

# Verificación final

- Contrato completo y extensión contada.
- Fuentes sostienen mecanismos; ambas condiciones explícitas cuando corresponden.
- Resumen/final preservan incertidumbre y autoridad.
- Inputs e informes anteriores conservados; checks reales, sin datos inventados.

# Modos de fallo conocidos

Exportación tomada como prueba → exigir mecanismo. Brecha llamada invalidez → No determinable. Secciones redundantes → receta compacta. Riesgos inventados → separar límites y observaciones válidas.

# Límites

No demuestra generalización, causalidad ni ausencia universal de leakage. Producción requiere revisión humana de proceso.

# Referencias

Expediente autorizado; autocontenida, sin dependencia del Foundry ni rutas de clientes.
