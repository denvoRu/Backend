from src.infrastructure.exceptions.shared import NotFoundException, Names


class ScheduleLessonNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(Names.SCHEDULE_LESSON)
        