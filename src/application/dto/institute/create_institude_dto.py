from pydantic import BaseModel, Field


class CreateInstituteDTO(BaseModel):
    name: str = Field(min_length=2, max_length=100, examples=["Институт радиоэлектроники и информационных технологий-РТФ", "Институт новых материалов и технологий"])
    short_name: str = Field(min_length=2, max_length=50, examples=["ИРИТ-РТФ", "ИНМИТ"])
    address: str = Field(min_length=2, max_length=100, examples=["ул. Ленина, 1"])
