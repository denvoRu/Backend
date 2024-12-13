from fastapi import Depends
from .user import User
from .check_role import RoleChecker

from typing_extensions import Annotated

class CurrentTeacher(Annotated[User, Depends(RoleChecker.teacher)]): ...
class CurrentAdmin(Annotated[User, Depends(RoleChecker.admin)]): ...