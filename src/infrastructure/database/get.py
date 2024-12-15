import math
from typing import List, TypeVar
from src.infrastructure.models.page_response import PageResponse
from src.infrastructure.database import db, commit_rollback
from sqlalchemy import func, or_, select, text, desc as order_desc

TableInstance = TypeVar("TableInstance")

async def get_by_id(instance: TableInstance, instance_id: str) -> TableInstance:
    select(instance).where(instance.id == instance_id)
    s = await db.execute(select(instance).where(instance.id == instance_id))
    
    data: TableInstance = s.first()[0]
    return data
    
async def get_all(
    instance: TableInstance,
    page: int = 1,
    limit: int = 10,
    columns: str = None,
    sort: str = None,
    search: str = None,
    desc: int = 0,
    filter: str = None
) -> List[TableInstance]:
    try:
        if columns is not None and columns != "all": 
            columns = columns.split(',')
            columns = delete_password_from_array(columns)
            has_column = len(columns) > 0
        else:
            has_column = False

        if sort is not None and sort != "null": 
            sort = sort.split(',')
            sort = delete_password_from_array(sort)
            has_sort = len(sort) > 0
        else:
            has_sort = False
        
        if search is not None and search != "null": 
            search = search.split(',')
            search = delete_password_from_array(search)
            has_search = len(search) > 0
        else:
            has_search = False

        query = select(instance)

        if has_column:
            query = select(*[getattr(instance, x) for x in columns])

        if filter is not None:
            query = query.where(filter)
            
        if has_search:
            criteria = dict(x.split("*") for x in search)
            criteria_list = []

            for attr, value in criteria.items():
                _attr = getattr(instance, attr)
                search_value = "%{}%".format(value)
                criteria_list.append(_attr.like(search_value))

            query = query.search(or_(*criteria_list))


        if has_sort:
            stmt = list(map(text, sort))
                        
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

        if has_column:
            iterable = columns if has_column else sort
            result = list(
                {j[0]: j[1] for j in zip(iterable, i)} for i in result
            )
        else:
            result = list([i[0].model_dump(
                exclude=["password"]
            ) for i in result])
        
        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_page,
            total_record=total_record,
            content=result
        )
    except Exception as e:
        await commit_rollback()
        raise Exception(str(e))
        

def delete_password_from_array(data: List[str]):
    data = list(set(data))
    try: 
        data.remove("password")
    except Exception as e: ...

    return data