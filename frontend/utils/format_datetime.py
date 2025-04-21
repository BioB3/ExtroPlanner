from datetime import datetime


def format_datetime(ts: str | datetime):
    datetime_obj = ts
    if type(ts) is not datetime:
        datetime_obj = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")
    return datetime_obj.strftime("%d/%m/%Y %H:%M")


def format_datetime_range(ts_range: str):
    ts1, ts2 = ts_range.split(" -- ")
    datetime_obj1 = datetime.strptime(ts1, "%Y-%m-%dT%H:%M:%S")
    if ts1 == ts2:
        return f'Around {datetime_obj1.strftime("%d/%m/%Y %H:%M")}'
    datetime_obj2 = datetime.strptime(ts2, "%Y-%m-%dT%H:%M:%S")
    return f'{datetime_obj1.strftime("%d/%m/%Y %H:%M")} to {datetime_obj2.strftime("%d/%m/%Y %H:%M")}'
