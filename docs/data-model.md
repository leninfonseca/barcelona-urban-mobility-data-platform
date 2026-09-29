# Data Model

I am evolving the model layer by layer instead of defining the final schema before inspecting the real sources.

## Bronze

Current raw object:

```text
Files/bronze/opendata/district_data/district_data.json
```

The CKAN response contains this high-level structure:

```text
root
├── help
├── success
└── result
    ├── resource_id
    ├── fields
    ├── records
    └── ...
```

I keep this envelope intact in Bronze so source metadata and raw records remain reproducible.

## Silver

The next model will extract `result.records` and persist a typed Delta table. The first source already exposes contextual fields such as reference date, district code/name and neighborhood code/name.

The Silver layer will contain:

- explicit data types
- normalized column names
- null handling
- duplicate handling
- schema validation
- ingestion metadata

## Gold

I will build the Gold layer once mobility sources are incorporated and the common grain is clear. The target design will use dimensional modeling where it adds analytical value, with candidate entities such as date, location, transport/mobility source and mobility observations.
