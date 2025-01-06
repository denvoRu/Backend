from src.infrastructure.database import Subject

from sqlalchemy import select
from uuid import UUID


def stmt_get_by_module_id(module_id: UUID):
    return select(Subject.id).where(Subject.module_id == module_id)