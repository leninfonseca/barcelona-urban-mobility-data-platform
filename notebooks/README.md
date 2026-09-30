# Fabric / PySpark Notebooks

Fabric Data Factory handles Bronze ingestion. I use notebooks for transformation, quality and curated-layer logic.

## Implemented

### nb_bronze_to_silver_districts

The first notebook is operational and performs the full Bronze-to-Silver transformation for the contextual district dataset.

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

## Planned notebooks

1. `nb_bronze_to_silver_<mobility_source>`
   - normalize the first mobility-specific source
   - enforce source-specific quality rules
   - persist a curated Delta table

2. `nb_silver_enrichment`
   - join mobility and contextual/geographic datasets
   - apply window functions and derived attributes

3. `nb_gold_model`
   - build business-ready aggregations, dimensions and facts

4. `nb_incremental_load`
   - implement watermark patterns
   - add Delta MERGE/upsert logic
