# Tests

I keep validation close to each transformation so data-quality rules execute with the pipeline logic they protect.

## Bronze validation

The Bronze milestone is validated through:

- REST source preview
- successful pipeline execution
- successful raw JSON creation in OneLake
- expected CKAN response structure

## Silver validation

The first Silver notebook contains executable assertions for the current source:

- output must not be empty
- `source_id` must remain unique
- critical columns must not contain nulls
- `value` must not contain negative values
- Bronze and Silver row counts are reconciled

Current run:

```text
Bronze records: 100
Silver records: 100
All Silver data quality checks passed.
```

These checks run before the curated Delta table is considered valid.

## Planned tests

As the platform grows I will add:

- schema contracts
- accepted ranges and domains
- malformed-record quarantine
- freshness checks
- referential-integrity checks
- Gold KPI reconciliation
