import math
from typing import List, TypeVar
from src.infrastructure.models.page_response import PageResponse
from src.infrastructure.database import db
from sqlalchemy import column, func, or_, select, text
from .extensions import user_to_save_dict

TableInstance = TypeVar("TableInstance")

async def get_by_id(instance_id: str, instance: TableInstance) -> TableInstance:
    select(instance).where(instance.id == instance_id)
    s = await db.execute(select(instance).where(instance.id == instance_id))
    
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
    query = select(instance)

    if columns is not None and columns != "all":
        query = select(instance, convert_columns(columns))

    if filter is not None and filter != "null":
        criteria = dict(x.split("*") for x in filter.split('-'))
        criteria_list = []

        for attr, value in criteria.items():
            _attr = getattr(instance, attr)
            search = "%{}%".format(value)
            criteria_list.append(_attr.like(search))

        query = query.filter(or_(*criteria_list))


    if sort is not None and sort != "null":
        query = query.order_by(text(convert_sort(sort)))

    # count query
    count_query = select(func.count(1)).select_from(query)
    offset_page = page - 1

    # pagination
    query = (query.offset(offset_page * limit).limit(limit))

    # total record
    total_record = (await db.execute(count_query)).scalar() or 0

    # total page
    total_page = math.ceil(total_record / limit)

    result = (await db.execute(query)).fetchall()


    return PageResponse(
        page_number=page,
        page_size=limit,
        total_pages=total_page,
        total_record=total_record,
        content=list([i[0].model_dump() for i in result])
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
