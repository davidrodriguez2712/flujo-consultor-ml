---
skill: detect-leakage
version: "0.2.0"
fecha: 2026-10-12
condicion: treatment
estado: auditado_no_determinable
inputs:
  - path: case.md
    sha256: db7f2572bc7e591a8d537735dade9cdbcc1da74a100ecb2dd245673b3540e951
  - path: inputs/context.md
    sha256: ae79d0d67bdd4f71349d51644732c99ae1ce547ad618a6d663a30195042b1c7e
  - path: inputs/dictionary.json
    sha256: 72636cf89cf406c70e90c0c1325ddcb7c89229a915199153c35c9f167c414fe3
  - path: inputs/observations.csv
    sha256: 32ae7c42472e440093583da2798aba677eb2ceae58289e5d5dc77f3e46354532
---

## Resumen

No es determinable si `complaint_count` introduce leakage. Falta tanto la ventana de reclamos contados como su disponibilidad efectiva y versión histórica al scoring. La exportación posterior permite evaluar outcomes conocidos, pero no demuestra que la feature existiera antes de predecir ni que incluya información posterior. El expediente no sustenta certificar su uso válido ni confirmar contaminación.

## Hallazgos

**No determinable — feature de soporte.** Componente: `complaint_count`. Mecanismo posible: contar reclamos ocurridos después del scoring, o incorporar reclamos previos que llegaron al motor después, si la exportación representa el estado de agosto. No hay evidencia que confirme ninguno. Fuente: `inputs/context.md`, párrafo único; `inputs/dictionary.json`, claves `complaint_count`, `feature_available_at` y `construction_code`; CSV, filas de datos 1–3. Confianza: alta en la insuficiencia documental; indeterminada sobre la existencia de leakage. Severidad: potencialmente alta si información indisponible influye en la predicción; impacto no medido. Acción: solicitar definición temporal, trazabilidad de cálculo y disponibilidad histórica antes de usar esta feature en un backtest que pretenda reproducir el scoring.

## Evidencia

La unidad es cliente al scoring `2025-06-01T00:00:00Z`, con target de cancelación en los 30 días siguientes. Las tres filas fueron exportadas el `2025-08-01T00:00:00Z` y contienen conteos 3, 0 y 2. El contexto declara que solo `complaint_count` es feature; IDs, target y fechas son metadata. La presencia de outcomes posteriores para evaluación retrospectiva es compatible con el objetivo y no demuestra uso ilegítimo como predictor.

El diccionario documenta ventana y disponibilidad desconocidas, y código de construcción ausente. Los valores no revelan cuándo sucedieron los reclamos ni cuándo fueron accesibles. La relación observada entre conteos y target tampoco permite identificar un mecanismo causal de leakage.

Checks ejecutados: la utility fija `.runtime/check_inputs.py`, con el Python autorizado del workspace, generó los hashes consignados y contó tres filas CSV. No evalúa leakage. Las fechas y definiciones se inspeccionaron por lectura; no se ejecutaron checks automáticos de disponibilidad, pipeline, entrenamiento ni performance. No hay split, preprocessing ni código de construcción disponibles para evaluar sus mecanismos. Se leyó y aplicó el snapshot de la guía 0.2.0; no se invocó un pluginCLI ni una herramienta Skill.

## Preguntas abiertas

¿Qué intervalo de hechos incluye cada conteo y cuál es su corte? ¿Cuándo llegó cada reclamo y cuándo estuvo disponible el conteo para scoring? ¿Existen snapshots o logs que prueben el valor accesible el 1 de junio, incluyendo revisiones tardías? ¿Cómo se construyen y unen estas features? ¿Cuándo se entrena, qué labels estaban disponibles y cómo se realizan splits y transformaciones?

## Recomendaciones

Obtener evidencia de ventana y disponibilidad conjuntamente. Una fuente histórica con corte verificable, hechos permitidos y acceso anterior o igual al scoring respaldaría el uso; evidencia de reclamos posteriores o disponibilidad tardía confirmaría el mecanismo de contaminación correspondiente. Reconstruir solo si esa trazabilidad existe, conservando reclamos previos legítimamente disponibles.

Aumentar filas no resuelve esta falta de proceso. Documentar la incertidumbre y proponer al responsable mantener pendiente la validación temporal de la feature; no eliminarla automáticamente ni certificar producción. Este reporte no aprueba decisiones de negocio, gates o promociones del Foundry.
