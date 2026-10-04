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

Important fields include:

- `source_id`
- `neighborhood_code`
- `district_code`
- `neighborhood_name`
- `district_name`
- `census_section`
- `value`
- `reference_date`

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
- `silver_processed_at` — time at which Spark processed the row

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

The current dimension represents the latest known descriptive state of each station.

Columns:

- `station_key` — deterministic surrogate key generated with `xxhash64(station_id)`
- `station_id` — natural/business identifier from the source
- `station_uid`
- `station_name`
- `latitude`
- `longitude`
- `has_ebikes`

### gold_dim_date

**Grain:** one row per calendar date between the minimum and maximum Silver snapshot date.

Columns:

- `date_key` — integer formatted as `yyyyMMdd`
- `full_date`
- `year`
- `quarter`
- `month`
- `month_name`
- `day`
- `week_of_year`
- `day_of_week` — Monday = 1 through Sunday = 7
- `day_name`
- `is_weekend`

### gold_dim_time

**Grain:** one row per observed hour/minute combination in Silver snapshots.

Columns:

- `time_key` — integer in `HHmm` form
- `hour`
- `minute`
- `time_label`
- `day_period`

Day periods:

```text
Night      00:00-05:59
Morning    06:00-11:59
Afternoon  12:00-17:59
Evening    18:00-23:59
```

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

Measures and attributes:

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

KPI definitions:

```text
bike_availability_pct = free_bikes / station_capacity * 100
dock_availability_pct = empty_slots / station_capacity * 100
ebike_share_pct        = ebikes / free_bikes * 100
```

Percentages are only calculated when their denominator is greater than zero. Otherwise the KPI remains NULL instead of assigning a misleading numeric value.

## Gold refresh model

Silver is incrementally maintained and remains the historical source of truth.

Gold is currently rebuilt from Silver with Delta `overwrite` and `overwriteSchema=true`.

This is intentional for the current data volume: rebuilding the analytical layer is simple, deterministic and keeps historical rows consistent when KPI logic or dimensional structures change.

## SQL analytical serving model

The SQL Analytics Endpoint exposes the same Gold Delta tables without creating a second physical copy of the model.

The SQL queries consume the fact and dimensions through T-SQL joins and aggregations.

The Power BI serving query presents a denormalized analytical projection with:

- station name and coordinates
- calendar attributes
- time-of-day attributes
- raw availability measures
- Gold KPIs
- station online state
- `availability_status`

`availability_status` is derived with ordered `CASE` logic:

```text
is_online = 0                  → Offline
capacity is NULL or 0          → No capacity
bike_availability_pct < 20     → Low bikes
dock_availability_pct < 20     → Low docks
otherwise                      → Balanced
```

The denormalized serving query does not replace the Gold star schema; it is a consumption-friendly projection over the dimensional model.

## District context relationship

`silver_district_context` is intentionally not joined to the Bicing Gold model yet.

The current Bicing dataset exposes station identifiers and coordinates, while the contextual dataset exposes district/neighborhood identifiers but no direct station key or geometry that supports a reliable join.

The project therefore avoids an artificial name-based relationship. Geographic enrichment can be introduced later through a real spatial mapping.
