import duckdb

con = duckdb.connect()

print("=== DISTRIBUCION DEL TARGET ===")
resultado = con.execute("""
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
""").df()

print(resultado)
