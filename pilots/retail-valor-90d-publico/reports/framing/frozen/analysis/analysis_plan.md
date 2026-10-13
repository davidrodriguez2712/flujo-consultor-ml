# Plan analítico del engagement

Framing propuesto: contrato en framing/retail_contract.yaml. Antes de entrenar, Diagnosis verificará población, solapamiento, exclusiones, repeticiones, cobertura temporal y cutoffs con historia/horizonte completos.

Baseline: ventas positivas históricas90; RFM como comparación secundaria. Máximo Ridge sobre log1p(target) y una alternativa HistGradientBoosting preespecificada en el plan. Los outputs serán cliente/cutoff; no se entrenó ni generó target.

Holdout y acceptance_decision se congelarán en Diagnosis sin observar desempeño de modelos. Reproducir transformaciones y checks de no futuro; preservar fuente, snapshots y evidencia histórica.
