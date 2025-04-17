import pandas as pd
import plotly.express as px
from utils import APIFetcher


def render_graph(y: str, location: str, days: int, detail: bool = False):
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
