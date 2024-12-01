from sqlalchemy import Column, Integer, String

from src.database.initialize_database import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_first_name = Column(String(100))
    user_second_name = Column(String(100))
    user_third_name = Column(String(100))
    user_email = Column(String(255))
    user_password = Column(String(72))