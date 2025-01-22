from src.infrastructure.exceptions.shared import AlreadyExistsException, Names


class ModuleAlreadyExistsException(AlreadyExistsException):
    def __init__(self):
        super().__init__(Names.MODULE)
        