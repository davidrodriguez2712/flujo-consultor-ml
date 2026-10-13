# Revisión final nativa del piloto

## Alcance y método

Revisión del conjunto por el mismo ejecutor, como pasada separada de implementación, siguiendo template requesting-code-review. Sin agente revisor por la preferencia explícita de ejecución nativa; no atribuir independencia/fresh-context a esta revisión. Workspace sin Git: se revisan código, plan/spec y manifests/copias históricas, sin crear repositorio ni commits.

## Plan y foco de revisión

1. Hojas/aliases: columnas normalizadas explícitas y errores/aliases ambiguos rechazados; fuente real de dos hojas conservada.
2. Cancelaciones/cantidades/precios/duplicados: filtros con motivos y provenance, máxima multiplicidad entre hojas y repeticiones internas conservadas. Exclusión estándar es convención aprobada, no identidad de mercancía acreditada.
3. Cutoff/horizonte/labels: tests de [inicio,fin), horizonte/history completos, cero observado y madurez al fit. Tenure solo pasado y scaler fittrain.
4. IDs/capacidad/empates: ID textual, ausencia excluida, K efectivo y empate lexicográfico; outcome one_to_one y misma población.
5. Concentración/inestabilidad: por período, Top-1/Top-10 y cancelaciones separados; narrativa no identifica causalidad, ROI o CLV completo.
6. Transferencia: entorno nuevo desde17paquetes locked, reconstrucción desde Excel, seis comparaciones y métricas/decisión; fuente/resultados originales intactos.

## Hallazgos

### Critical / Important

No quedan hallazgos Critical/Important abiertos que invaliden este benchmark bajo contratos/supuestos aprobados. El primer reproductor omitía persistencia/lectura CSV y falló; se corrigió únicamente harness, regression test RED→GREEN y nueva reproducción PASS con tolerancias originales. Incidentes/logs preservados; no ajustar estrategia ni hashes esperados.

### Minor / límites de reutilización

- Helpers analíticos consumen los schemas numéricos/datetime normalizados de este piloto; no son una API general para DataFrames arbitrarios. `top_k` comprueba finitud por conversión pero ordena columna original: strings numéricos fuera del schema pueden ordenarse como texto. Las fuentes de score de este flujo son floats (fit_predict/read_csv); el benchmark y reproducción no están afectados. Registrar para hardening si se exporta el helper como API general, sin cambiar código/resultados congelados del piloto.
- Lock fija versiones, no hashes de wheels ni sistema. Soporte demostrado macOSarm64/Python3.13.2; instrucciones Windows/Linux no constituyen ejecución en esas plataformas.
- Auto-review/artefactos no sustituyen revisión de negocio: Handoff seguirá NEEDS_REVIEW hasta David.

## Conductas consideradas fuera del scope

- Servicio productivo, integración/contacto de campaña y ejecución causal: no autorizados ni observables, no se evalúan como funcionalidades omitidas.
- Eficacia comparativa de skills: uso guiado, sin baseline/treatment ni expected oculto; no elevar madurez.
- Nuevos datos/inputs externos o API genérica: este benchmark está ligado a fuente/schema/hash específicos. Una ampliación requerirá contratos/versión/tests nuevos.
- Evaluación analítica Windows/Linux: no realizada; cobertura del producto ACOS anterior no se transfiere.

## Dictamen

Paquete listo para revisión humana de Handoff, no cierre automático. Recomendación baseline se mantiene; sin afirmar ganancia causal ni superioridad general. Tests original y copia56pasan; seis comparaciones reproducidas, mismos IDs/selección, numéricos dentro rtol1e-8/atol1e-6. Gasto APIUS$0. Revisar límites antes de usar fuera del caso aprobado.
