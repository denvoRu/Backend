from src.infrastructure.exceptions.shared import AlreadyExistsException, Names


class FeedbackAlreadyExistsException(AlreadyExistsException):
    def __init__(self):
        super().__init__(Names.FEEDBACK)
        