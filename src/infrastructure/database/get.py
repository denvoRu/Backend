import math
from typing import List, TypeVar
from src.infrastructure.models.page_response import PageResponse
from src.infrastructure.database.initialize_database import get_session
from sqlalchemy import column, func, or_, select, text
from .extensions import user_to_save_dict

TableInstance = TypeVar("TableInstance")

async def get_by_id(instance_id: str, instance: TableInstance) -> TableInstance:
    async_session = get_session()

    async with async_session() as session:
        select(instance).where(instance.id == instance_id)
        s = await session.execute(select(instance).where(instance.id == instance_id))
        
        data: TableInstance = s.first()[0]
        return user_to_save_dict(data)
    
async def get_all(
    instance: TableInstance,
    page: int = 1,
    limit: int = 10,
    columns: str = None,
    sort: str = None,
    filter: str = None
) -> List[TableInstance]:
    async_session = get_session()

    async with async_session() as session:
        query = select(from_obj=instance, columns="*")

        if columns is not None and columns != "all":
        
            query = select(from_obj=instance, columns=convert_columns(columns))

        # select filter dynamically
        if filter is not None and filter != "null":
            # we need filter format data like this  --> {'name': 'an','country':'an'}

            # convert string to dict format
            criteria = dict(x.split("*") for x in filter.split('-'))

            criteria_list = []

            # check every key in dict. are there any table attributes that are the same as the dict key ?

            for attr, value in criteria.items():
                _attr = getattr(instance, attr)

                # filter format
                search = "%{}%".format(value)

                # criteria list
                criteria_list.append(_attr.like(search))

            query = query.filter(or_(*criteria_list))

        # select sort dynamically
        if sort is not None and sort != "null":
            # we need sort format data like this --> ['id','name']
            query = query.order_by(text(convert_sort(sort)))

        # count query
        count_query = select(func.count(1)).select_from(query)

        offset_page = page - 1
        # pagination
        query = (query.offset(offset_page * limit).limit(limit))

        # total record
        total_record = (await session.execute(count_query)).scalar() or 0

        # total page
        total_page = math.ceil(total_record / limit)

        result = (await session.execute(query)).fetchall()

        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_page,
            total_record=total_record,
            content=result
        )
        
def convert_sort(sort):
    """
    # separate string using split('-')
    split_sort = sort.split('-')
    # join to list with ','
    new_sort = ','.join(split_sort)
    """
    return ','.join(sort.split('-'))


def convert_columns(columns):
    """
    # seperate string using split ('-')
    new_columns = columns.split('-')

    # add to list with column format
    column_list = []
    for data in new_columns:
        column_list.append(data)

    # we use lambda function to make code simple

    """

    return list(map(lambda x: column(x), columns.split('-')))
