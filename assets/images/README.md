# Project images

## Bronze, Silver and troubleshooting

Images `01` through `12` document the initial Fabric Lakehouse, REST ingestion, Bronze/Silver transformations and the original Bicing quality/troubleshooting work.

## Historical / incremental Bicing evidence

- `13-bicing-bronze-history.png` — timestamped immutable Bronze snapshots partitioned by date
- `14-bicing-incremental-merge.png` — incremental Delta MERGE result
- `15-bicing-end-to-end-pipeline.png` — successful Copy → historical notebook orchestration

## Gold analytical evidence

- `16-gold-star-schema-tables.png` — persisted Gold dimension and fact tables in the Lakehouse
- `17-gold-quality-checks.png` — Gold row reconciliation, referential-integrity and KPI validation
- `18-gold-analytical-validation.png` — analytical validation against the persisted Gold star schema

## Planned final evidence

- architecture overview
- SQL Analytics Endpoint queries
- Power BI analytical dashboard
