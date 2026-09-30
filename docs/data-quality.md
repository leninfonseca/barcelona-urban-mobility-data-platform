# Data Quality

I introduce data-quality controls incrementally as each layer becomes operational.

## Bronze validation

### Context source

I validated that:

- the REST connection succeeds from Fabric
- the CKAN response returns `success: true`
- schema metadata is present in `result.fields`
- source records are returned in the payload
- the pipeline execution completes successfully
- the raw JSON is materialized in the expected OneLake path

### Bicing source

I validated that:

- the CityBikes REST connection succeeds from Fabric
- the response identifies the `bicing` network
- `network.stations` is present in the payload
- station-level availability fields are returned
- the pipeline execution completes
- `bicing_snapshot.json` is readable from the Bronze destination

## Silver validation

The contextual PySpark transformation includes executable checks for:

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

The Bicing Silver transformation will add source-specific checks for station identifier completeness, coordinate validity, availability ranges and timestamp parsing.

## Planned controls

As additional sources and Gold models are added, I will extend validation with:

- schema contracts
- accepted value/domain checks
- malformed-record handling
- freshness thresholds
- referential integrity between facts and dimensions
- KPI reconciliation
