from src.infrastructure.exceptions.shared import NotFoundException, Names


class UserNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(Names.USER)
        