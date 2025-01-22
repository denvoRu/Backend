from src.infrastructure.exceptions.shared import AlreadyExistsException, Names


class TeacherAlreadyExistsException(AlreadyExistsException):
    def __init__(self):
        super().__init__(Names.TEACHER)
        

class TeacherAlreadyExistsInSubjectException(AlreadyExistsException):
    def __init__(self):
        super().__init__(Names.TEACHER, Names.SUBJECT)
