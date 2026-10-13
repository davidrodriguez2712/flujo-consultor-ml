# Model brief del refit final

Reutilizar `analysis/credit_baseline.py` 0.1.0 intacto y sus parámetros conservados: regresión logística L2, cinco features,600iteraciones,lr0.05,L2=0.01, sin tuning. Fit de mediana/mean/escala y referencia constante únicamente en train disponible al 2025-07-01. Intercepto sin penalizar; modelos/transformaciones fijos durante julio–septiembre.

La lista de train se reconstruye con disponibilidad individual de labels, no usando observed al extract como evidencia de disponibilidad histórica. Preflight de Diagnosis:2.140filas y249positivos. La referencia final se vuelve a estimar con ese train; no conservar la prevalencia vieja de development. Ningún target del periodo final entra al refit.

Scoring sobre todas las solicitudes del periodo con application_id/customer_id solo como metadatos. Desempeño evaluable condicionado a concedidas maduras; ausencia de labels de rechazadas impide afirmar calibración para ellas. Interpretación y resultados quedarán en `validation/model_validation.md` tras ejecutar con freeze.

El wrapper final es un artefacto del piloto, no nueva skill ni modificación del compiler. No promueve capacidades ni autoriza uso real.
