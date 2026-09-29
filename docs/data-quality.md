# Data Quality

I am introducing data-quality controls incrementally as each layer becomes operational.

## Bronze validation completed

For the first REST ingestion I validated:

- REST connection succeeds from Fabric
- CKAN response returns `success: true`
- expected schema metadata is present in `result.fields`
- source records are returned in the payload
- pipeline execution completes
- raw JSON is materialized in the expected OneLake path

## Silver checks planned

The first PySpark transformation will add automated checks for:

- required columns
- explicit data types
- null rates
- duplicate records
- valid district and neighborhood identifiers
- row counts before and after transformation
- malformed records
- ingestion timestamp and source lineage

## Gold checks planned

Analytical models will add:

- uniqueness of dimension keys
- referential integrity between facts and dimensions
- accepted value/domain checks
- KPI reconciliation
- freshness thresholds
