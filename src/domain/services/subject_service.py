from src.application.dto.subject import CreateSubjectDTO, EditSubjectDTO
from src.infrastructure.repositories import (
    subject_repository, module_repository
)
from src.infrastructure.exceptions import (
    SubjectNotFoundException,
    ModuleNotFoundException,
    InvalidParametersException,
    SubjectAlreadyExistsException
)

from fastapi import Response, status
from uuid import UUID


async def get_all(
    page, 
    limit, 
    columns, 
    sort, 
    search, 
    desc, 
    teacher_ids, 
    module_id, 
    not_in_module_by_id,
    subject_without_teacher_by_id,
    not_has_const_link_by_teacher_id
):
    """
    Gets all subjects
    :param page: page number
    :param limit: count of subjects
    :param columns: fields to return
    :param sort: field to sort
    :param search: search string
    :param desc: sort direction
    :param teacher_ids: teacher ids
    :param module_id: module id
    :param not_in_module_by_id: is subject in module
    :param subject_without_teacher_by_id: subject without teacher
    """
    if teacher_ids is not None:
        teacher_ids = teacher_ids.split(",")

    if search is not None and search != "":
        search = "name*{0}".format(search)
    
    try:
        return await subject_repository.get_all(
            page, 
            limit, 
            columns, 
            sort, 
            search, 
            desc, 
            teacher_ids, 
            module_id,
            not_in_module_by_id,
            subject_without_teacher_by_id,
            not_has_const_link_by_teacher_id
        )
    except Exception:
        raise InvalidParametersException()


async def get_by_id(subject_id: UUID):
    if not await subject_repository.has_by_id(subject_id):
        raise SubjectNotFoundException()
    
    return await subject_repository.get_by_id(subject_id)
    

async def create(dto: CreateSubjectDTO):
    if await subject_repository.has_by_name(dto.name):
        raise SubjectAlreadyExistsException()
    
    if not await module_repository.has_by_id(dto.module_id):
        raise ModuleNotFoundException
 
    await subject_repository.add(dto.module_id, dto.name)
    return Response(status_code=status.HTTP_201_CREATED)


async def edit(subject_id: UUID, dto: EditSubjectDTO):
    try:
        dto = dto.model_dump(exclude_none=True)
        return await subject_repository.update_by_id(subject_id, dto)
    except:
        raise InvalidParametersException()


async def delete(subject_id: UUID):
    if not await subject_repository.has_by_id(subject_id):
        raise SubjectNotFoundException()
   
    return await subject_repository.delete_by_id(subject_id)
