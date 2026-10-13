# Decisiones

## Inicialización

Composición confirmada; snapshots experimentales aceptados como provisionales. No se aprobaron gates de negocio ni se ampliaron permisos.

Registrar cambios de alcance/etapa, reviewer, evidencia y fecha antes de avanzar.

## 2026-10-09 — Discovery con datos reales

David aprobó diseño y plan; se ejecuta Discovery, sin aprobación de gate. Fuente UCI y copia normalizada congeladas. El solapamiento entre hojas queda documentado; ninguna deduplicación aplicada. La capacidad 100/horizonte90 son supuestos del encargo. Se usan snapshots experimentales, sin editar Foundry ni pilotos anteriores.

## Aprobación humana de Discovery

David responde «aprobado» al paquete Discovery; se registra PASS con evidencia y se avanza a Framing. No se aprueban tratamiento de datos, target, cutoffs ni modelos. Evidencia: reports/discovery/human-approval.json.

## Framing propuesto

La reconciliación se propone conservando multiplicidad máxima por patrón entre hojas; no deduplicación general. Código estándar delimita el target de compras, sin afirmar que lo excluido sea inválido. Preview: 788.187 líneas y 5.852 clientes en toda la historia; no elegibilidad por cutoff aún. Framing no aprobado, fuente/copia normalizada intactas.

## Corrección de alcance del freeze de Discovery

La verificación detectó que dos planes humanos mutables estaban incluidos por error en el freeze. Framing los actualizó legítimamente. Se conservan manifest inicial y planes actuales; se archivan versiones iniciales reconstruidas desde plantilla/perfil y verificadas con sus SHA256 originales. Manifest02 apunta a las versiones históricas. Fuentes, auditoría y snapshots no cambiaron. Evidencia: reports/framing/freeze-incident.json.

- 2026-10-09: David aprobó Framing; registro con SHA en reports/framing/human-approval.json. Avance a Diagnosis. Calendario/aceptación propuestos sin entrenamiento; pendiente aprobación de ambos gates.

- 2026-10-09: David aprobó Diagnosis/data-quality y reglas; avance Execution. JSON derivado de YAML aprobado para runner sin dependencia adicional; hash anclado a aprobación externa. Development de dos modelos fijos pierde4/4 frente a ventas90. No redefinir ventanas, features ni modelos; holdout reservado hasta aprobar Execution.

- 2026-10-09: David aprobó Execution; avance Validation. Selección baseline congelada antes de holdout (timestamp/hashes), solo baseline final evaluado. Ningún modelo descartado reseleccionado. Validación metodológica y cuatro reviews de módulos pendientes. Una única ejecución final registrada; futuras reproducciones solo mismo cálculo en copia aislada.

- 2026-10-09: David aprobó Validation y cuatro reviews; avance Delivery. Recomendación conserva baseline, solo datos/resultados congelados. Memo/reporte/contrato y43claims preparados para review; no publicación ni campaña actual. Planes vivos actualizados como vistas de estado sin cambiar contratos; versiones históricas intactas. Handoff todavía pendiente.

- 2026-10-09: Delivery aprobado por David; avance Handoff. Entorno aislado desde lock y Excel original reproducidos; primera discrepancia debida a persistencia/lectura CSV omitida en harness, corregida y log preservado, sin alterar datos/modelos/tolerancias. Review final nativo, no independiente. Foundry solo lectura/feedback local. Último gate Handoff pendiente antes de COMPLETED.

- 2026-10-09: David aprobó Handoff («si»); manifest263 intacto antes del cierre. Todas las etapas/gates registrados PASS, estado COMPLETED. Cierre no autoriza side effects externos ni cambia madurez Foundry.
