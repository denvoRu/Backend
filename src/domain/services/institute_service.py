from src.application.dto.institute import CreateInstituteDTO, EditInstituteDTO
from src.infrastructure.repositories import institute_repository
from src.infrastructure.exceptions import (
    InstituteNotFoundException,
    InvalidParametersException,
    InstituteAlreadyExistsException
)

from fastapi import Response, status
from uuid import UUID


async def get_all(page, limit, columns, sort, search, desc):
    """
    Gets all institutes with needed filters
    :param page: page number
    :param limit: count of results to return
    :param columns: fields to return
    :param sort: field to sort by
    :param search: search string
    :param desc: sort direction
    """
    if search is not None and search != "":
        search = "name*{0},short_name*{0}".format(search)
        
    try: 
        return await institute_repository.get_all(
            page, limit, columns, sort, search, desc
        )
    except Exception:
        raise InvalidParametersException()


async def get_by_id(institute_id: UUID):
    if not await institute_repository.has_by_id(institute_id):
        raise InstituteNotFoundException()
 
    return await institute_repository.get_by_id(institute_id)
        

async def create(dto: CreateInstituteDTO):
    if await institute_repository.has_by_name(dto.name):
        raise InstituteAlreadyExistsException()
    
    await institute_repository.add(
        dto.name, 
        dto.short_name,
        dto.address
    )
    return Response(status_code=status.HTTP_201_CREATED)


async def edit(institute_id: UUID, dto: EditInstituteDTO):
    if not await institute_repository.has_by_id(institute_id):
        raise InstituteNotFoundException()
    
    await institute_repository.update_by_id(
        institute_id, 
        dto.model_dump(exclude_none=True)
    )
    return Response(status_code=status.HTTP_200_OK)


async def delete(institute_id: UUID):
    if not await institute_repository.has_by_id(institute_id):
        raise InstituteNotFoundException()

    await institute_repository.delete_by_id(institute_id)
    return Response(status_code=status.HTTP_200_OK)