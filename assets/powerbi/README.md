# Power BI

## Report artifact

```text
Bicing Network Overview.pbix
```

The PBIX is a **live-connected** report artifact backed by the Microsoft Fabric semantic model.

It preserves the report definition and layout, but it does not embed the Direct Lake data inside the file.

## Semantic model

The report uses the Gold star schema directly:

```text
gold_dim_station  1 ─── * gold_fact_bicing_availability
gold_dim_date     1 ─── * gold_fact_bicing_availability
gold_dim_time     1 ─── * gold_fact_bicing_availability
```

Cross-filter direction is single from dimensions to fact.

## DAX measures

The report includes:

- `Total Observations`
- `Bike Availability %`
- `Dock Availability %`
- `E-bike Share %`
- `Online Observations`
- `Online Observation %`

The percentage measures use ratios of sums so network-level values are weighted by the relevant base quantities.

## Report page

The final Network Overview page includes:

- KPI cards
- date slicer
- day-period slicer
- searchable station slicer
- Azure Maps station view
- network availability over time
- low-availability station ranking

## Permanent portfolio evidence

The PBIX depends on the Fabric semantic model for data access.

Permanent visual evidence is therefore also stored as:

```text
assets/demos/project-barcelona.gif
assets/images/21-powerbi-semantic-model.png
assets/images/23-powerbi-network-overview.png
```
