from src.infrastructure.exceptions.shared import NotFoundException, Names


class LessonNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(Names.LESSON)
        