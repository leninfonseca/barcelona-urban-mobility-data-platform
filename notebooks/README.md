# Fabric / PySpark Notebooks

Fabric Data Factory handles Bronze ingestion. I use notebooks for transformation, data quality and curated-layer logic.

## Implemented

### nb_bronze_to_silver_districts

This notebook performs the full Bronze-to-Silver transformation for the contextual district dataset.

It:

- reads the CKAN Bronze JSON
- extracts and explodes `result.records`
- normalizes names and types
- validates critical data-quality rules
- writes `silver_district_context` as Delta

A repository-friendly PySpark version is stored in `nb_bronze_to_silver_districts.py`.

### nb_bronze_to_silver_bicing

This notebook performs the Bronze-to-Silver transformation for CityBikes Bicing station data.

It:

- reads `Files/bronze/citybikes/bicing/bicing_snapshot.json`
- extracts and explodes `network.stations`
- flattens station and `extra` fields
- normalizes identifiers and measures
- explicitly parses the source timestamp
- derives `station_capacity`
- removes duplicate station snapshots by `station_id + source_timestamp`
- separates critical assertions from non-critical warnings
- adds `bike_breakdown_valid`
- writes `silver_bicing_station_status` as Delta
- validates the persisted table

The current validated output contains 544 rows.

A repository-friendly PySpark version is stored in `nb_bronze_to_silver_bicing.py`.

## Planned notebooks

1. `nb_bicing_snapshot_history`
   - preserve multiple station snapshots
   - add deterministic ingestion timestamps/partitions
   - prevent duplicate reprocessing

2. `nb_silver_enrichment`
   - join mobility and contextual/geographic datasets
   - apply window functions and derived attributes

3. `nb_gold_model`
   - build business-ready dimensions, facts and KPIs

4. `nb_incremental_load`
   - implement incremental patterns
   - add Delta MERGE/upsert logic where appropriate
