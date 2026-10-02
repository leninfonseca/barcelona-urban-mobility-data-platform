from pyspark.sql.functions import (
    col,
    current_timestamp,
    explode,
    regexp_replace,
    to_timestamp,
    trim,
)

BRONZE_PATH = "Files/bronze/citybikes/bicing/bicing_snapshot.json"
SILVER_TABLE = "silver_bicing_station_status"

raw_bicing_df = (
    spark.read
    .option("multiline", "true")
    .json(BRONZE_PATH)
)

stations_df = (
    raw_bicing_df
    .select(explode(col("network.stations")).alias("station"))
)

bicing_df = stations_df.select("station.*")

silver_bicing_df = (
    bicing_df
    .select(
        col("id").alias("station_id"),
        col("extra.uid").cast("long").alias("station_uid"),
        trim(col("name")).alias("station_name"),
        col("latitude").cast("double").alias("latitude"),
        col("longitude").cast("double").alias("longitude"),
        to_timestamp(
            regexp_replace(col("timestamp"), "Z$", ""),
            "yyyy-MM-dd'T'HH:mm:ss.SSSSSSXXX",
        ).alias("source_timestamp"),
        col("free_bikes").cast("long").alias("free_bikes"),
        col("empty_slots").cast("long").alias("empty_slots"),
        col("extra.ebikes").cast("long").alias("ebikes"),
        col("extra.normal_bikes").cast("long").alias("normal_bikes"),
        col("extra.has_ebikes").cast("boolean").alias("has_ebikes"),
        col("extra.online").cast("boolean").alias("is_online"),
    )
    .withColumn(
        "station_capacity",
        col("free_bikes") + col("empty_slots"),
    )
    .withColumn(
        "bike_breakdown_valid",
        col("free_bikes") == (col("ebikes") + col("normal_bikes")),
    )
    .withColumn("silver_processed_at", current_timestamp())
    .dropDuplicates(["station_id", "source_timestamp"])
)

total_rows = silver_bicing_df.count()

duplicate_station_snapshots = (
    silver_bicing_df
    .groupBy("station_id", "source_timestamp")
    .count()
    .filter(col("count") > 1)
    .count()
)

null_critical = silver_bicing_df.filter(
    col("station_id").isNull()
    | col("source_timestamp").isNull()
    | col("latitude").isNull()
    | col("longitude").isNull()
).count()

null_availability = silver_bicing_df.filter(
    col("free_bikes").isNull()
    | col("empty_slots").isNull()
    | col("ebikes").isNull()
    | col("normal_bikes").isNull()
).count()

invalid_availability = silver_bicing_df.filter(
    (col("free_bikes") < 0)
    | (col("empty_slots") < 0)
    | (col("ebikes") < 0)
    | (col("normal_bikes") < 0)
).count()

invalid_coordinates = silver_bicing_df.filter(
    (col("latitude") < -90)
    | (col("latitude") > 90)
    | (col("longitude") < -180)
    | (col("longitude") > 180)
).count()

bike_breakdown_mismatch = silver_bicing_df.filter(
    col("free_bikes") != (col("ebikes") + col("normal_bikes"))
).count()

assert total_rows > 0, "Bicing Silver table is empty"
assert duplicate_station_snapshots == 0, "Duplicate station snapshots detected"
assert null_critical == 0, "Null values detected in critical station fields"
assert null_availability == 0, "Null values detected in availability fields"
assert invalid_availability == 0, "Negative availability values detected"
assert invalid_coordinates == 0, "Invalid station coordinates detected"

if bike_breakdown_mismatch > 0:
    print(
        f"WARNING: {bike_breakdown_mismatch} station records "
        "have an inconsistent bike breakdown."
    )

print("All critical Bicing Silver data quality checks passed.")

(
    silver_bicing_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(SILVER_TABLE)
)

validated_bicing_df = spark.table(SILVER_TABLE)

print(f"Rows in Bicing Silver Delta table: {validated_bicing_df.count()}")

validated_bicing_df.printSchema()
display(validated_bicing_df)
