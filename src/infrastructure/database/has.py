from src.infrastructure.database import db
from sqlalchemy import select, ColumnExpressionArgument
from typing import Union

async def has_instance(instance, where: Union[tuple, ColumnExpressionArgument]):
    where_is_tuple = isinstance(where, tuple)
    stmt = select(instance)
    
    if where_is_tuple:
        stmt = stmt.where(*where)
    else: 
        stmt = stmt.where(where)

    s = await db.execute(stmt)
    return len(s.all()) > 0