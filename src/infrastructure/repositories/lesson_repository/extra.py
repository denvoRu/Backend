from src.infrastructure.database import Lesson, StudyGroup, has_instance

from sqlalchemy import select
from uuid import UUID


async def is_teacher_of_lesson(teacher_id: UUID, lesson_id: UUID):
    """
    Checks that teacher is related to lesson
    """
    study_group_ids = select(StudyGroup.id).where(StudyGroup.teacher_id == teacher_id)

    return await has_instance(
        Lesson, 
        (Lesson.id == lesson_id,
         Lesson.study_group_id.in_(study_group_ids)) 
    )
    