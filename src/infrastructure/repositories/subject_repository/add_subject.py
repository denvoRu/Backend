from src.infrastructure.database import Subject, Module, add_instance, db

from typing import List
from aiomodeus.student_voice.subject import Subject as SubjectModeus
from uuid import UUID


async def add(module_id: UUID, name: str):
    module = Subject(
        module_id=module_id,
        name=name,
        rating=0
    )
    await add_instance(module)


async def add_from_modeus(institute_id: UUID, subjects: List[SubjectModeus]):
    """
    Import subjects from modeus to institute
    """
    for subject in subjects:
        module_id = await subject.find_in_orm(
            db, 
            Module, 
            whereclause=(
                Module.institute_id == institute_id,
                Module.name == subject.module_name
            ),
            columns=["id"]
        )
        
        subject = Subject(
            module_id=module_id[0][0],
            name=subject.name,
            rating=0            
        )
        db.add(subject)
    
    await db.commit_rollback()
    