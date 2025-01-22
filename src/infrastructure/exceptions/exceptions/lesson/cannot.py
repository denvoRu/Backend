from src.infrastructure.exceptions.shared import CannotException


class NotTodayDateException(CannotException):
    def __init__(self):
        super().__init__("change lessons for dates other than today")
    

class TimeLessOriginalException(CannotException):
    def __init__(self):
        super().__init__("set the time less than it was originally")
    

class DeleteLessonWithFeedbackException(CannotException):
    def __init__(self):
        super().__init__("delete a lesson with feedback")


class InitialFromScheduleException(CannotException):
    def __init__(self):
        super().__init__("create a lesson for this day")