#!/usr/bin/env python
# coding: utf-8

# ## nb_gold_bicing_analytics
# 
# null

# In[2]:


from pyspark.sql.functions import (
    col,
    count,
    countDistinct,
    max as spark_max,
    min as spark_min,
    row_number,
    xxhash64
)

from pyspark.sql.window import Window


SILVER_HISTORY_TABLE = "silver_bicing_station_history"

GOLD_DIM_STATION = "gold_dim_station"
GOLD_DIM_DATE = "gold_dim_date"
GOLD_DIM_TIME = "gold_dim_time"
GOLD_FACT_AVAILABILITY = "gold_fact_bicing_availability"


silver_history_df = spark.table(
    SILVER_HISTORY_TABLE
)

print(
    f"Silver historical rows: "
    f"{silver_history_df.count()}"
)

silver_history_df.printSchema()


# In[3]:


# Validate Silver grain before building Gold

silver_rows = silver_history_df.count()

silver_unique_grain = (
    silver_history_df
    .select(
        "station_id",
        "snapshot_ingested_at"
    )
    .distinct()
    .count()
)

silver_duplicate_grain = (
    silver_rows - silver_unique_grain
)

print(f"Silver rows: {silver_rows}")
print(f"Unique historical observations: {silver_unique_grain}")
print(f"Duplicate historical observations: {silver_duplicate_grain}")

assert silver_duplicate_grain == 0, \
    "Silver historical grain is not unique"


# In[4]:


station_window = (
    Window
    .partitionBy("station_id")
    .orderBy(
        col("snapshot_ingested_at").desc()
    )
)

gold_dim_station_df = (
    silver_history_df
    .withColumn(
        "station_row_number",
        row_number().over(station_window)
    )
    .filter(
        col("station_row_number") == 1
    )
    .select(
        xxhash64(
            col("station_id")
        ).alias("station_key"),

        col("station_id"),
        col("station_uid"),
        col("station_name"),
        col("latitude"),
        col("longitude"),
        col("has_ebikes")
    )
)

print(
    f"Gold station dimension rows: "
    f"{gold_dim_station_df.count()}"
)

display(gold_dim_station_df)


# In[5]:


from pyspark.sql.functions import (
    date_format,
    dayofmonth,
    dayofweek,
    explode,
    expr,
    lit,
    month,
    quarter,
    sequence,
    to_date,
    weekofyear,
    when,
    year
)

date_bounds = (
    silver_history_df
    .select(
        spark_min(
            to_date(col("snapshot_ingested_at"))
        ).alias("min_date"),

        spark_max(
            to_date(col("snapshot_ingested_at"))
        ).alias("max_date")
    )
    .first()
)

min_date = date_bounds["min_date"]
max_date = date_bounds["max_date"]

print(f"Minimum historical date: {min_date}")
print(f"Maximum historical date: {max_date}")


gold_dim_date_df = (
    spark.range(1)
    .select(
        explode(
            sequence(
                lit(min_date),
                lit(max_date),
                expr("INTERVAL 1 DAY")
            )
        ).alias("full_date")
    )
    .select(
        date_format(
            col("full_date"),
            "yyyyMMdd"
        ).cast("int").alias("date_key"),

        col("full_date"),

        year(col("full_date")).alias("year"),

        quarter(
            col("full_date")
        ).alias("quarter"),

        month(
            col("full_date")
        ).alias("month"),

        date_format(
            col("full_date"),
            "MMMM"
        ).alias("month_name"),

        dayofmonth(
            col("full_date")
        ).alias("day"),

        weekofyear(
            col("full_date")
        ).alias("week_of_year"),

        when(
            dayofweek(col("full_date")) == 1,
            7
        )
        .otherwise(
            dayofweek(col("full_date")) - 1
        )
        .alias("day_of_week"),

        date_format(
            col("full_date"),
            "EEEE"
        ).alias("day_name"),

        when(
            dayofweek(col("full_date")).isin(1, 7),
            True
        )
        .otherwise(False)
        .alias("is_weekend")
    )
)

display(gold_dim_date_df)


# In[6]:


from pyspark.sql.functions import (
    hour,
    minute,
    lpad,
    concat,
    when
)

gold_dim_time_df = (
    silver_history_df
    .select(
        hour(
            col("snapshot_ingested_at")
        ).alias("hour"),

        minute(
            col("snapshot_ingested_at")
        ).alias("minute")
    )
    .distinct()
    .withColumn(
        "time_key",
        (
            col("hour") * 100
            + col("minute")
        ).cast("int")
    )
    .withColumn(
        "time_label",
        concat(
            lpad(
                col("hour").cast("string"),
                2,
                "0"
            ),
            lit(":"),
            lpad(
                col("minute").cast("string"),
                2,
                "0"
            )
        )
    )
    .withColumn(
        "day_period",
        when(
            col("hour") < 6,
            "Night"
        )
        .when(
            col("hour") < 12,
            "Morning"
        )
        .when(
            col("hour") < 18,
            "Afternoon"
        )
        .otherwise(
            "Evening"
        )
    )
    .select(
        "time_key",
        "hour",
        "minute",
        "time_label",
        "day_period"
    )
    .orderBy(
        "time_key"
    )
)

