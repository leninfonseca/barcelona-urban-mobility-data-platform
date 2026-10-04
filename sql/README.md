# SQL Analytics

These T-SQL queries consume the Gold Delta tables through the Microsoft Fabric SQL Analytics Endpoint.

## Queries

### 01_gold_star_schema_preview.sql

Joins the central availability fact with station, date and time dimensions and returns a readable preview of the star schema.

### 02_low_availability_stations.sql

Filters online observations, groups by station and ranks stations by average bike availability.

Key SQL concepts:

- `WHERE`
- `GROUP BY`
- `COUNT`
- `AVG`
- `ORDER BY`

### 03_availability_by_day_period.sql

Uses `gold_dim_time` to compare average availability across:

- Night
- Morning
- Afternoon
- Evening

### 04_weekday_vs_weekend.sql

Uses `gold_dim_date.is_weekend` to compare availability between weekday and weekend observations.

### 05_availability_by_day.sql

Aggregates Gold KPIs by day of week and orders them using `day_of_week` rather than alphabetical day names.

### 06_powerbi_serving_query.sql

Creates a consumption-friendly analytical result by joining:

```text
gold_fact_bicing_availability
+ gold_dim_station
+ gold_dim_date
+ gold_dim_time
```

It also derives `availability_status` with `CASE`:

```text
Offline
No capacity
Low bikes
Low docks
Balanced
```

This query is intended as the SQL-side serving shape for the next Power BI phase.

## Why the SQL layer exists

Spark creates and validates the Gold model.

The SQL Analytics Endpoint provides a familiar T-SQL consumption surface for analysis and BI without duplicating the underlying Gold Delta data.
