# Revisión nativa de preparación

## Alcance

Autor y reviewer local: mismo agente nativo. Sin agentes delegados, review independiente, outputs de modelos o llamadas de pago. La aceptación del alcance de preparación no es autorización de ejecución.

## Comprobaciones

- Seis cases, dos por familia: tres con discrepancia y tres coherentes. No se usaron IDs ni respuestas de rondas anteriores.
- Contrato y datos idénticos entre ramas; única diferencia: tres secciones del workflow. Baseline es una ablación explícita, no una release histórica reconstruida.
- Doce payloads reconstruidos exclusivamente desde common, condiciones y agent_inputs. Ningún archivo de expected, índice privado, protocolo o revisión participa del ensamblado.
- Estado esperado y cuatro obligaciones semánticas por case; acciones prohibidas incluyen omisión de error y falso bloqueo. El checker local recomputa hechos concretos, no depende de outputs inventados de modelos.
- Freeze: hashes de planes y manifest representados con contenido textual exacto. Se corrigió durante preparación una ambigüedad inicial entre hash canónico del objeto y hash del archivo; las aprobaciones del fixture ahora referencian SHA-256 de su texto exacto. No hubo ejecución de modelos ni cambio de criterio después de observar una respuesta.
- Reproducción: writer CSV `.1f` y reader float reproducen selección Q-17; omitirlos produce selección distinta dentro de tolerancia numérica. El caso coherente usa JSON con whitespace diferente y datos tipados/selección iguales, conforme al contrato.
- Etiquetas: Norte, on_time_share, última semana completa 2025-10-20; 92/100=92%. Los dos oracles se mantienen en las 24 permutaciones de sus tablas.
- Las aprobaciones y owners incluidos son explícitamente hipotéticos; la tarea solo autoriza revisar/proponer. No hay permiso para aceptar gates, publicar o alterar artifacts.

## Límites y pendientes

La validación acredita consistencia de los fixtures y qué se envía en los payloads guardados. No acredita aislamiento efectivo del runtime ni eficacia del treatment. Los casos contienen definiciones necesarias y un formato común; no son consultoría totalmente abierta ni ejecución de cambios reales en filesystem.

Pendientes antes de calls: aceptación del protocolo/expected concretos, runtime/modelo/configuración, presupuesto nuevo, transporte compatible con formato común, checker de outputs y verificación de aislamiento. Una sola repetición por condición/case se propone para reducir gasto; solo produciría evidencia exploratoria.

No se recomienda crear/promover una skill o agent a partir de esta preparación.
