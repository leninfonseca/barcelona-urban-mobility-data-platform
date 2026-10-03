# Data Model

## Bronze

Context:

```text
Files/bronze/opendata/district_data/district_data.json
```

Bicing history:

```text
Files/bronze/citybikes/bicing/history/year=YYYY/month=MM/day=DD/bicing_YYYYMMDD_HHMMSS.json
```

## Silver

### silver_district_context
Typed contextual observations.

### silver_bicing_station_status
Initial single-snapshot Bicing milestone.

### silver_bicing_station_history
Historical Bicing Delta table.

**Grain:** one station observation per ingestion snapshot.

**Key:** `station_id + snapshot_ingested_at`.

Important timestamps:
- `source_timestamp`
- `snapshot_ingested_at`
- `silver_processed_at`

The model does not assume a fixed station count. Observed snapshots have contained both 544 and 543 stations, and prior history is preserved when a station is absent from a later snapshot.

## Gold

Gold is the next milestone and will be designed from the validated historical grain.
