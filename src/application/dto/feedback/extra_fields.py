from pydantic import BaseModel, Field


class ExtraFields(BaseModel):
    """
    Extra fields that users can add to a feedback form
    """
    question: str = Field(default="", min_length=2, max_length=100)
    answer: str = Field(default="", min_length=2, max_length=300)
