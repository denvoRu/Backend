from datetime import date


def get_semester_end_date():
    """
    Returns the end date of the current semester.
    The first semester ends on June 23,
    The second semester ends on December 23.

    :return: the end date of the current semester (datetime.date)
    """
    today = date.today()  # Get the current date
    year = today.year  # Extract the current year

    # Define semester end dates
    summer_semester_end = date(year, 6, 23)  # End date of the summer semester
    winter_semester_end = date(year, 12, 23)  # End date of the winter semester

    # Determine the current semester
    if today <= summer_semester_end:
        return summer_semester_end  # Return summer semester end date
    else:
        return winter_semester_end  # Return winter semester end date
