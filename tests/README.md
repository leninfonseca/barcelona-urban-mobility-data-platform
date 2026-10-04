# Tests

Validation is executed close to each transformation instead of being deferred to the end of the pipeline.

## Context Silver

- non-empty output
- unique source identifiers
- critical null checks
- non-negative analytical values

## Bicing historical / incremental Silver

- incremental batch is non-empty when processing continues
- unique `station_id + snapshot_ingested_at`
- critical fields are non-null
- availability values are non-negative
- coordinates are valid
- bike-breakdown inconsistencies are warnings, not hard failures
- Delta MERGE is idempotent
- final historical duplicates remain zero
- watermark advances after successful insertion
- no-new-data exits successfully

The end-to-end Copy → Notebook pipeline has also been executed successfully.

## Gold star schema

Before persistence, `nb_gold_bicing_analytics` validates:

- Silver row count equals Gold fact row count
- unique `station_key + snapshot_ingested_at` fact grain
- unique `station_key` values in `gold_dim_station`
- non-null `station_key`, `date_key` and `time_key`
- zero orphan station foreign keys
- zero orphan date foreign keys
- zero orphan time foreign keys
- percentage KPIs remain between 0 and 100 when non-null

After persistence, the notebook reads the Delta tables again and performs analytical joins and sample aggregations to validate that the star schema is consumable for downstream SQL and BI workloads.
