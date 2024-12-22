from pydantic import BaseModel


class ExtraFields(BaseModel):
    question: str
    answer: str