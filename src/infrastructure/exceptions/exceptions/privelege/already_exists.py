from src.infrastructure.exceptions.shared import AlreadyExistsException, Names


class PrivilegeAlreadyExistsException(AlreadyExistsException):
    def __init__(self):
        super().__init__(Names.PRIVILEGE)
        