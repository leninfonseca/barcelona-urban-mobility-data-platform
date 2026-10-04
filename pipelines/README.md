# Fabric Pipelines

## pl_ingest_bicing_bronze

The Bicing pipeline now orchestrates the complete Bronze → Silver → Gold engineering flow.

```text
cp_ingest_bicing_bronze
        │ Success
        ▼
Historical Silver notebook
        │ Success
        ▼
nb_gold_bicing_analytics
```

## Historical Bronze destination

Folder expression:

```text
@concat(
    'bronze/citybikes/bicing/history/year=',
    formatDateTime(utcNow(),'yyyy'),
    '/month=', formatDateTime(utcNow(),'MM'),
    '/day=', formatDateTime(utcNow(),'dd')
)
```

File expression:

```text
@concat('bicing_', formatDateTime(utcNow(),'yyyyMMdd_HHmmss'), '.json')
```

Each successful ingestion creates an immutable timestamped snapshot instead of overwriting a previous source file.

## Incremental Silver processing

The historical Silver notebook:

1. Reads the current watermark from `silver_bicing_station_history`.
2. Recursively lists Bronze history files.
3. Selects only snapshots newer than the watermark.
4. Exits successfully when there is no new data.
5. Applies PySpark transformations and data quality checks.
6. Performs an idempotent Delta MERGE.
7. Validates the resulting historical table and watermark advancement.

## Gold processing

After Silver succeeds, `nb_gold_bicing_analytics`:

1. Revalidates the Silver historical grain.
2. Builds `gold_dim_station`, `gold_dim_date` and `gold_dim_time`.
3. Builds `gold_fact_bicing_availability`.
4. Calculates analytical KPIs.
5. Validates row reconciliation and referential integrity.
6. Overwrites the Gold Delta tables with a consistent rebuild.
7. Re-reads the persisted model and validates analytical joins.

## Final validation

The complete pipeline has been executed successfully with all three stages completing correctly:

```text
Bronze Copy  ✅
Silver       ✅
Gold         ✅
```

Evidence:

```text
assets/images/22-end-to-end-bronze-silver-gold.png
```
