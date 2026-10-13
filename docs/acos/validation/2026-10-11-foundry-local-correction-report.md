# Foundry — corrección local y configuración 02

## Resultado

Corrección local aprobada implementada: el prompt común expone el comando exacto de la utility, archivos legibles, única ruta de reporte y límites de Bash/Skill. El guard sigue rechazando comandos alternativos, accesos exteriores y escrituras a inputs. No se relajaron permisos.

Los rechazos ahora conservan nombre de herramienta y preview de argumentos, con máximo8192 caracteres, límites de profundidad/colecciones y redacción de clave conocida del proxy, patrones sk-/Bearer y campos sensibles. No conserva headers ni respuesta completa del proveedor. Esto facilita diagnosticar el comando concreto; no garantiza detectar secretos arbitrarios. El comando desconocido de round01 sigue desconocido: no se reconstruyó ni inventó.

## Verificación local

Dos pruebas nuevas fallaron antes del cambio por ausencia de instrucciones operativas y de `rejected_tool`, y pasaron después. Un tercer check comprueba tamaño y redacción de campos sensibles. Con Claude Code real y proveedor simulado se observó el comando/límites en el contexto enviado y la ejecución del comando exacto, escritura y finalización. El escenario rechazado conservó información útil sin clave/token de prueba y no ejecutó el comando.

Suite completa: **226 pruebas pasadas**, cero fallos/errores/skips, 14.59s. **Cero nuevas llamadas pagadas, US$0 de API en esta corrección**. Las respuestas simuladas suministran el comando correcto: esto acredita transmisión/ejecución/control, no elección espontánea del modelo ni eficacia de detect-leakage. No se cargó .env ni credenciales reales.

## Configuración nueva

`execution-config-02/`:29archivos, verificación PASS_FROZEN_CONFIG, manifest SHA256 `66c77ceb0eccbc72ef6e8f7e65132d3023374077d5f380570391e57c8ee0f941`. Conserva exactamente cases, expected, skill, workflow y protocolo. Solo actualiza fuentes/pruebas e instrucciones de configuración. El nombre `execution-manifest-01.json` se conserva dentro del directorio02 por la interfaz del coordinador.

Plan propuesto: nuevo smoke y seis ejecuciones, máximo8solicitudes por sesión y56globales, sin retries automáticos. Presupuesto propuesto **hasta US$0.099310925 para round02**, manteniendo US$0.10 estimados acumulados junto a los US$0.000689075 de round01. No garantizar completar todos los pares.

## Conservación y pendientes

Se verificaron manifests históricos Foundry de27/12/89archivos, configuración01 de29 y run01 de13: intactos. Evidencia de corrección en `local-correction-01/` con XML, resumen y probe nativo simulado. Foundry canónico y madurez sin cambios. Eficacia NOT_EVALUATED; revisión del autor, no independiente.

Pendiente autorización explícita ligada al manifest02 para cualquier nueva llamada real. El usuario aprobó esta corrección local **sin gasto**, por lo que no se reutiliza approval01 ni se reanuda round01. Después de ejecutar, revisar contenido frente a expected sin reparar outputs; David puede actuar como reviewer distinto del autor, todavía pendiente.
