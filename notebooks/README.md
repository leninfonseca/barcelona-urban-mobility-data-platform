# Fabric / PySpark Notebooks

## Implemented

### nb_bronze_to_silver_districts

Transforms the contextual CKAN payload into `silver_district_context`.

Available repository exports:

- `nb_bronze_to_silver_districts.ipynb`
- `nb_bronze_to_silver_districts.py`

### nb_bronze_to_silver_bicing

Implements the initial single-snapshot Bicing Silver milestone.

Available repository exports:

- `nb_bronze_to_silver_bicing.ipynb`
- `nb_bronze_to_silver_bicing.py`

### nb_bicing_snapshot_history

Production-oriented historical/incremental notebook.

It supports bootstrap and incremental execution, derives a watermark from `silver_bicing_station_history`, reads only newer Bronze snapshots, exits successfully when no new data exists, applies Silver transformations and quality checks, performs an idempotent Delta MERGE and validates watermark advancement.

Historical key:

```text
station_id + snapshot_ingested_at
```

Available repository exports:

- `nb_bicing_snapshot_history.ipynb`
- `nb_bicing_snapshot_history.py`

### nb_gold_bicing_analytics

Builds and validates the analytical Gold layer from `silver_bicing_station_history`.

The notebook:

- validates the Silver historical grain
- creates `gold_dim_station` from the latest known row per station
- generates a deterministic `station_key` with `xxhash64(station_id)`
- creates calendar and time dimensions
- builds `gold_fact_bicing_availability`
- calculates availability and e-bike KPIs
- validates row reconciliation, key uniqueness and referential integrity
- persists the four Gold tables as Delta
- validates the persisted star schema with analytical joins and aggregations
- prints a final Gold summary

Gold tables:

```text
gold_dim_station
gold_dim_date
gold_dim_time
gold_fact_bicing_availability
```

The Gold layer currently uses a full rebuild with Delta overwrite from the validated Silver history.

Available repository exports:

- `nb_gold_bicing_analytics.ipynb`
- `nb_gold_bicing_analytics.py`

## Next

The next project phase is SQL analytics over the Gold tables, followed by the Power BI serving layer.
