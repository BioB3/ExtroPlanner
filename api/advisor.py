from datetime import datetime
from typing import Collection, Any


class HeatIndexCalculator:
    __c1 = -8.78469475556
    __c2 = 1.61139411
    __c3 = 2.33854883889
    __c4 = -0.14611605
    __c5 = -0.012308094
    __c6 = -0.0164248277778
    __c7 = 2.211732e-3
    __c8 = 7.2546e-4
    __c9 = -3.582e-6

    @classmethod
    def calculate_heat_index(cls, t: float, h: float | int) -> float:
        """
        Return the calculated heat index

        Calculates a heat index using recorded temperature and
        relative humidity values.

        :param t: The temperature in Celsius
        :param h: The relative humidity in percentage
        :return: The calculated heat index in Celsius
        """
        return (
            cls.__c1
            + cls.__c2 * t
            + cls.__c3 * h
            + cls.__c4 * t * h
            + cls.__c5 * (t**2)
            + cls.__c6 * (h**2)
            + cls.__c7 * (t**2) * h
            + cls.__c8 * (h**2) * t
            + cls.__c9 * (h**2) * (t**2)
        )


class EventAdvisor:
    __rain_threshold = 0.8
    __heat_threshold = 0.8
    __heat_warn = 40.0
    __heat_danger = 45.0

    @classmethod
    def get_heat_index(cls, weather_data: Collection[dict[Any]]) -> list[float]:
        indexes = []
        for data in weather_data:
            heat_index = HeatIndexCalculator.calculate_heat_index(
                data["temperature"], data["humidity"]
            )
            indexes.append(heat_index)
        return indexes

    @classmethod
    def get_weather_conditions_summary(cls, weather_data):
        max_temp = max(weather_data, key=lambda x: x["temperature"])
        heat_indexes = cls.get_heat_index(weather_data)
        max_heat = max(heat_indexes)
        return {"max_temp": max_temp, "max_heat": max_heat}

    @classmethod
    def get_descriptive_event_advice(cls, weather_data):
        metrics = cls.get_event_metrics(weather_data)
        decision = cls.get_host_event_decision(
            metrics["rain_ratio"],
            metrics["max_heat"],
            metrics["heat_ratio"],
            metrics["duration"],
        )
        data = {}
        if decision:
            data["suggestion"] = "Can host event."
            data["description"] = "Overall weather is suitable for outdoor activites."
        else:
            data["suggestion"] = "Should not host event."
            data["description"] = "Weather is unsuitable for outdoor activities."
        data["items"] = cls.get_suggested_equipment(
            metrics["rain_ratio"], metrics["heat_ratio"], metrics["duration"]
        )
        rain_periods, heat_periods = cls.get_extreme_weather_periods(weather_data)
        data["rain_periods"] = rain_periods
        data["heat_periods"] = heat_periods
        return data

    @classmethod
    def get_extreme_weather_periods(cls, weather_data):
        rain_periods = []
        start = None
        end = None
        for entry in weather_data:
            if entry["weather"] == "rain":
                if not start:
                    start = entry["ts"]
                end = entry["ts"]
            else:
                if start:
                    rain_periods.append(f"{start} -- {end}")
                    start = None
        if start:
            rain_periods.append(f"{start} -- {end}")

        indexes = cls.get_heat_index(weather_data)
        hot_periods = []
        start = None
        end = None
        for i in range(len(indexes)):
            if indexes[i] >= cls.__heat_warn:
                if not start:
                    start = weather_data[i]["ts"]
                end = weather_data[i]["ts"]
            else:
                if start:
                    hot_periods.append(f"{start} -- {end}")
                    start = None
        if start:
            hot_periods.append(f"{start} -- {end}")
        return rain_periods, hot_periods

    @classmethod
    def get_event_metrics(cls, weather_data):
        rain_count = sum(x["weather"] == "rain" for x in weather_data)
        rain_ratio = rain_count / len(weather_data)
        heat_indexes = cls.get_heat_index(weather_data)
        max_heat = max(heat_indexes)
        heat_ratio = sum(index > cls.__heat_warn for index in heat_indexes) / len(
            heat_indexes
        )
        start_time = datetime.fromisoformat(weather_data[0]["ts"])
        end_time = datetime.fromisoformat(weather_data[-1]["ts"])
        duration = abs(end_time - start_time).seconds // 360
        return {
            "rain_ratio": rain_ratio,
            "max_heat": max_heat,
            "heat_ratio": heat_ratio,
            "duration": duration,
        }

    @classmethod
    def get_host_event_decision(cls, rain_ratio, max_heat, heat_ratio, duration):
        if rain_ratio >= cls.__rain_threshold:
            return False
        if max_heat > cls.__heat_danger:
            return False
        if duration <= 3:
            return True
        if heat_ratio >= cls.__heat_threshold:
            return False
        return True

    @classmethod
    def get_suggested_equipment(cls, rain_ratio, heat_ratio, duration):
        items = []
        if rain_ratio > 0:
            items.append("Umbrellas")
        if rain_ratio > 0.5:
            items.append("Tents")
        if heat_ratio > 0.2:
            items.append("Water")
        if duration <= 3:
            return items
        if heat_ratio > 0.5:
            items.append("Fans")
        if heat_ratio > 0.7:
            if duration > 5:
                items.append("Tents")
            else:
                items.append("Umbrellas")
        return items
