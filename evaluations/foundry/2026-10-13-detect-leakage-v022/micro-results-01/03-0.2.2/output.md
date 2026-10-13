---
skill: detect-leakage
version: 0.2.2
fecha: 2026-10-13
modo: guia_textual
estado: no_determinable
inputs: context.md, dictionary.json, observations.csv
---

## Resumen

Estado: **No determinable**. No puede recomendarse el uso de complaint_count para scoring hoy. El expediente no documenta ventana de conteo ni disponibilidad efectiva al scoring (2025-06-01). La exportación (2025-08-01) no demuestra nada sobre ese momento.

## Hallazgos

- **Componente:** feature complaint_count.
- **Conclusión:** No determinable; no se confirma leakage ni se declara la feature válida.
- **Brecha:** ventana, disponibilidad y estado temporal no documentados; construction_code y feature_available_at son null.
- **Fuente:** context.md, dictionary.json.
- **Confianza en la brecha:** alta. **Confianza en leakage:** no evaluable.
- **Severidad:** no estimable.
- **Acción:** no usar en scoring hoy; uso reservado a autoridad del owner.

## Evidencia

- Lectura de observations.csv: 3 filas, prediction_at 2025-06-01, exported_at 2025-08-01.
- Comprobación por lectura, no ejecutada: no hay hashes, cutoffs ni joins verificados.
- Tres filas no permiten inferir señal ni validez.

## Preguntas abiertas

- ¿Cuál es la ventana de conteo?
- ¿Cuándo estaba disponible el dato en producción?
- ¿Se usó el estado al scoring o al exportar?
- ¿Existe código de construcción o versión histórica?

## Recomendaciones

- **Confirmación:** demostrar información posterior usada como feature, o disponibilidad posterior tratada como disponible al scoring.
- **Posible validez temporal:** requiere ventana previa y disponibilidad efectiva al 2025-06-01, con linaje verificable.
- **Acción provisional:** no usar en scoring hoy hasta obtener evidencia; los outcomes sirven solo para evaluación retrospectiva.