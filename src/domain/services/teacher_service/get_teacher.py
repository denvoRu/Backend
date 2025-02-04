from src.domain.extensions.check_role.user import User
from src.infrastructure.enums.privilege import Privilege
from src.infrastructure.enums.role import Role
from src.infrastructure.repositories import (
    teacher_repository,
    subject_repository
)
from src.infrastructure.exceptions import (
    TeacherNotFoundException,
    InvalidParametersException
)

from uuid import UUID


async def get_all(
    page: int = 1,
    limit: int = 10,
    columns: str = None,
    sort: str = None,
    search: str = None,
    desc: int = 0,
    rating_start: int = -1,
    rating_end: int = -1,
    institute_ids: str = None,
    subject_ids: str = None,
    not_in_subject_by_id: UUID = None
):
    """
    Gets all teachers
    :param page: page number
    :param limit: count of teachers
    :param columns: fields to show
    :param sort: field to sort by
    :param search: search string
    :param desc: sort desc
    :param rating_start: start rating of teacher
    :param rating_end: end rating of teacher
    :param subject_ids: subject ids
    :param not_in_subject_by_id: is teacher in subject
    """
    if subject_ids is not None:
        subject_ids = subject_ids.split(",")
    
    if institute_ids is not None:
        institute_ids = institute_ids.split(",")
        
    try:
        return await teacher_repository.get_all(
            page, 
            limit, 
            columns, 
            sort, 
            search, 
            desc,
            rating_start, 
            rating_end, 
            subject_ids,
            institute_ids=institute_ids,
            not_in_subject_by_id=not_in_subject_by_id,
        )
    except Exception:
        raise InvalidParametersException()


async def get_by_id(user: User, teacher_id: str):
    if not await teacher_repository.has_by_id(teacher_id):
        raise TeacherNotFoundException()

    teacher_data = await teacher_repository.get_by_id(teacher_id)
    
    if  user.role == Role.TEACHER and \
        not await teacher_repository.privilege.has_by_name(
        teacher_id, 
        Privilege.SEE_RATING
    ):
        teacher_data.pop("rating")
    privileges = await teacher_repository.privilege.get_by_id(teacher_id)

    teacher_data["privileges"] = privileges
    return teacher_data


async def get_subjects(
    teacher_id: UUID, 
    page: int = 1,
    limit: int = 10,
    desc: int = 0,
    columns: str = None,
    sort: str = None,
    search: str = None
):
    if not await teacher_repository.has_by_id(teacher_id):
        raise TeacherNotFoundException()
    
    if search is not None and search != "":
        search = "name*{0}".format(search)
    
    if columns is not None and columns != "":
        columns = columns.split(",")
    
    if sort is not None and sort != "":
        sort = sort.split(",")
    
    return await subject_repository.get_all(
        page, 
        limit, 
        columns, 
        sort, 
        search, 
        desc, 
        teacher_ids=[teacher_id]
    )
