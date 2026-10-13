# Contrato de selección operacional — propuesta local 0.2.0
Estado: propuesta experimental documental, sin promoción ni integración. Extiende el scope del contrato 0.1.0: además de Top-K, selección binaria pequeña con presupuesto y costes variables, sin routing ni efectos combinatorios.

Separar ranking de riesgo, selección por valor, factibilidad y causalidad. output_type describe el producto; causal_identification.status describe si la evidencia identifica el efecto solicitado. Un ranking descriptivo no resuelve una pregunta causal. No suponer sesgo ni no representatividad cuando el mecanismo de observación es desconocido.

Filtrar elegibilidad antes de ordenar o optimizar. Capacidad es máximo, no obligación de llenado. Top-K descriptivo: seleccionar min(K,elegibles) según score descendente y desempate preespecificado; mantener ese orden, no ordenar después por ID. risk_ranking_ids conserva el ranking completo de elegibles si existen scores.

Cuando el objetivo es valor neto aditivo y existen costes/budget, maximizar la suma de valores bajo suma de costes <= presupuesto y número <= capacidad. Los datos deben definir si el valor ya es neto o debe restarse coste; no descontarlo dos veces. No usar automáticamente score ni ratio valor/coste: en selección indivisible, greedys pueden fallar. Una selección vacía es válida cuando no hay valor positivo. Optimalidad significa óptimo del problema y valores declarados, no política real universal. Desempatar soluciones por menor coste, luego lista de IDs ascendente; ordenar miembros elegidos por valor neto descendente, luego ID.

Si faltan costes o valores críticos, no afirmar óptimo o factibilidad: conservar selection_status=indeterminate, effective_k=null, selected_ids=[] como ausencia de decisión, total_cost/expected_net_value=null. Puede conservarse un ranking descriptivo en risk_ranking_ids sin llamarlo política resuelta.

Precision usa positivos/seleccionados; recall usa positivos seleccionados/positivos de la población solicitada; lift usa precision/prevalencia de esa misma población. Verificar cobertura por métrica. Si todos los seleccionados tienen label, precision puede identificarse aun sin recall/lift poblacionales. Ausente no significa cero. Denominador cero: null, estado undefined y motivo. Con selección vacía y positivos poblacionales conocidos, recall=0; precision/lift indefinidos.

Identificación causal: not_requested si no se pide efecto; identifiable si diseño y supuestos sustentan el estimand; not_identifiable si la evidencia provista no lo identifica; indeterminate si no puede evaluarse el diseño. En un experimento aleatorio por estrato, diferencias de medias pueden estimar efectos promedio bajo supuestos documentados. No convertir ese promedio en efecto individual cierto ni ignorar incertidumbre. Optimizar point estimates no acredita optimalidad bajo incertidumbre ni validez fuera de población.

Justificar con evidencia y cálculos; preguntar solo por brechas que cambien la decisión o su alcance. Gate siempre requiere aprobación humana; producir un output no autoriza ejecución de campañas o inspecciones.
