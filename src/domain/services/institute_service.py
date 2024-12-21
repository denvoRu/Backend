from src.application.dto.institute import CreateInstituteDTO, EditInstituteDTO
from src.infrastructure.repositories import institute_repository

from fastapi import HTTPException, Response, status


async def get_all(page, limit, columns, sort, search, desc):
    if search is not None and search != "":
        search = "name*{0},short_name*{0}".format(search)
        
    try: 
        return await institute_repository.get_all(
            page, 
            limit, 
            columns, 
            sort, 
            search, 
            desc
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="One or more parameters are invalid"
        )

async def get_by_id(institute_id: int):
    if not await institute_repository.has_by_id(institute_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institute not found"
        )
 
    return await institute_repository.get_by_id(institute_id)
        


async def create_institute(dto: CreateInstituteDTO):
    has_by_name = await institute_repository.has_by_name(dto.name)
    if has_by_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Institute already exists"
        )
    
    await institute_repository.add(
        dto.name, 
        dto.short_name,
        dto.address
    )
    return Response(status_code=status.HTTP_201_CREATED)

async def edit_institute(institute_id: int, dto: EditInstituteDTO):
    await institute_repository.update_by_id(
        institute_id, 
        dto.model_dump(exclude_none=True)
    )
    return Response(status_code=status.HTTP_200_OK)

async def delete_institute(institute_id: int):
    try: 
        await institute_repository.delete_by_id(institute_id)
        return Response(status_code=status.HTTP_200_OK)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institute not found"
        )
    