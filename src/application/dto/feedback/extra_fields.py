from pydantic import BaseModel


class ExtraFields(BaseModel):
    """
    Extra fields that users can add to a feedback form
    """
    question: str
    answer: str
