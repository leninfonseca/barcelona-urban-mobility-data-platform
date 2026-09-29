# Fabric / PySpark Notebooks

The Bronze ingestion is already handled by Fabric Data Factory, so I am using notebooks primarily for transformation, quality and curated-layer logic.

## Notebook plan

1. `01_bronze_to_silver`
   - read `district_data.json`
   - inspect the nested CKAN payload
   - extract `result.records`
   - normalize schema and column names
   - cast data types
   - handle nulls and duplicates
   - write the first Silver Delta table

2. `02_data_quality`
   - reusable validation checks
   - invalid-record analysis
   - row-count and schema assertions

3. `03_silver_enrichment`
   - joins between mobility and contextual/geographic datasets
   - window functions and derived attributes

4. `04_gold_model`
   - business-ready aggregations
   - dimensions and facts

5. `05_incremental_load`
   - watermark/incremental patterns
   - Delta MERGE/upsert logic

I will export the actual Fabric notebooks here as each implementation milestone is completed.
