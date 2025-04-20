CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-447504.tbikeshare.ridership_2023_ext`
(
  trip_id STRING,
  trip_duration STRING,
  start_station_id STRING,
  start_time STRING,
  start_station_name STRING,
  end_station_id STRING,
  end_time STRING,
  end_station_name STRING,
  bike_id STRING,
  user_type STRING
)
OPTIONS (
  format = 'CSV',
  uris = ['gs://tbikeshare/ridershipdata_2023/*.csv'],
  skip_leading_rows = 1
);