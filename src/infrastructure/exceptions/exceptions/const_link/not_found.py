from src.infrastructure.exceptions.shared import NotFoundException, Names


class ConstLinkNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(Names.CONST_LINK)

