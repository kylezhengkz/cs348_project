WITH durations AS (
  SELECT 
    "userID",
    EXTRACT(EPOCH FROM ("bookEndDateTime" - "bookStartDateTime")) / 60 AS duration_mins
  FROM "Booking"
  WHERE "userID" = %(user_id)s
),

hour_buckets AS (
  SELECT 
    DATE_TRUNC('hour', "bookStartDateTime") AS hour_slot,
    COUNT(*) AS count
  FROM "Booking"
  WHERE "userID" = %(user_id)s
  GROUP BY hour_slot
),

top_hour AS (
  SELECT hour_slot
  FROM hour_buckets
  ORDER BY count DESC
  LIMIT 1
),

agg_duration AS (
  SELECT ROUND(AVG(duration_mins)) AS avg_duration_mins FROM durations
)

SELECT 
  agg_duration.avg_duration_mins,
  TO_CHAR(top_hour.hour_slot, 'HH24:MI') AS most_booked_hour
FROM agg_duration, top_hour;
