from src.infrastructure.repositories import institute_repository


async def get_rating(): 
    return await institute_repository.get_overall_rating()
