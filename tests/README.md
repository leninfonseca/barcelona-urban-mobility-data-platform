# Tests

I am keeping validation close to each transformation instead of adding placeholder tests before the corresponding data layer exists.

## Current validation

The Bronze milestone is validated through:

- REST source preview
- successful pipeline execution
- successful raw JSON creation in OneLake
- expected CKAN response structure

## Planned automated tests

As Silver and Gold become operational I will add:

- schema assertions
- required-column checks
- null thresholds
- duplicate detection
- accepted ranges/domains
- row-count reconciliation
- referential-integrity checks
- freshness checks
