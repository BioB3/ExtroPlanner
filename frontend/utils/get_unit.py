def get_unit(key: str):
    units = {
        "temperature": "°C",
        "humidity": "%",
        "rainfall": "mm"
    }
    return units[key.lower()]