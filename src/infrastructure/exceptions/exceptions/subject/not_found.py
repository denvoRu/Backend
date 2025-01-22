from src.infrastructure.exceptions.shared import NotFoundException, Names
from src.infrastructure.exceptions.helpers import to_many_form


class SubjectNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(Names.SUBJECT)
        

class OneOrMoreSubjectsNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(
            to_many_form(Names.SUBJECT), 
            has_one_or_more=True
        )