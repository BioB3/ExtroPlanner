# ExtroPlanner
API Web-application to aid in planing outdoor events/activities and monitor the current environment.

# Installation
1. clone the project using <br>```git clone https://github.com/BioB3/ExtroPlanner.git```
2. Rename ```config.py.example``` to ```config.py``` and input your database credentials

# Running the application
1. create a virtual env <br>```python -m venv env```
2. Activate the virtual environment<br>
    ```
    # on Mac/Linux use
    .env/bin/activate
    
    # on Windows use
    .\env\scripts\activate
    ```
3. Run the application<br>```uvicorn app:app --port 8000 --reload```
4. Go to http://127.0.0.1:8000/

# database schema
You will need a MySQL database with the following schema

# Prediction model + data acquisition
You can customize the prediction model and get sample code to collect data here: [khunakorn/ExtroPlanner-data](https://github.com/KhunakornP/ExtroPlanner-data)