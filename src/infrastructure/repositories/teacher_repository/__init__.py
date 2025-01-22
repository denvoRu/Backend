import src.infrastructure.repositories.teacher_repository.privilege as privilege
from .delete_teacher import delete_by_id
from .has_teacher import has_by_id, has_many
from .edit_teacher import update_by_id
from .get_teacher import (
    get_all, 
    get_by_id, 
    get_by_study_group, 
    get_id_by_study_group
)
