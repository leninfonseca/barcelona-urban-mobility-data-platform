# Data Quality

I separate critical rules from non-critical source warnings.

## Critical Bicing checks
- non-empty incremental batch
- unique `station_id + snapshot_ingested_at`
- non-null station/timestamp/coordinate fields
- non-null availability fields
- non-negative availability values
- valid latitude/longitude ranges

## Non-critical warning

```text
free_bikes = ebikes + normal_bikes
```

This relationship is tracked through `bike_breakdown_valid` but does not stop processing.

## Historical / incremental validation

The notebook validates each incremental batch before MERGE and the historical table after MERGE.

It also verifies:
- final historical duplicates remain zero
- the watermark advances after new rows are inserted
- no-new-data exits successfully instead of failing

## Snapshot cardinality

Station count is not assumed constant across snapshots. One observed incremental snapshot contained 543 stations while previous snapshots contained 544.

Historical observations are preserved as received.

See [Troubleshooting](troubleshooting.md) for the timestamp parsing and original availability inconsistency cases.
