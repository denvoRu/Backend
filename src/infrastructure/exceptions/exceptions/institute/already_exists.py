from src.infrastructure.exceptions.shared import AlreadyExistsException, Names


class InstituteAlreadyExistsException(AlreadyExistsException):
    def __init__(self):
        super().__init__(Names.INSTITUTE)
        