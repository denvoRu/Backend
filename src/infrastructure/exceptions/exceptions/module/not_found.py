from src.infrastructure.exceptions.shared import NotFoundException, Names


class ModuleNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(Names.MODULE)
        