# Fabric Pipelines

## pl_ingest_bicing_bronze

The Bicing pipeline orchestrates Bronze ingestion and incremental Silver processing.

```text
cp_ingest_bicing_bronze
        │ Success
        ▼
nb_process_bicing_history
```

### Historical Bronze destination

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

Each successful ingestion therefore creates an immutable timestamped snapshot instead of overwriting the previous source file.

## Incremental Silver processing

The notebook activity:

1. Reads the current watermark from `silver_bicing_station_history`.
2. Recursively lists Bronze history files.
3. Selects only snapshots newer than the watermark.
4. Exits successfully when there is no new data.
5. Applies PySpark transformations and data quality checks.
6. Performs an idempotent Delta MERGE.
7. Validates the resulting historical table and watermark advancement.

The end-to-end Copy → Notebook execution has been validated successfully.

## Gold downstream processing

`nb_gold_bicing_analytics` now builds the Gold star schema from `silver_bicing_station_history`.

At the current project stage, Gold is executed separately and is **not yet part of `pl_ingest_bicing_bronze`**. This keeps the documented orchestration aligned with what has actually been implemented.

A future orchestration step can attach Gold processing after successful Silver completion once the SQL/BI serving flow is finalized.
