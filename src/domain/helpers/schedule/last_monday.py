from datetime import date, timedelta


def get_last_monday():
    today = date.today()
    last_monday = today - timedelta(days=today.weekday())
    return last_monday
