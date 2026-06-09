-- ============================================================
-- CREDIT RISK SCORECARD — Parte 1: Data Analyst
-- Script 01: Calidad de datos
-- Dataset: Give Me Some Credit (Kaggle)
-- Motor: DuckDB
-- ============================================================

-- 1. VISION GENERAL DEL DATASET
SELECT
    COUNT(*)                    AS total_registros,
    COUNT(DISTINCT rowid)       AS ids_unicos
FROM read_csv_auto('data/raw/cs-training.csv');

-- 2. VALORES NULOS POR COLUMNA
SELECT
    COUNT(*) - COUNT(MonthlyIncome)     AS nulos_income,
    COUNT(*) - COUNT(NumberOfDependents) AS nulos_dependents,
    ROUND(100.0 * (COUNT(*) - COUNT(MonthlyIncome)) 
        / COUNT(*), 2)                  AS pct_income,
    ROUND(100.0 * (COUNT(*) - COUNT(NumberOfDependents)) 
        / COUNT(*), 2)                  AS pct_dependents
FROM read_csv_auto('data/raw/cs-training.csv');

-- 3. DISTRIBUCION DEL TARGET
SELECT
    SeriousDlqin2yrs                                       AS default_flag,
    COUNT(*)                                               AS total,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2)     AS porcentaje
FROM read_csv_auto('data/raw/cs-training.csv')
GROUP BY 1
ORDER BY 1;

-- 4. ESTADISTICAS POR GRUPO (DEFAULT VS NO DEFAULT)
SELECT
    SeriousDlqin2yrs                                    AS default_flag,
    COUNT(*)                                            AS total,
    ROUND(AVG(age), 1)                                  AS edad_media,
    ROUND(MEDIAN(TRY_CAST(MonthlyIncome AS DOUBLE)), 0) AS ingreso_mediano,
    ROUND(AVG(RevolvingUtilizationOfUnsecuredLines), 3) AS utilizacion_media,
    ROUND(AVG(NumberOfTimes90DaysLate), 2)              AS mora90_media
FROM read_csv_auto('data/raw/cs-training.csv')
GROUP BY 1
ORDER BY 1;

-- 5. TASA DE DEFAULT POR SEGMENTO DE EDAD
SELECT
    CASE
        WHEN age BETWEEN 18 AND 25 THEN '18-25'
        WHEN age BETWEEN 26 AND 35 THEN '26-35'
        WHEN age BETWEEN 36 AND 45 THEN '36-45'
        WHEN age BETWEEN 46 AND 55 THEN '46-55'
        WHEN age BETWEEN 56 AND 65 THEN '56-65'
        ELSE '65+'
    END                                      AS segmento_edad,
    COUNT(*)                                 AS total,
    SUM(SeriousDlqin2yrs)                    AS defaults,
    ROUND(100.0 * AVG(SeriousDlqin2yrs), 2) AS tasa_default_pct
FROM read_csv_auto('data/raw/cs-training.csv')
WHERE age BETWEEN 18 AND 100
GROUP BY 1
ORDER BY tasa_default_pct DESC;

-- 6. TASA DE DEFAULT POR BANDA DE UTILIZACION
SELECT
    CASE
        WHEN RevolvingUtilizationOfUnsecuredLines < 0.10 THEN '0-10%'
        WHEN RevolvingUtilizationOfUnsecuredLines < 0.30 THEN '10-30%'
        WHEN RevolvingUtilizationOfUnsecuredLines < 0.50 THEN '30-50%'
        WHEN RevolvingUtilizationOfUnsecuredLines < 0.70 THEN '50-70%'
        WHEN RevolvingUtilizationOfUnsecuredLines < 0.90 THEN '70-90%'
        ELSE '90-100%'
    END                                       AS banda_utilizacion,
    COUNT(*)                                  AS total,
    SUM(SeriousDlqin2yrs)                     AS defaults,
    ROUND(100.0 * AVG(SeriousDlqin2yrs), 2)  AS tasa_default_pct
FROM read_csv_auto('data/raw/cs-training.csv')
WHERE RevolvingUtilizationOfUnsecuredLines BETWEEN 0 AND 1
GROUP BY 1
ORDER BY tasa_default_pct DESC;