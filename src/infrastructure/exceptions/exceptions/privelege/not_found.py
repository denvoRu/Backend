from src.infrastructure.exceptions.shared import NotFoundException, Names


class PrivilegeNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(Names.PRIVILEGE)
        