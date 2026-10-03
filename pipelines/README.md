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

The notebook activity obtains the Silver watermark, selects only newer Bronze snapshots, exits successfully when nothing is new, applies quality checks, performs Delta MERGE and validates the updated watermark.

The end-to-end Copy → Notebook execution has been validated successfully.
