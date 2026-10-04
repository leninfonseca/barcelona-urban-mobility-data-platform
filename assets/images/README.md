# Project images

## Bronze, Silver and troubleshooting

Images `01` through `12` document the initial Fabric Lakehouse, REST ingestion, Bronze/Silver transformations and the original Bicing quality/troubleshooting work.

## Historical / incremental Bicing evidence

- `13-bicing-bronze-history.png` — timestamped immutable Bronze snapshots partitioned by date
- `14-bicing-incremental-merge.png` — incremental Delta MERGE result
- `15-bicing-end-to-end-pipeline.png` — successful Copy → historical Silver notebook orchestration

## Gold analytical evidence

- `16-gold-star-schema-tables.png` — persisted Gold dimension and fact tables
- `17-gold-quality-checks.png` — row reconciliation, referential integrity and KPI validation
- `18-gold-analytical-validation.png` — analytical validation of the persisted star schema

## SQL analytical evidence

- `19-sql-analytics-endpoint.png` — Gold Delta tables exposed through the SQL Analytics Endpoint
- `20-sql-serving-query.png` — joined T-SQL serving query

## Power BI and final orchestration

- `21-powerbi-semantic-model.png` — Gold star-schema relationships in the Power BI semantic model
- `22-end-to-end-bronze-silver-gold.png` — successful final Bronze → Silver → Gold pipeline run
- `23-powerbi-network-overview.png` — final Bicing Network Overview dashboard

Interactive demo:

```text
assets/demos/project-barcelona.gif
```
