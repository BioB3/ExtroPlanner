# ExtroPlanner
API Web-application to aid in planing outdoor events/activities and monitor the current environment.

# Members:

| Name                  | ID         | Department                         | Faculty     |
|-----------------------|------------|------------------------------------|-------------|
| Khunakorn Pattayakorn | 6610545766 | Software and Knowledge Engineering | Engineering |
| Phasin    Sae-Ngow    | 6610545383 | Software and Knowledge Engineering | Engineering |

# Project Overview:
## Main features
- Visualisations for historical weather data.
- View latest sensor readings.
- Predictions for future weather conditions.
- Event advisor to suggest if an event should be conducted and recommend equipment based on predicted weather conditions.

## APIs provided

1. Weather statistics endpoints

| Endpoint             | Method | Description                                                                                                                             |
|----------------------|--------|-----------------------------------------------------------------------------------------------------------------------------------------|
| `/locations`         | GET    | Return locations with observed weather data                                                                                             |
| `/weather`           | GET    | Return the Latest weather observation for the given location.<br> If a date is specified return the closet observation to that date.    |
| `/weather/last`      | GET    | Return weather observations from the last x days.<br> If no duration is specified return weather observations from yesterday.           |
| `/weather/aggregate` | GET    | Return aggregated weather data from the last x days.<br> If no duration is specified return weather data from yesterday.                |
| `/temperature/max`   | GET    | Return the maximum observed temperature from the last x days. If no duration is specified return the maximum temperature from yesterday |
| `/temperature/min`   | GET    | Return the minimum observed temperature from the last x days. If no duration is specified return the minimum temperature from yesterday |
| `/humidity/max`      | GET    | Return the maximum observed humidity from the last x days. If no duration is specified return the maximum humidity from yesterday       |
| `/humidity/min`      | GET    | Return the minimum observed humidity from the last x days. If no duration is specified return the minimum humidity from yesterday       |
| `/pressure/max`      | GET    | Return the maximum observed pressure from the last x days. If no duration is specified return the maximum pressure from yesterday       |
| `/pressure/min`      | GET    | Return the minimum observed pressure from the last x days. If no duration is specified return the minimum pressure from yesterday       |
| `/rainfall/max`      | GET    | Return the maximum observed rainfall from the last x days. If no duration is specified return the maximum rainfall from yesterday       |
| `/rainfall/min`      | GET    | Return the minimum observed rainfall from the last x days. If no duration is specified return the minimum rainfall from yesterday       |
| `/sensor/latest`     | GET    | Return the Latest weather observation from the sensor.                                                                                  |

2. prediction endpoints

| Endpoint               | Method | Description                                                                                                                                                                          |
|------------------------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/predict/temperature` | GET    | Predicts temperature values from the last observed date in the models training data until the specified date for the given location.                                                 |
| `/predict/humidity`    | GET    | Predicts humidity values from the last observed date in the models training data until the specified date for the given location.                                                    |
| `/predict/pressure`    | GET    | Predicts pressure values from the last observed date in the models training data until the specified date for the given location.                                                    |
| `/predict/rain`        | GET    | Predicts hourly rain from the last observed date in the models training data until the specified date for the given location. (Each returned value is either cloudy/no rain or rain) |

3. Evaluation endpoints

| Endpoint            | Method   | Description                                                                                                                                                   |
|---------------------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/event/conditions` | GET      | Return the predicted weather conditions during the given period, maximum predicted temperature, highest heat index calculated, and rainy periods.             |
| `/event/describe`   | POST     | Return a suggestion for hosting the event (yes/no), along with a description of important weather periods (heat wave, rainy periods) and suggested equipment. |
| `/heatindex`        | GET/POST | When the method is GET, calculates a single heat index. Use POST for calculating multiple heat indices.                                                       |

# Installation
Please see [Installation.md](installation.md) for installation instructions.

# Using the application
## Running the backend (API service)
1. create a virtual env. <br>```python -m venv env```
2. Activate the virtual environment.<br>
    ```
    # on Mac/Linux use
    .env/bin/activate
    
    # on Windows use
    .\env\scripts\activate
    ```
3. In the projects root directory, Run the backend using:<br>
   ```python -m uvicorn api.app:app_api --port 8000 --reload```
4. Use http://127.0.0.1:8000/explan/ as a base path to call the API<br> 
or go to http://127.0.0.1:8000/docs/ to call the APIs using a GUI

## Running the frontend (Web application + Visualizations)
1. Run the [backend](#running-the-backend-api-service) using the provided instructions.
2. navigate to the ```frontend``` directory.
3. Run the frontend using: ```streamlit run main.py```
4. Wait for the site to load.
5. If the site does not open automatically, go to http://localhost:8501/ .

# Database Schema
You will need a MySQL database to run this project.<br>
you can find the required database schema in the [database setup readme](database_setup.md#overview)
or in the [project wiki](../../wiki/Database%20Schema).

# Prediction model + data acquisition
The provided project already has starting models which are capable of weather prediction.<br>
The provided data allows for predictions at Kasetsart University and the Nak Niwat 48 district.
These models are (*to a degree*) capable of predicting weather conditions at other locations within Bangkok.<br><br>
To allow the models to predict weather conditions at other locations, add the sample observation data in the ```api/models/trained_models/data``` directory.<br>
(Note: The location data provided must be recorded in the Weather Data integration table)<br><br>
Tutorials to create your own prediction models and sample code to collect data can be found here: [khunakorn/ExtroPlanner-data](https://github.com/KhunakornP/ExtroPlanner-data)