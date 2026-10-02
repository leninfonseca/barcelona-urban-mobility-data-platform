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
- `network.stations` is present
- station-level availability fields are returned
- the pipeline execution completes
- `bicing_snapshot.json` is readable from Bronze

## Context Silver validation

The contextual transformation validates:

- non-empty output
- row-count reconciliation
- duplicate `source_id` values
- critical nulls
- negative analytical values

Validated result:

```text
Bronze records: 100
Silver records: 100
Duplicate source_id values: 0
Rows with nulls in critical columns: 0
Rows with negative values: 0
All Silver data quality checks passed.
```

## Bicing Silver validation

The Bicing transformation validates:

- non-empty output
- uniqueness of `station_id + source_timestamp`
- non-null station ID, timestamp and coordinates
- non-null availability values
- non-negative bike and slot counts
- valid latitude and longitude ranges
- consistency of the bike-type breakdown as a non-critical quality signal

Validated result:

```text
Total rows: 544
Duplicate station snapshots: 0
Rows with critical nulls: 0
Rows with invalid availability: 0
Rows with invalid coordinates: 0
Rows with inconsistent bike breakdown: 1
```

The bike-breakdown inconsistency is preserved through `bike_breakdown_valid` and reported as a warning. It does not stop the transformation because the source contract does not establish the relationship as a guaranteed invariant.

Critical checks still fail the notebook through assertions.

## Troubleshooting

The timestamp parsing failure and bike-breakdown anomaly are documented in [Troubleshooting](troubleshooting.md).

## Planned controls

The historical and Gold layers will add:

- freshness thresholds
- historical snapshot completeness
- schema contracts
- accepted value/domain checks
- referential integrity
- KPI reconciliation
