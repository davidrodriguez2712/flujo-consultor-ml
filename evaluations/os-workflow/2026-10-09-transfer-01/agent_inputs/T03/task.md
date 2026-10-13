Revisa por qué no coincide la shortlist de reposición del run de reproducción. Indica el próximo recorrido que debe proponerse para comprobar el resultado contratado.

## Contrato de salida

Devuelve un único objeto JSON, sin fences ni texto adicional, con status (READY, MUST_CORRECT o NOT_DETERMINABLE), findings (lista de objetos con statement y evidence_paths), proposed_actions (lista de strings), next_step (string) y limitations (lista de strings). Las evidence_paths deben corresponder exactamente a claves de los artifacts incluidos.
