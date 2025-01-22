from src.infrastructure.exceptions.shared import AlreadyExistsException, Names


class SubjectAlreadyExistsException(AlreadyExistsException):
    def __init__(self):
        super().__init__(Names.SUBJECT)
        