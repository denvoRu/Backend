from src.infrastructure.database import Institute, get, db

from sqlalchemy import select
from uuid import UUID


async def get_all(page, limit, columns, sort, search, desc):
    """
    Gets all institutes
    :param page: current page
    :param limit: limit of institutes
    :param columns: fields to get
    :param sort: field to sort by
    :param search: search string
    :param desc: sort direction
    """
    return await get.get_all(
        Institute,
        page, 
        limit, 
        columns, 
        sort, 
        search, 
        desc
    )


async def get_by_id(institute_id: UUID):
    return await get.get_by_id(Institute, institute_id)


async def get_overall_rating():
    """
    Gets an overall institutes rating
    """
    stmt = select(Institute.rating).where(Institute.rating > 0.0)

    ratings = await db.execute(stmt)
    ratings = [i[0] for i in ratings.all()]

    return sum(ratings) / len(ratings)
