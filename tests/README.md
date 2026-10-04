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

After persistence, the notebook re-reads the Delta tables and validates dimensional joins and analytical aggregations.

## Power BI semantic model validation

The semantic model was checked with:

- `dim_station 1:* fact`
- `dim_date 1:* fact`
- `dim_time 1:* fact`
- single-direction filters from dimensions to fact
- DAX KPI cards responding to slicer filter context
- station slicer filtering cards, map, temporal chart and ranking
- date/day-period slicers propagating through the fact
- latitude/longitude station map rendering expected Barcelona locations

## End-to-end orchestration validation

The complete Fabric chain has been executed successfully:

```text
Bronze Copy  ✅
Silver       ✅
Gold         ✅
```

Evidence is stored in:

```text
assets/images/22-end-to-end-bronze-silver-gold.png
```
