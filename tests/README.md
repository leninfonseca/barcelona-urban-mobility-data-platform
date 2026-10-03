# Tests

Validation is executed close to each transformation.

## Context Silver
- non-empty output
- unique source identifiers
- critical null checks
- non-negative analytical values

## Bicing historical / incremental
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

The end-to-end Copy → Notebook pipeline has also been executed successfully.
