from pyspark.sql import functions as F

from helpers import get_cities_by_region

def run_job(spark, final_output_table):
  
  # Filter to cities in the Pacific Northwest
  pnw_cities_df = get_cities_by_region(spark, "PNW")
  
  # Read bookings from the last 30 days
  bookings_df = spark.sql("SELECT * FROM booking WHERE confirm_time >= date_sub(current_date(), 30)")

  # Join the bookings with the cities
  pnw_cities_df.createOrReplaceTempView("pnw_cities")
  bookings_df.createOrReplaceTempView("bookings_30_days")
  joined_df = spark.sql("""
    SELECT
      timestamp(date_trunc(b.confirm_time, 'DD')) AS "booking_date",
      b.earning_adjustment_commission_rate AS "commission_rate",
      b.receipt_payment_type AS "payment_type",
      b.reward_id AS "reward_id",
      c.*,
    FROM
      bookings_30_days b
      JOIN pnw_cities c
      ON b.city_id = c.city_id
  """)

  # Write the joined data to the final output table
  joined_df.write.mode("overwrite").saveAsTable(final_output_table)

  joined_df.createOrReplaceTempView("joined_temp")
  commission_rate_metrics_df = spark.sql("""
    SELECT 
      booking_date,
      avg(commission_rate) AS "avg_commission_rate",
      max(commission_rate) AS "max_commission_rate",
      min(commission_rate) AS "min_commission_rate"
    FROM
      joined_temp
  """)

  # Merge into existing metrics table
  commission_rate_metrics_df.createOrReplaceTempView("commission_rate_metrics_temp")
  spark.sql(f"""
    MERGE INTO commission_rate_metrics m
    USING commission_rate_metrics_temp t
    ON m.booking_date = t.booking_date
    WHEN MATCHED THEN
      UPDATE SET
        m.avg_commission_rate = t.avg_commission_rate,
        m.max_commission_rate = t.max_commission_rate,
        m.min_commission_rate = t.min_commission_rate
    WHEN NOT MATCHED THEN
      INSERT (booking_date, avg_commission_rate, max_commission_rate, min_commission_rate)
      VALUES (t.booking_date, t.avg_commission_rate, t.max_commission_rate, t.min_commission_rate)
  """)
