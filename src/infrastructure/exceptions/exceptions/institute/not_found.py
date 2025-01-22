from src.infrastructure.exceptions.shared import NotFoundException, Names


class InstituteNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(Names.INSTITUTE)
        