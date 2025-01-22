from src.infrastructure.exceptions.shared import AlreadyExistsException, Names


class ExtraFieldAlreadyExistsException(AlreadyExistsException):
    def __init__(self):
        super().__init__(Names.EXTRA_FIELD)
        