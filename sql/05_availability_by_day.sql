SELECT
    d.day_name,
    d.day_of_week,

    COUNT(*) AS observations,

    AVG(
        f.bike_availability_pct
    ) AS avg_bike_availability_pct,

    AVG(
        f.dock_availability_pct
    ) AS avg_dock_availability_pct

FROM gold_fact_bicing_availability AS f

LEFT JOIN gold_dim_date AS d
    ON f.date_key = d.date_key

GROUP BY
    d.day_name,
    d.day_of_week

ORDER BY
    d.day_of_week;