from src.infrastructure.exceptions.shared import RequiredException, Names
from src.infrastructure.exceptions.helpers import to_many_form 


class SubjectsAreRequiredException(RequiredException):
    def __init__(self):
        super().__init__(
            to_many_form(Names.SUBJECT),
            has_are=True
        )
        