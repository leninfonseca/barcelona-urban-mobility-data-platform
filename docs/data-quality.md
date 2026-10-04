# Data Quality

I separate critical rules from non-critical source warnings.

## Silver Bicing checks

Critical checks include:

- non-empty incremental batch
- unique `station_id + snapshot_ingested_at`
- non-null station, timestamp and coordinate fields
- non-null availability fields
- non-negative availability values
- valid latitude/longitude ranges

## Non-critical source warning

```text
free_bikes = ebikes + normal_bikes
```

This relationship is tracked through `bike_breakdown_valid` but does not stop processing.

The source observation is preserved instead of silently correcting it.

## Historical / incremental validation

The historical notebook validates each incremental batch before MERGE and the resulting historical table after MERGE.

It also verifies:

- final historical duplicates remain zero
- the watermark advances after new rows are inserted
- no-new-data exits successfully instead of failing
- reprocessing the same historical key does not create duplicate rows

## Gold quality checks

`nb_gold_bicing_analytics` validates the analytical model before persisting it.

### Row reconciliation

```text
Silver historical row count = Gold fact row count
```

This protects against accidentally dropping or multiplying station observations during the Silver → Gold transformation.

### Fact grain uniqueness

The Gold fact must remain unique by:

```text
station_key + snapshot_ingested_at
```

### Station key uniqueness

Every row in `gold_dim_station` must have a unique `station_key`.

### Foreign-key completeness

The fact rejects NULL values in:

- `station_key`
- `date_key`
- `time_key`

### Referential integrity

Left anti joins are used to detect fact keys that do not exist in their dimensions.

Validated relationships:

- fact `station_key` → `gold_dim_station`
- fact `date_key` → `gold_dim_date`
- fact `time_key` → `gold_dim_time`

All orphan-key counts must be zero.

### KPI validity

Non-null percentage KPIs must remain within the range 0–100:

- `bike_availability_pct`
- `dock_availability_pct`
- `ebike_share_pct`

KPI values intentionally remain NULL when their denominator is zero.

## Analytical validation

After Gold is persisted, the notebook reads the Delta tables again and joins the fact to all three dimensions.

It compares the fact row count with the joined analytical row count and runs sample aggregations by day period and station to verify that the dimensional model is usable for analytics.

## Snapshot cardinality

Station count is not assumed constant across snapshots. Historical observations are preserved as received even when a station is absent from a later snapshot.

See [Troubleshooting](troubleshooting.md) for the timestamp parsing and original availability inconsistency cases.
