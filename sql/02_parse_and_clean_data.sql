CREATE OR REPLACE VIEW `de-zoomcamp-447504.tbikeshare.ridership_2023_cleaned` AS
SELECT
  SAFE_CAST(trip_id AS INT64) AS trip_id,
  SAFE_CAST(trip_duration AS INT64) AS trip_duration,
  SAFE_CAST(start_station_id AS INT64) AS start_station_id,
  PARSE_TIMESTAMP('%m/%d/%Y %H:%M', start_time) AS start_time,
  start_station_name,
  SAFE_CAST(end_station_id AS INT64) AS end_station_id,
  PARSE_TIMESTAMP('%m/%d/%Y %H:%M', end_time) AS end_time,
  end_station_name,
  SAFE_CAST(bike_id AS INT64) AS bike_id,
  user_type
FROM `de-zoomcamp-447504.tbikeshare.ridership_2023_ext`;
