CREATE OR REPLACE TABLE `de-zoomcamp-447504.tbikeshare.ridership_2023_partitioned_clustered`
PARTITION BY DATE(start_time)
CLUSTER BY user_type, start_station_id
AS
SELECT * FROM `de-zoomcamp-447504.tbikeshare.ridership_2023_cleaned`;