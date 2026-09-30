# Fabric / PySpark Notebooks

Fabric Data Factory handles Bronze ingestion. I use notebooks for transformation, data quality and curated-layer logic.

## Implemented

### nb_bronze_to_silver_districts

This notebook performs the full Bronze-to-Silver transformation for the contextual district dataset.

It:

- reads `Files/bronze/opendata/district_data/district_data.json`
- parses the multiline CKAN JSON envelope
- extracts and explodes `result.records`
- flattens the record structure
- renames columns to a consistent English schema
- casts source identifiers and values explicitly
- removes exact duplicates
- adds `silver_processed_at`
- performs row-count, uniqueness, null and range assertions
- writes `silver_district_context` as a Delta table
- reads the Delta table back for validation

A repository-friendly PySpark version is stored in `nb_bronze_to_silver_districts.py`.

## Next notebook

### nb_bronze_to_silver_bicing

The Bicing Bronze payload is now available at:

```text
Files/bronze/citybikes/bicing/bicing_snapshot.json
```

The next notebook will:

- read the nested CityBikes response
- inspect the inferred Spark schema
- extract and explode `network.stations`
- normalize station identifiers, names, coordinates and availability measures
- convert source timestamps explicitly
- add processing metadata
- validate station IDs, coordinates, availability values and row counts
- persist `silver_bicing_station_status` as a Delta table

## Planned notebooks

1. `nb_silver_enrichment`
   - join mobility and contextual/geographic datasets
   - apply window functions and derived attributes

2. `nb_gold_model`
   - build business-ready aggregations, dimensions and facts

3. `nb_incremental_load`
   - preserve historical Bicing snapshots
   - implement watermark patterns
   - add Delta MERGE/upsert logic where appropriate
