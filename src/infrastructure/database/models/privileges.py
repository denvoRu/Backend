from sqlmodel import SQLModel, Field

class Privileges(SQLModel):
    __tablename__ = "privileges"

    id: int = Field(primary_key=True)
    teacher_id: int
    privilage: str