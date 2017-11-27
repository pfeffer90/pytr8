import datetime

TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def get_current_time():
    return datetime.datetime.now()

def get_current_time_as_string():
    return get_current_time().strftime(TIME_FORMAT)
