from datetime import datetime

def format_datetime(ts: str | datetime):
    datetime_obj = ts
    if type(ts) is not datetime:
        datetime_obj = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")
    return datetime_obj.strftime("%d/%m/%Y %H:%M")