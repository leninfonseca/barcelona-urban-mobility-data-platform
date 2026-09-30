# Data Quality

I am introducing data-quality controls incrementally as each layer becomes operational.

## Bronze validation

The first REST ingestion validates that:

- the REST connection succeeds from Fabric
- the CKAN response returns `success: true`
- schema metadata is present in `result.fields`
- source records are returned in the payload
- the pipeline execution completes successfully
- the raw JSON is materialized in the expected OneLake path

## Silver validation

The first PySpark transformation includes executable checks for:

- non-empty output
- row-count reconciliation between Bronze records and Silver
- duplicate detection using `source_id`
- null detection in critical fields
- invalid negative values in the analytical `value` column
- explicit type casting
- processing metadata through `silver_processed_at`

Current validated result:

```text
Bronze records: 100
Silver records: 100
Duplicate source_id values: 0
Rows with nulls in critical columns: 0
Rows with negative values: 0
All Silver data quality checks passed.
```

Assertions stop notebook execution when these core rules fail instead of allowing bad data to be silently persisted.

## Planned controls

As additional sources and Gold models are added, I will extend validation with:

- required-column and schema contracts
- accepted value/domain checks
- malformed-record handling
- freshness thresholds
- referential integrity between facts and dimensions
- KPI reconciliation
