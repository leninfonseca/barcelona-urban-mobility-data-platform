SELECT
    t.day_period,
    COUNT(*) AS observations,
    AVG(f.free_bikes) AS avg_free_bikes,
    AVG(f.bike_availability_pct) AS avg_bike_availability_pct,
    AVG(f.dock_availability_pct) AS avg_dock_availability_pct

FROM gold_fact_bicing_availability AS f

LEFT JOIN gold_dim_time AS t
    ON f.time_key = t.time_key

GROUP BY
    t.day_period

ORDER BY
    t.day_period;