from math import ceil
from typing import List, TypeVar
from src.infrastructure.models.page_response import PageResponse
from src.infrastructure.database import db
from sqlalchemy import func, or_, select, text, desc as order_desc


TableInstance = TypeVar("TableInstance")


async def get_all(
    instance: TableInstance,
    page: int = 1,
    limit: int = 10,
    columns: str = None,
    sort: str = None,
    search: str = None,
    desc: int = 0,
    filters: list = None
) -> List[TableInstance]:
    try:
        filters = filters if filters is not None else []

        if columns is not None and columns != "all": 
            columns = columns.split(",")
            columns = delete_unsafe_data_from_array(columns)
            has_column = len(columns) > 0
        else:
            has_column = False

        if sort is not None and sort != "null": 
            sort = sort.split(",")
            sort = delete_unsafe_data_from_array(sort)
            has_sort = len(sort) > 0
        else:
            has_sort = False
        
        if search is not None and search != "null": 
            search = search.split(",")
            search = delete_unsafe_data_from_array(search)
            has_search = len(search) > 0
        else:
            has_search = False

        query = select(instance)

        if has_column:
            query = select(*[getattr(instance, x) for x in columns])

        if has_search:
            criteria = dict(x.split("*") for x in search)
            criteria_list = []

            for attr, value in criteria.items():
                _attr = getattr(instance, attr)
                search_value = "%{}%".format(value)
                criteria_list.append(func.lower(_attr).like(search_value.lower()))

            query = query.filter(or_(*criteria_list))

        if hasattr(instance, "is_disabled"):
            filters.append(instance.is_disabled == False)

        query = query.where(*filters)

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
        total_page = ceil(total_record / limit)

        result = (await db.execute(query)).fetchall()

        if has_column:
            iterable = columns if has_column else sort
            result = list(
                {j[0]: j[1] for j in zip(iterable, i)} for i in result
            )
        else:
            result = list([i[0].model_dump(
                exclude={"password", "is_disabled"}
            ) for i in result])
        
        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_page,
            total_record=total_record,
            content=result
        )
    except Exception as e:
        await db.commit_rollback()
        raise Exception(str(e))
        

def delete_unsafe_data_from_array(data: List[str]):
    data = list(set(data))
    try: 
        data.remove("password")
    except: ...
    try: 
        data.remove("is_disabled")
    except: ...

    return data


async def get_by_id(
    instance: TableInstance, 
    instance_id: str, 
    attr_name: str = None, 
    id_name = "id"
) -> TableInstance:
    try:
        where_args = [getattr(instance, id_name) == instance_id]
        getted_instance =  getattr(instance, attr_name) if attr_name else instance

        if hasattr(instance, "is_disabled"):
            where_args.append(instance.is_disabled == False)
        s = await db.execute(
            select(getted_instance)
            .where(*where_args)
        )
        
        data: TableInstance = s.first()[0]
        return data
    except Exception as e:
        await db.commit_rollback()
        raise Exception(str(e))
