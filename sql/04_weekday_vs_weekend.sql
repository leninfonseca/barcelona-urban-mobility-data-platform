SELECT
    d.is_weekend,
    COUNT(*) AS observations,
    AVG(f.free_bikes) AS avg_free_bikes,
    AVG(f.empty_slots) AS avg_empty_slots,
    AVG(f.bike_availability_pct) AS avg_bike_availability_pct,
    AVG(f.dock_availability_pct) AS avg_dock_availability_pct

FROM gold_fact_bicing_availability AS f

LEFT JOIN gold_dim_date AS d
    ON f.date_key = d.date_key

GROUP BY
    d.is_weekend

ORDER BY
    d.is_weekend;