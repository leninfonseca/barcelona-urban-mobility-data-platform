# Tests

I keep validation close to each transformation so data-quality rules execute with the logic they protect.

## Bronze validation

The Bronze layer is validated through:

- source previews
- successful pipeline executions
- expected source structures
- successful raw JSON persistence in OneLake

## Context Silver validation

The contextual Silver notebook validates:

- non-empty output
- unique `source_id`
- non-null critical fields
- non-negative analytical values
- Bronze-to-Silver row reconciliation

## Bicing Silver validation

The Bicing notebook validates:

- non-empty output
- unique `station_id + source_timestamp`
- non-null identifiers, timestamps and coordinates
- non-null availability values
- non-negative availability values
- valid coordinate ranges

The bike-type breakdown consistency is intentionally a warning rather than a critical assertion. The result is preserved in `bike_breakdown_valid`.

Current validated output:

```text
Bicing Silver rows: 544
Critical checks: passed
Bike breakdown warnings: 1
```

## Planned validation

Historical and Gold processing will add:

- snapshot freshness checks
- duplicate ingestion protection
- schema contracts
- referential-integrity checks
- Gold KPI reconciliation
