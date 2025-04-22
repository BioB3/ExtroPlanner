# ExtroPlanner
API Web-application to aid in planing outdoor events/activities and monitor the current environment.

# Installation
1. clone the project using <br>```git clone https://github.com/BioB3/ExtroPlanner.git```.
2. Rename ```config.py.example``` to ```config.py``` and input your database credentials.

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
or in the [project wiki](../../wiki/Database-Schema).

# Prediction model + data acquisition
The provided project already has starting models which are capable of weather prediction.<br>
The provided data allows for predictions at Kasetsart University and the Nak Niwat 48 district.
These models are (*to a degree*) capable of predicting weather conditions at other locations within Bangkok.<br><br>
To allow the models to predict weather conditions at other locations, add the sample observation data in the ```api/models/trained_models/data``` directory.<br>
(Note: The location data provided must be recorded in the Weather Data integration table)<br><br>
Tutorials to create your own prediction models and sample code to collect data can be found here: [khunakorn/ExtroPlanner-data](https://github.com/KhunakornP/ExtroPlanner-data)