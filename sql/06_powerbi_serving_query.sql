SELECT
    s.station_key,
    s.station_name,
    s.latitude,
    s.longitude,

    d.full_date,
    d.day_name,
    d.day_of_week,
    d.is_weekend,

    t.time_label,
    t.day_period,

    f.snapshot_ingested_at,

    f.free_bikes,
    f.empty_slots,
    f.ebikes,
    f.normal_bikes,
    f.station_capacity,

    f.bike_availability_pct,
    f.dock_availability_pct,
    f.ebike_share_pct,

    f.is_online,

    CASE
        WHEN f.is_online = 0
            THEN 'Offline'

        WHEN f.station_capacity IS NULL
             OR f.station_capacity = 0
            THEN 'No capacity'

        WHEN f.bike_availability_pct < 20
            THEN 'Low bikes'

        WHEN f.dock_availability_pct < 20
            THEN 'Low docks'

        ELSE 'Balanced'
    END AS availability_status

FROM gold_fact_bicing_availability AS f

LEFT JOIN gold_dim_station AS s
    ON f.station_key = s.station_key

LEFT JOIN gold_dim_date AS d
    ON f.date_key = d.date_key

LEFT JOIN gold_dim_time AS t
    ON f.time_key = t.time_key;