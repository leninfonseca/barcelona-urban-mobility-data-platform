SELECT TOP 50
    s.station_name,
    d.full_date,
    t.time_label,
    t.day_period,

    f.free_bikes,
    f.empty_slots,
    f.ebikes,
    f.normal_bikes,
    f.station_capacity,

    f.bike_availability_pct,
    f.dock_availability_pct,
    f.ebike_share_pct,

    f.is_online

FROM gold_fact_bicing_availability AS f

LEFT JOIN gold_dim_station AS s
    ON f.station_key = s.station_key

LEFT JOIN gold_dim_date AS d
    ON f.date_key = d.date_key

LEFT JOIN gold_dim_time AS t
    ON f.time_key = t.time_key

ORDER BY
    d.full_date DESC,
    t.time_key DESC,
    s.station_name;