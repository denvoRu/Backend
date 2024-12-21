from src.application.dto.institute import CreateInstitudeDTO, EditInstitudeDTO
from src.infrastructure.repositories import institute_repository
from fastapi import HTTPException, status


async def get_all(page, limit, columns, sort, search, desc):
    try: 
        if search is not None and search != "":
            search = "name*{0},short_name*{0}".format(search)
        return await institute_repository.get_all_institutes(
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
    try:
        return await institute_repository.get_institute(institute_id)
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institute not found"
        )


async def create_institute(dto: CreateInstitudeDTO):
    has_by_name = await institute_repository.has_by_name(dto.name)
    if has_by_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Institute already exists"
        )
    
    await institute_repository.create_institute(
        dto.name, 
        dto.short_name,
        dto.address
    )
    return { "status": "ok" }

async def edit_institute(institute_id: int, dto: EditInstitudeDTO):
    await institute_repository.edit_institute(
        institute_id, 
        dto.model_dump(exclude_none=True)
    )
    return { "status": "ok" }

async def delete_institute(institute_id: int):
    try: 
        await institute_repository.delete_institute(institute_id)
        return { "status": "ok" }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institute not found"
        )
    