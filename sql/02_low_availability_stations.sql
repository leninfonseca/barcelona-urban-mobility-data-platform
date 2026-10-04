SELECT TOP 20
    s.station_name,
    COUNT(*) AS observations,
    AVG(f.bike_availability_pct) AS avg_bike_availability_pct

FROM gold_fact_bicing_availability AS f

LEFT JOIN gold_dim_station AS s
    ON f.station_key = s.station_key

WHERE f.is_online = 1

GROUP BY
    s.station_name

ORDER BY
    avg_bike_availability_pct ASC;