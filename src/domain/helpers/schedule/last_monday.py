from datetime import date, timedelta


def get_last_monday():
    """
    Gets last monday depending on which day is it today (needed for schedule)
    """
    today = date.today()
    last_monday = today - timedelta(days=today.weekday())
    return last_monday
