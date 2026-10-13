# Contexto del engagement

## Encargo simulado

Un responsable comercial de e-commerce necesita proponer hasta 100 clientes al mes para revisión comercial según ventas positivas esperadas a 90 días. El cliente, owner, capacidad y horizonte del encargo son supuestos del piloto. David revisa los gates; no existe una campaña ni autoridad para contactar clientes reales.

## Datos reales

Online Retail II, Chen, D. (2012), UCI, DOI 10.24432/C5CG6D. Fuente: https://archive.ics.uci.edu/dataset/502/online+retail+ii. Licencia CC BY 4.0. Archivo original `data/raw/online_retail_II.xlsx`; SHA256 `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980`.

La auditoría completa verifica 1,067,371 filas en dos hojas, desde 2009-12-01T07:45:00 hasta 2011-12-09T12:50:00. Identificadores de cliente ausentes en 22.77% de filas. No conocemos latencias de registro o correcciones históricas.

## Qué decisión puede respaldar

Comparar retrospectivamente un ranking por ventas positivas futuras con un baseline, en clientes identificables con historia. No identificar efecto de contacto, margen, ingresos netos, CLV completo ni ROI. Modelos y labels no se han construido.

## Preguntas de Discovery

1. Aprobar tratamiento del solapamiento entre hojas antes de agregarlas para negocio.
2. Definir qué códigos corresponden a mercancía, cargos, ajustes o casos inciertos.
3. Elegir población y reportar cobertura excluida por ausencia de ID.
4. Confirmar definición de target/ventanas y supuesto de disponibilidad retrospectiva.
5. Fijar cutoffs y aceptación sin observar desempeño del holdout.

## Propuesta para Framing, aún sin aprobación

Cliente y cutoff mensual; historia 180 días, baseline 90 días, horizonte 90 días y capacidad máxima 100. Target de ventas positivas registradas, con cancelaciones analizadas por separado y exclusiones explícitas. El diseño aprobado permite proponer estos contratos; no aprueba resultados ni gates.
