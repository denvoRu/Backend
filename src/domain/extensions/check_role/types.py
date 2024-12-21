from fastapi import Depends
from .user import User
from .check_role import RoleChecker

from typing_extensions import Annotated


CurrentTeacher = Annotated[User, Depends(RoleChecker.teacher)]
CurrentAdmin = Annotated[User, Depends(RoleChecker.admin)]