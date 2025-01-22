from src.infrastructure.exceptions.shared import AlreadyExistsException, Names


class ConstLinkAlreadyExistsException(AlreadyExistsException):
    def __init__(self):
        super().__init__(Names.CONST_LINK)
        