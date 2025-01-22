from src.infrastructure.exceptions.shared import NotFoundException, Names


class AdministratorNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(Names.ADMINISTRATOR)
        