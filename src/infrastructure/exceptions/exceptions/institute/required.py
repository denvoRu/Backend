from src.infrastructure.exceptions.shared import RequiredException, Names


class InstituteIsRequiredException(RequiredException):
    def __init__(self):
        super().__init__(Names.INSTITUTE)
        