from typing import Optional
from pydantic import BaseModel, Field


class EditInstituteDTO(BaseModel):
    name: Optional[str] = Field(max_length=100, default=None, examples=["Институт радиоэлектроники и информационных технологий-РТФ", "Институт новых материалов и технологий"])
    short_name: Optional[str] = Field(max_length=50, default=None, examples=["ИРИТ-РТФ", "ИНМИТ"])
    address: Optional[str] = Field(max_length=100, default=None, examples=["ул. Ленина, 1"])
