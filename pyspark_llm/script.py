

def run_job(spark, final_output_table):
  
  # Read bookings from the last 30 days
  bookings_df = spark.sql("SELECT * FROM booking WHERE confirm_time >= date_sub(current_date(), 30)")

  bookings_city_df = spark.sql("""
    WITH bookings_30_days AS (
      SELECT
          booking_id,
          city_id,
          CASE
            WHEN status IN ('COMPLETED', 'DROPPING_OFF')
                THEN 'COMPLETED'
            WHEN status IN ('CANCELLED', 'CANCELLED_DRIVER', 'CANCELLED_OPERATOR', 'RETURNED')
                THEN status
            WHEN status = 'CANCELLED_USER'
                THEN 'CANCELLED_PASSENGER'
            ELSE 'UNALLOCATED'
            END AS status_simple,
          booking_broadcast_time,
          confirm_time,
          confirm_time - booking_broadcast_time AS time_to_confirm,
          commission_rate,
          earning_adjustment_commission_rate,
          earning_adjustment_commission_rate - commission_rate AS tip,
          tax,
          receipt_payment_type,
          confirm_time,    
          reward_id,
      FROM booking
    )
    SELECT
        booking_id,
        city_id,
        status_simple,
        booking_broadcast_time,
        confirm_time,
        time_to_confirm,
        commission_rate,
        earning_adjustment_commission_rate,
        tip,
        tax,
        receipt_payment_type,
        confirm_time,    
        reward_id,
        CASE WHEN status_simple = 'COMPLETED'
            THEN tax + tip
        ELSE 0
        END AS additional_fees,
        city_name,
        city.region AS city_region,
        city.territory AS city_territory,
        city.time_zone AS city_time_zone,
        city.enable_tip AS city_enable_tip,
        city.is_capital AS city_is_capital              
    FROM 
        bookings_30_days
    JOIN
        (SELECT 
            DISTINCT id, city_name, region, territory, time_zone, enable_tip, is_capital 
        FROM city) AS city
    ON
      city_id = city.id        
  """)
  bookings_city_df.createOrReplaceTempView("bookings_30_days_with_city_new")
  # Merge
  spark.sql(f"""
    MERGE INTO {final_output_table} b
    USING bookings_30_days_with_city_new t
    ON
    b.booking_id = t.booking_id
    WHEN MATCHED THEN
      UPDATE SET
        b.city_id = t.city_id,
        b.status_simple = t.status_simple,
        b.booking_broadcast_time = t.booking_broadcast_time,
        b.confirm_time = t.confirm_time,
        b.time_to_confirm = t.time_to_confirm,
        b.commission_rate = t.commission_rate,
        b.earning_adjustment_commission_rate = t.earning_adjustment_commission_rate,
        b.tip = t.tip,
        b.additional_fees = t.additional_fees,
        b.receipt_payment_type = t.receipt_payment_type,
        b.confirm_time = t.confirm_time,
        b.reward_id = t.reward_id,
        b.city_name = t.city_name,
        b.city_region = t.city_region,
        b.city_territory = t.city_territory,
        b.city_time_zone = t.city_time_zone,
        b.city_enable_tip = t.city_enable_tip,
        b.city_is_capital = t.city_is_capital
    WHEN NOT MATCHED THEN
      INSERT (
            booking_id, 
            city_id, 
            status_simple, 
            booking_broadcast_time, 
            confirm_time, 
            time_to_confirm, 
            commission_rate, 
            earning_adjustment_commission_rate, 
            tip, 
            additional_fees,
            receipt_payment_type, 
            confirm_time, 
            reward_id, 
            city_name, 
            city_region, 
            city_territory, 
            city_time_zone, 
            city_enable_tip, 
            city_is_capital
      )
      VALUES (
            t.booking_id, 
            t.city_id, 
            t.status_simple, 
            t.booking_broadcast_time,
            t.confirm_time, 
            t.time_to_confirm, 
            t.commission_rate, 
            t.earning_adjustment_commission_rate, 
            t.tip, 
            t.additional_fees,
            t.receipt_payment_type, 
            t.confirm_time, 
            t.reward_id, 
            t.city_name, 
            t.city_region, 
            t.city_territory, 
            t.city_time_zone, 
            t.city_enable_tip, 
            t.city_is_capital
      )
  """)

