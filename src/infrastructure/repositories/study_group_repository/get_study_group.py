from src.infrastructure.database import StudyGroup, Teacher
from src.infrastructure.repositories import teacher_repository

from sqlmodel import select


async def get_by_id(subject_id, page, limit, columns, sort, search, desc):
    stmt = select(StudyGroup.teacher_id).where(StudyGroup.subject_id == subject_id)
    return await teacher_repository.get_all(
        page, 
        limit, 
        columns, 
        sort, 
        search, 
        desc, 
        [Teacher.id.in_(stmt)]
    )
    

def get_subject_ids_by_teacher_statement(teacher_ids):
    return (
        select(StudyGroup.subject_id)
        .where(StudyGroup.teacher_id.in_(teacher_ids))
    )
