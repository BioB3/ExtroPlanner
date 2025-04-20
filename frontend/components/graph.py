import pandas as pd
import plotly.express as px
from datetime import datetime
from utils import APIFetcher


def render_old_data_graph(y: str, location: str, days: int, detail: bool = False):
    try:
        if detail:
            data = APIFetcher.get_last_days_weather(location, days)
        else:
            data = APIFetcher.get_aggregate_weather(location, days)
        df = pd.DataFrame.from_dict(data)
        return px.line(data_frame=df, x="ts", y=y,
                    labels={
                        "ts": "Datetime",
                        y: f"{y.capitalize()}"
                    })
    except ValueError:
        return None

def render_prediction_data(y: str, location: str, start: datetime, end: datetime):
    func_call = {
        "temperature": APIFetcher.get_temperature_prediction
    }

    df = func_call[y](location, start, end)
    return px.line(data_frame=df, x="ts", y=y,
                    labels={
                        "ts": "Datetime",
                        y: f"{y.capitalize()}"
                    })
    
