import math
from typing import List, TypeVar
from src.infrastructure.models.page_response import PageResponse
from src.infrastructure.database import db
from sqlalchemy import func, or_, select, text, desc as order_desc
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
    filter: str = None,
    desc: int = 0
) -> List[TableInstance]:
    hasColumn = columns is not None and columns != "all"
    hasSort = sort is not None and sort != "null"
    query = select(instance)

    if hasColumn:
        query = select(*[getattr(instance, x) for x in columns.split(',')])

    if filter is not None and filter != "null":
        criteria = dict(x.split("*") for x in filter.split(','))
        criteria_list = []

        for attr, value in criteria.items():
            _attr = getattr(instance, attr)
            search = "%{}%".format(value)
            criteria_list.append(_attr.like(search))

        query = query.filter(or_(*criteria_list))


    if hasSort:
        stmt = list(map(text, sort.split(',')))
                    
        if desc == 1:
            stmt = list(map(order_desc, stmt))
            
        query = query.order_by(*stmt)
    

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

    if hasColumn or hasSort:
        iterable = columns if hasColumn else sort
        result = list(
            {j[1]: j[0] for j in zip(i, iterable.split(','))} for i in result
        )
    else:
        result = list([i[0].model_dump() for i in result])
    return PageResponse(
        page_number=page,
        page_size=limit,
        total_pages=total_page,
        total_record=total_record,
        content=result
    )
        