# How to install

## Prerequisite requirements

- python 3.11 or newer
  - If your using windows you can check your python version by typing ```python --version```
  - For mac/linux use ```python3 --version``` <br>
  if you don't have a suitable version of python or you don't have python
  installed visit https://www.python.org/downloads/
- [Git](https://git-scm.com/downloads) for running git commands (Optional)<br>
- An ESP32 device capable of connecting to wifi
- A DHT(11/22) sensor, and a [MQ-9 Gas sensor](https://www.haoyuelectronics.com/Attachment/MQ-9/MQ9.pdf)
- A MySQL database
- A server hosting Node-RED

## Installation instructions
1. clone the repository with the following command
    - make sure you are in a suitable directory before cloning
    - alternatively download and extract the .zip file into the desired directory
   [here](https://github.com/BioB3/ExtroPlanner/releases)
   ```https://github.com/BioB3/ExtroPlanner.git```

2. Rename ```config.py.example``` to ```config.py``` and input your database credentials.
3. install required libraries as specified in [requirements.txt](requirements.txt)<br> Use:```pip install -r requirements.txt``` or your preferred package manager 