from src.infrastructure.exceptions.shared import CannotException


class FutureDateException(CannotException):
    def __init__(self):
        super().__init__("set a future date")


class UpdateLessonWithFeedbackException(CannotException):
    def __init__(self):
        super().__init__("update a lesson with feedback") 


class DeleteLessonWithFeedbackException(CannotException):
    def __init__(self):
        super().__init__("delete a lesson with feedback")


class InitialFromScheduleException(CannotException):
    def __init__(self):
        super().__init__("create a lesson for this day")