display(gold_dim_time_df)


# In[7]:


from pyspark.sql.functions import round as spark_round

gold_fact_bicing_availability_df = (
    silver_history_df
    .join(
        gold_dim_station_df.select(
            "station_key",
            "station_id"
        ),
        on="station_id",
        how="inner"
    )
    .select(
        col("station_key"),

        date_format(
            col("snapshot_ingested_at"),
            "yyyyMMdd"
        ).cast("int").alias("date_key"),

        (
            hour(col("snapshot_ingested_at")) * 100
            + minute(col("snapshot_ingested_at"))
        ).cast("int").alias("time_key"),

        col("snapshot_ingested_at"),
        col("source_timestamp"),

        col("free_bikes"),
        col("empty_slots"),
        col("ebikes"),
        col("normal_bikes"),
        col("station_capacity"),

        col("is_online"),
        col("bike_breakdown_valid")
    )
    .withColumn(
        "bike_availability_pct",
        when(
            col("station_capacity") > 0,
            spark_round(
                col("free_bikes")
                / col("station_capacity")
                * 100,
                2
            )
        )
    )
    .withColumn(
        "dock_availability_pct",
        when(
            col("station_capacity") > 0,
            spark_round(
                col("empty_slots")
                / col("station_capacity")
                * 100,
                2
            )
        )
    )
    .withColumn(
        "ebike_share_pct",
        when(
            col("free_bikes") > 0,
            spark_round(
                col("ebikes")
                / col("free_bikes")
                * 100,
                2
            )
        )
    )
)

print(
    f"Gold fact rows: "
    f"{gold_fact_bicing_availability_df.count()}"
)

display(gold_fact_bicing_availability_df)


# In[8]:


# Gold model quality checks

silver_rows = silver_history_df.count()
fact_rows = gold_fact_bicing_availability_df.count()

# 1. Row reconciliation
assert fact_rows == silver_rows, \
    f"Row mismatch: Silver={silver_rows}, Gold fact={fact_rows}"


# 2. Fact grain must remain unique
fact_unique_grain = (
    gold_fact_bicing_availability_df
    .select(
        "station_key",
        "snapshot_ingested_at"
    )
    .distinct()
    .count()
)

fact_duplicate_grain = fact_rows - fact_unique_grain

assert fact_duplicate_grain == 0, \
    f"Duplicate fact observations found: {fact_duplicate_grain}"


# 3. Dimension surrogate key must be unique
station_rows = gold_dim_station_df.count()

station_unique_keys = (
    gold_dim_station_df
    .select("station_key")
    .distinct()
    .count()
)

assert station_rows == station_unique_keys, \
    "Duplicate station_key values found in gold_dim_station"


# 4. Critical foreign keys cannot be NULL
null_foreign_keys = (
    gold_fact_bicing_availability_df
    .filter(
        col("station_key").isNull()
        | col("date_key").isNull()
        | col("time_key").isNull()
    )
    .count()
)

assert null_foreign_keys == 0, \
    f"NULL foreign keys found: {null_foreign_keys}"


# 5. Referential integrity: station
orphan_station_keys = (
    gold_fact_bicing_availability_df
    .select("station_key")
    .distinct()
    .join(
        gold_dim_station_df.select("station_key"),
        on="station_key",
        how="left_anti"
    )
    .count()
)

assert orphan_station_keys == 0, \
    f"Fact contains {orphan_station_keys} unknown station keys"


# 6. Referential integrity: date
orphan_date_keys = (
    gold_fact_bicing_availability_df
    .select("date_key")
    .distinct()
    .join(
        gold_dim_date_df.select("date_key"),
        on="date_key",
        how="left_anti"
    )
    .count()
)

assert orphan_date_keys == 0, \
    f"Fact contains {orphan_date_keys} unknown date keys"


# 7. Referential integrity: time
orphan_time_keys = (
    gold_fact_bicing_availability_df
    .select("time_key")
    .distinct()
    .join(
        gold_dim_time_df.select("time_key"),
        on="time_key",
        how="left_anti"
    )
    .count()
)

assert orphan_time_keys == 0, \
    f"Fact contains {orphan_time_keys} unknown time keys"


# 8. KPI validity
invalid_kpis = (
    gold_fact_bicing_availability_df
    .filter(
        ((col("bike_availability_pct") < 0)
         | (col("bike_availability_pct") > 100))
        |
        ((col("dock_availability_pct") < 0)
         | (col("dock_availability_pct") > 100))
        |
        ((col("ebike_share_pct") < 0)
         | (col("ebike_share_pct") > 100))
    )
    .count()
)

assert invalid_kpis == 0, \
    f"Invalid percentage KPI values found: {invalid_kpis}"


