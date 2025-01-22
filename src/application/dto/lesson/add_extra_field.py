from pydantic import BaseModel, Field

class AddLessonExtraFieldDTO(BaseModel):
    name: str = Field(min_length=2, max_length=100, examples=["Вы поняли, как строится регрессионная модель?", "Что запомнилось больше всего?"])