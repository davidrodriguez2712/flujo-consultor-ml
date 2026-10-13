Devuelve solo tres acciones de seguimiento y una explicación breve del estado del expediente, dentro del contrato indicado. No redactes un task ni una plantilla de tarea.

## Contrato de salida

Un único objeto JSON, sin fences ni texto externo, con status (READY, MUST_CORRECT o NOT_DETERMINABLE), findings (lista de objetos con statement y evidence_paths), proposed_actions (lista de strings), next_step (string), limitations (lista de strings). Se permiten campos adicionales JSON; no se exige nombre particular para ellos. evidence_paths debe corresponder exactamente a claves de los artifacts incluidos.