print("Gold quality checks passed")
print(f"Silver rows: {silver_rows}")
print(f"Gold fact rows: {fact_rows}")
print(f"Duplicate fact observations: {fact_duplicate_grain}")
print(f"NULL foreign keys: {null_foreign_keys}")
print(f"Orphan station keys: {orphan_station_keys}")
print(f"Orphan date keys: {orphan_date_keys}")
print(f"Orphan time keys: {orphan_time_keys}")
print(f"Invalid KPI values: {invalid_kpis}")


# In[9]:


# Persist Gold star schema as Delta tables

(
    gold_dim_station_df
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(GOLD_DIM_STATION)
)

(
    gold_dim_date_df
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(GOLD_DIM_DATE)
)

(
    gold_dim_time_df
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(GOLD_DIM_TIME)
)

(
    gold_fact_bicing_availability_df
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(GOLD_FACT_AVAILABILITY)
)

print("Gold Delta tables written successfully.")

gold_tables = [
    GOLD_DIM_STATION,
    GOLD_DIM_DATE,
    GOLD_DIM_TIME,
    GOLD_FACT_AVAILABILITY
]

for table_name in gold_tables:
    rows = spark.table(table_name).count()

    print(
        f"{table_name}: "
        f"{rows} rows"
    )


# In[10]:


from pyspark.sql.functions import (
    avg,
    count as spark_count
)

# Read persisted Gold tables

gold_fact_df = spark.table(
    GOLD_FACT_AVAILABILITY
)

gold_station_df = spark.table(
    GOLD_DIM_STATION
)

gold_date_df = spark.table(
    GOLD_DIM_DATE
)

gold_time_df = spark.table(
    GOLD_DIM_TIME
)


# Join fact with dimensions

gold_analytics_df = (
    gold_fact_df
    .join(
        gold_station_df,
        on="station_key",
        how="left"
    )
    .join(
        gold_date_df,
        on="date_key",
        how="left"
    )
    .join(
        gold_time_df,
        on="time_key",
        how="left"
    )
)

print(
    f"Fact rows: "
    f"{gold_fact_df.count()}"
)

print(
    f"Joined analytical rows: "
    f"{gold_analytics_df.count()}"
)

display(
    gold_analytics_df.select(
        "station_name",
        "full_date",
        "time_label",
        "day_period",
        "free_bikes",
        "empty_slots",
        "station_capacity",
        "bike_availability_pct",
        "dock_availability_pct",
        "ebike_share_pct",
        "is_online"
    )
)


# In[11]:


availability_by_period_df = (
    gold_analytics_df
    .groupBy(
        "day_period"
    )
    .agg(
        spark_count("*").alias(
            "observations"
        ),

        avg(
            "free_bikes"
        ).alias(
            "avg_free_bikes"
        ),

        avg(
            "bike_availability_pct"
        ).alias(
            "avg_bike_availability_pct"
        ),

        avg(
            "dock_availability_pct"
        ).alias(
            "avg_dock_availability_pct"
        )
    )
    .orderBy(
        "day_period"
    )
)

display(availability_by_period_df)


# In[12]:


station_availability_df = (
    gold_analytics_df
    .filter(
        col("is_online") == True
    )
    .groupBy(
        "station_key",
        "station_name"
    )
    .agg(
        spark_count("*").alias(
            "observations"
        ),

        avg(
            "bike_availability_pct"
        ).alias(
            "avg_bike_availability_pct"
        )
    )
    .orderBy(
        col(
            "avg_bike_availability_pct"
        ).asc()
    )
)

display(
    station_availability_df.limit(20)
)


# In[13]:


# Final Gold validation and summary

final_fact_df = spark.table(
    GOLD_FACT_AVAILABILITY
)

total_fact_rows = final_fact_df.count()

distinct_stations = (
    final_fact_df
    .select("station_key")
    .distinct()
    .count()
)

distinct_snapshots = (
    final_fact_df
    .select("snapshot_ingested_at")
    .distinct()
    .count()
)

snapshot_bounds = (
    final_fact_df
    .agg(
        spark_min(
            "snapshot_ingested_at"
        ).alias("first_snapshot"),

        spark_max(
            "snapshot_ingested_at"
        ).alias("last_snapshot")
    )
    .first()
)

print("Gold layer validation completed")
print("--------------------------------")
print(f"Fact rows: {total_fact_rows}")
print(f"Distinct stations: {distinct_stations}")
print(f"Distinct snapshots: {distinct_snapshots}")
print(
    f"Historical range: "
    f"{snapshot_bounds['first_snapshot']} "
    f"→ {snapshot_bounds['last_snapshot']}"
)

print()
print("Gold tables:")
print(f"- {GOLD_DIM_STATION}")
print(f"- {GOLD_DIM_DATE}")
print(f"- {GOLD_DIM_TIME}")
print(f"- {GOLD_FACT_AVAILABILITY}")

