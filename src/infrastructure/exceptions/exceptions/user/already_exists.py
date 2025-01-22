from src.infrastructure.exceptions.shared import AlreadyExistsException, Names


class UserAlreadyExistsException(AlreadyExistsException):
    def __init__(self):
        super().__init__(Names.USER)
        