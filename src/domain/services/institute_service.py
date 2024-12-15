from src.application.dto.institute import CreateInstitudeDTO, EditInstitudeDTO
from src.infrastructure.repositories import institute_repository
from fastapi import HTTPException, status


async def get_all(page, limit, columns, sort, filter, desc):
    return await institute_repository.get_all_institutes(
        page, 
        limit, 
        columns, 
        sort, 
        filter, 
        desc
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
    has_institute = await institute_repository.has_institute(dto.name)
    if has_institute:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Institute already exists"
        )
    
    await institute_repository.create_institute(
        dto.name, 
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
    