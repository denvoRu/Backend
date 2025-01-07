from typing import Optional
from pydantic import BaseModel, Field


class EditInstituteDTO(BaseModel):
    # edit institute data transfer fields
    name: Optional[str] = Field(min_length=2, max_length=100, default=None, examples=["Институт радиоэлектроники и информационных технологий-РТФ", "Институт новых материалов и технологий"])
    short_name: Optional[str] = Field(min_length=2, max_length=50, default=None, examples=["ИРИТ-РТФ", "ИНМИТ"])
    address: Optional[str] = Field(min_length=2, max_length=100, default=None, examples=["ул. Ленина, 1"])
