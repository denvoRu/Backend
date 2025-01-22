from src.infrastructure.exceptions.shared import NotFoundException, Names


class ExtraFieldNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(Names.EXTRA_FIELD)

