from pydantic import BaseModel, Field


class EditInstituteDTO(BaseModel):
    # edit institute data transfer fields
    name: str = Field(default=None, min_length=2, max_length=100, examples=["Институт радиоэлектроники и информационных технологий-РТФ", "Институт новых материалов и технологий"])
    short_name: str = Field(default=None, min_length=2, max_length=50, examples=["ИРИТ-РТФ", "ИНМИТ"])
    address: str = Field(default=None, min_length=2, max_length=100, examples=["ул. Ленина, 1"])
