# Data Model

## Bronze

Context:

```text
Files/bronze/opendata/district_data/district_data.json
```

Bicing history:

```text
Files/bronze/citybikes/bicing/history/year=YYYY/month=MM/day=DD/bicing_YYYYMMDD_HHMMSS.json
```

## Silver

### silver_district_context

Typed contextual observations from Barcelona Open Data.

### silver_bicing_station_status

Initial single-snapshot Bicing milestone.

### silver_bicing_station_history

Historical Bicing Delta table.

**Grain:** one station observation per ingestion snapshot.

**Logical key:**

```text
station_id + snapshot_ingested_at
```

Important timestamps:

- `source_timestamp` — timestamp supplied by the upstream API
- `snapshot_ingested_at` — capture time derived from the Bronze filename
- `silver_processed_at` — Spark processing time

The model does not assume a fixed station count. Historical observations remain preserved when a station is absent from a later snapshot.

## Gold

Gold is modeled as a star schema.

```text
                    gold_dim_station
                           │
                           │ station_key
                           ▼
gold_dim_date ──> gold_fact_bicing_availability <── gold_dim_time
```

### gold_dim_station

**Grain:** one row per distinct station observed in Silver.

The dimension represents the latest known descriptive state of each station.

Columns include:

- `station_key`
- `station_id`
- `station_uid`
- `station_name`
- `latitude`
- `longitude`
- `has_ebikes`

`station_key` is generated deterministically with `xxhash64(station_id)`.

### gold_dim_date

**Grain:** one row per calendar date between the minimum and maximum Silver snapshot date.

Columns include:

- `date_key`
- `full_date`
- `year`
- `quarter`
- `month`
- `month_name`
- `day`
- `week_of_year`
- `day_of_week`
- `day_name`
- `is_weekend`

### gold_dim_time

**Grain:** one row per observed hour/minute combination.

Columns include:

- `time_key`
- `hour`
- `minute`
- `time_label`
- `day_period`

### gold_fact_bicing_availability

**Grain:** one station observation per ingestion snapshot.

**Logical key:**

```text
station_key + snapshot_ingested_at
```

Foreign keys:

- `station_key` → `gold_dim_station`
- `date_key` → `gold_dim_date`
- `time_key` → `gold_dim_time`

Measures and attributes include:

- `free_bikes`
- `empty_slots`
- `ebikes`
- `normal_bikes`
- `station_capacity`
- `is_online`
- `bike_breakdown_valid`
- `bike_availability_pct`
- `dock_availability_pct`
- `ebike_share_pct`
- `snapshot_ingested_at`
- `source_timestamp`

## Gold refresh model

Silver is incrementally maintained and remains the historical source of truth.

Gold is rebuilt from Silver with Delta `overwrite` and `overwriteSchema=true`.

For the current data volume, rebuilding the analytical layer is deterministic and keeps KPI logic consistent across the full history.

## SQL analytical serving model

The SQL Analytics Endpoint exposes the same Gold Delta tables without creating a second physical copy.

The versioned T-SQL queries perform joins and aggregations over the star schema and include a consumption-friendly serving projection.

## Power BI semantic model

Power BI consumes the physical Gold star schema directly.

Relationships:

```text
gold_dim_station[station_key]  1 ─── * gold_fact_bicing_availability[station_key]
gold_dim_date[date_key]        1 ─── * gold_fact_bicing_availability[date_key]
gold_dim_time[time_key]        1 ─── * gold_fact_bicing_availability[time_key]
```

Cross-filter direction is single, from dimensions to fact.

### DAX measures

The report defines:

```text
Total Observations
Bike Availability %
Dock Availability %
E-bike Share %
Online Observations
Online Observation %
```

Availability measures use weighted ratios over base fact values.

For example:

```text
Bike Availability %
= SUM(free_bikes) / SUM(station_capacity)
```

This is intentionally different from taking a simple average of row-level percentages because stations can have different capacities.

The measures are evaluated dynamically under Power BI filter context.

## District context relationship

`silver_district_context` is intentionally not joined to the Bicing Gold model yet.

The current Bicing dataset exposes station identifiers and coordinates, while the contextual dataset exposes district/neighborhood identifiers but no reliable direct key or geometry.

The project therefore avoids an artificial name-based relationship. Geographic enrichment can be introduced later through a real spatial mapping.
