# Fabric / PySpark Notebooks

## Implemented

### nb_bronze_to_silver_districts
Transforms the contextual CKAN payload into `silver_district_context`.

### nb_bronze_to_silver_bicing
Implements the initial single-snapshot Bicing Silver milestone.

### nb_bicing_snapshot_history
Production-oriented historical/incremental notebook.

It supports bootstrap and incremental execution, derives a watermark from `silver_bicing_station_history`, reads only newer Bronze snapshots, exits successfully when no new data exists, applies Silver transformations and quality checks, performs an idempotent Delta MERGE, and validates watermark advancement.

Historical key: `station_id + snapshot_ingested_at`.

Repository-friendly code: `nb_bicing_snapshot_history.py`.

## Next

`nb_gold_model` will build the analytical Gold layer.
