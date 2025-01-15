from src.infrastructure.database import db
from sqlalchemy import select, ColumnExpressionArgument
from typing import Union


async def has_instance(instance, where_args: Union[tuple, ColumnExpressionArgument]):
    where_is_tuple = isinstance(where_args, tuple)
    stmt = select(instance)
    
    if where_is_tuple:
        where_args = list(where_args)
    else: 
        where_args = [where_args]
    
    if hasattr(instance, "is_disabled"):
        where_args.append(instance.is_disabled == False)

    stmt = stmt.where(*where_args)

    s = await db.execute(stmt)
    return len(s.all()) > 0
