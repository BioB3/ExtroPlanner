# Overview

The database schema consists of 3 tables
- Data integration table (Weather_cleaned): Contains aggregated records from the Sensor and API tables in a 30 minute frequency.
- API table (weather_api): Contains weather data fetched from [Open Weather API](https://openweathermap.org/current) current weather data API.
- Sensor table (weather_sensor): Contains weather data read from data acquisition devices.

You can change the names of these tables but you will have to update cleaned_table and sensor_table definitions in `app.py` and `predictor.py`

# Schema
The schema for each table are as follows

## weather_cleaned
- `weather_cleaned`
  - `id`: `INT`
  - `ts` : `TIMESTAMP`
  - `location` : `VARCHAR(255)`
  - `wind_sp` : `FLOAT`
  - `wind_deg` : `INT`
  - `pressure` : `FLOAT`
  - `temperature` : `FLOAT`
  - `humidity` : `FLOAT`
  - `cloud_per` : `FLOAT`
  - `rain_amt` : `FLOAT`
  - `weather` : `VARCHAR(255)`

## weather_api
- `weather_api`
  - `id` : `INT`
  - `ts` : `TIMESTAMP`
  - `latitude` : `FLOAT`
  - `longitude` : `FLOAT`
  - `wind_sp` : `FLOAT`
  - `wind_deg` : `INT`
  - `pressure` : `FLOAT`
  - `temperature` : `FLOAT`
  - `humidity` : `FLOAT`
  - `cloud_per` : `FLOAT`
  - `rain_amt` : `FLOAT`
  - `weather` : `VARCHAR(50)`

## weather_sensor
- `weather_sensor`
  - `id` : `INT`
  - `ts` : `TIMESTAMP`
  - `latitude` : `FLOAT`
  - `longitude` : `FLOAT`
  - `temperature` : `FLOAT`
  - `humidity` : `FLOAT`
  - `co` : `FLOAT`

# Setup
## weather_cleaned table
```sql
CREATE TABLE `weather_cleaned` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `ts` TIMESTAMP NOT NULL,
  `location` VARCHAR(255) NOT NULL,
  `wind_sp` FLOAT,
  `wind_deg` INT,
  `pressure` FLOAT,
  `temperature` FLOAT,
  `humidity` FLOAT,
  `cloud_per` FLOAT,
  `rain_amt` FLOAT,
  `weather` VARCHAR(255)
);
```

## weather_api table
```sql
CREATE TABLE `weather_api` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `ts` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `latitude` FLOAT,
  `longitude` FLOAT,
  `wind_sp` FLOAT,
  `wind_deg` INT,
  `pressure` FLOAT,
  `temperature` FLOAT,
  `humidity` FLOAT,
  `cloud_per` FLOAT,
  `rain_amt` FLOAT DEFAULT '0',
  `weather` VARCHAR(50)
);
```

## weather_sensor table
```sql
CREATE TABLE `weather_sensor`(
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `ts` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `latitude` FLOAT,
  `longitude` FLOAT,
  `temperature` FLOAT,
  `humidity` FLOAT,
  `co` FLOAT
);
```