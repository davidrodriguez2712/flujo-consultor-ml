# Decisiones

## 2026-10-08 — Diseño e inicialización

David aprobó el diseño del piloto sintético de riesgo de crédito. Se generó un workspace nuevo mediante la CLI instalada y se usaron snapshots experimentales compatibles. No se promovieron capacidades ni modificó el Foundry.

## 2026-10-08 — Discovery preparado

Generator reproducible, seed 20261008, cinco tablas. Para el laboratorio se fija label completa al día 97, extract 2026-01-15, sin outcomes de rechazadas. Los antecedentes son resúmenes sintéticos, no un ledger de pagos.

Discovery queda IN_PROGRESS / NEEDS_REVIEW. La aprobación del diseño no se registró como aprobación del gate. No se avanzó a Framing ni se entrenaron modelos. No hay calls adicionales a APIs.

## 2026-10-08 — Discovery aprobado y avance a Framing

Tras presentar el paquete de Discovery con revisión humana pendiente, David indicó «continúa». Se registra como aprobación de ese paquete y autorización para avanzar. `gate_reviews.discovery`: PASS, reviewer David, evidencia y hash del perfil compilado. Discovery queda completado; ninguna otra etapa se declara aprobada.

## 2026-10-08 — Framing propuesto

Se preparan métrica primaria Brier, métricas secundarias, separación de poblaciones, ranking por riesgo hasta 100/mes y aceptación. Propuestas sujetas a revisión de Framing, sin cambios al perfil compilado ni métricas observadas de modelo.

## 2026-10-08 — Framing aprobado y avance a Diagnosis

David respondió «aprobado» tras el paquete de Framing. Se registró framing PASS con reviewer, evidencia y hash del perfil; se completó Framing y se avanzó explícitamente a Diagnosis. Brier como primaria, métricas secundarias, población y ranking por riesgo aprobados según ese paquete.

## 2026-10-08 — Diagnosis preparado

Se aplicaron manualmente las pautas de los snapshots understand-dataset, design-validation y detect-leakage 0.1.0 experimental; no es una prueba nueva de carga automática en runtimes nativos ni comparación baseline/treatment de capacidades. Reportes con provenance y checks ad hoc archivados. No se crearon nuevas skills ni se modificó Foundry.

Se propone fit al 2025-07-01 con 2.140 solicitudes concedidas con label disponible, holdout julio–septiembre y extract 2026-01-15. Fecha/cadencia/features/bins pendientes de revisión de Diagnosis. El Top-K mensual se declara benchmark retrospectivo, sin simular decisión online antes del desembolso.

Diagnosis y data-quality quedan NEEDS_REVIEW. No se entrenó modelo ni se ejecutó un split persistente. Los checks globales de calidad usan outcomes; no afirmar holdout ciego. La fase final no tiene métricas ni prevalencia agregada en esta etapa.

## 2026-10-08 — Diagnosis y data-quality aprobados

David respondió «arpbado», interpretado como «aprobado», tras presentar el paquete de Diagnosis con ambos gates pendientes. Registrados PASS, reviewer David, evidencia y hash del perfil. Diagnosis completado; avance a Execution autorizado.

## 2026-10-08 — Baseline fijo y revisión previa

Regresión logística L2 stdlib: cinco features, mediana/escala solo train, 600 iteraciones, learning_rate 0.05, L2 0.01; referencia prevalencia. Sin tuning. Tests RED antes de implementación y GREEN después. La revisión detectó falta de desgloses mensuales/nuevos/recurrentes; corregido con RED/GREEN antes del freeze. Minor de tests documentadas.

## 2026-10-08 — Development ejecutado

Código/configuración/inputs congelados antes del run principal; pruebas temporales previas sobre copias del mismo fixture declaradas. Train 1.248, validation 298. Brier 0.104092 vs 0.116932, ROC-AUC 0.708430. Checks y review por otro agente coinciden. No métricas finales, nuevas llamadas API ni cambios al Foundry. Execution sigue NEEDS_REVIEW; no se autoriza uso crediticio real ni promoción de skills.

## 2026-10-08 — Execution aprobado y avance a Validation

David respondió «apeobado», interpretado como «aprobado», tras el paquete Execution. Registrado PASS, evidencia/reviewer/hash; Execution completado. Se autorizó refit y evaluación final con la configuración conservada.

## 2026-10-08 — Evaluación final

Runner nuevo con nueve tests RED/GREEN en fixtures manuales y revisión técnica previa sin Critical/Important. Baseline y development intactos; finalrunner/policy/inputs/contratos congelados antes del run. Refit único con2.140filas al2025-07-01;900scores persistidos antes de labels. Evaluación447concedidasmaduras,60positivos;453rechazadas sinoutcome. Brier0.102487 vs0.116530,ROC-AUC0.752283. Mejora puntual, no generalizaciónreal o causalidad.

Top-100globalcoverage26%/22%/26%; métricas de esa lista no identificadas. Se documentan benchmark retrospectivo y desajustes/tamaños de calibración. No se cambió modelo, bins o configuración tras observar final.

Checks y review por otro agente coinciden; sin calls API, cambios al Foundry o publicación. Los cinco gates de Validation quedan NEEDS_REVIEW; no hay avance a Delivery ni autorización de uso real.

## 2026-10-08 — Validation aprobada y avance a Delivery

David respondió «aprobsdo», interpretado como «aprobado», tras presentar el paquete de cinco gates de Validation. Registrados PASS con reviewer/evidencia/hash, Validation completada y avance explícito a Delivery. Se aprueba la evidencia y sus límites, no una política crediticia real.

## 2026-10-08 — Delivery preparado

Decision memo, informe analítico, recomendación, contrato y ocho claims trazables. Recomendación propuesta: conservar prototipo como evidencia sintética; decisión global parcialmente respondida por labels no observados y falta de política online. Próximo trabajo debe definir política, población/outcomes y evaluación apropiada; no completar rechazadas como negativas ni asumir que observar concedidas resuelve riesgo contrafactual.

65 campos y19links locales comprobados; review documental por otro agente sin hallazgos bloqueantes. No modelos nuevos, calls API, envío o cambios al Foundry. Delivery sigue NEEDS_REVIEW; después de aprobación se preparará handoff.

## 2026-10-08 — Delivery aprobado y Handoff preparado

David respondió «aprobado» tras el paquete de Delivery. Registrado PASS con reviewer, evidencia y hash; Delivery completado y avance a Handoff. Runbook, handoffs técnico/negocio, feedback y pendientes preparados. Replay en copia fuera del checkout: 6 archivos de datos, 6 JSON development y 7 JSON final idénticos; metadata salvo timestamp. Integridad histórica conservada. Sin nuevas calls API, tuning, cambios al Foundry o promoción de capacidades. Handoff requiere aprobación humana antes del cierre.

## 2026-10-08 — Handoff aprobado y piloto cerrado

David respondió «aprobar» tras el paquete de Handoff. Registrado PASS con reviewer, evidencia y hash del perfil. Siete etapas completadas, estado COMPLETED, sin próximos gates. Se conserva el paquete revisado intacto y se crea un inventario de cierre separado para estado/vistas. Resultado sintético y decisión global parcialmente respondida; capacidades experimental, sin cambios al Foundry ni llamadas API adicionales.
