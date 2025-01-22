from src.infrastructure.exceptions.helpers import to_many_form
from src.infrastructure.exceptions.shared import NotFoundException, Names


class FeedbacksNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(to_many_form(Names.FEEDBACK))

