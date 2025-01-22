from src.infrastructure.exceptions.shared import NotFoundException, Names
from src.infrastructure.exceptions.helpers import to_many_form


class TeacherNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(Names.TEACHER)


class OneOrMoreTeachersNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(
            to_many_form(Names.TEACHER), 
            has_one_or_more=True
        )
     

class TeacherNotFoundInSubjectException(NotFoundException):
    def __init__(self):
        super().__init__(Names.TEACHER, Names.SUBJECT)
