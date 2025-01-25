from src.domain.extensions.get_hex_uuid import get_hex_uuid
from src.domain.extensions.email.email_sender import EmailSender
from src.infrastructure.repositories import (
    auth_repository
)
from src.application.dto.auth import (
    RestorePasswordDTO, 
    UpdatePasswordDTO
)
from src.infrastructure.exceptions import UserNotFoundException
from src.domain.helpers.auth import (
    add_restore_data_in_redis,
    get_restore_password_link, get_restore_token_from_redis,
    is_in_teacher_or_admin
)

from fastapi import HTTPException, Response, status
from bcrypt import hashpw, gensalt

    
async def restore_password(dto: RestorePasswordDTO):
    if not await is_in_teacher_or_admin(dto.email, dto.role):
        raise UserNotFoundException()

    # get token, add this data in Redis and create a restore link
    restore_token = get_hex_uuid()
    add_restore_data_in_redis(dto.email, dto.role, restore_token)
    restore_password_link = get_restore_password_link(restore_token)
    # await EmailSender.send_update_password(dto.email, restore_password_link)
    return Response(status_code=status.HTTP_200_OK)


async def update_password_from_token(dto: UpdatePasswordDTO):
    try:
        rp = get_restore_token_from_redis(dto.restore_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Restore token is expired"
        )

    # hashes a new password if check is passed and updates it
    salt = gensalt()
    dto.password = hashpw(dto.password.encode(), salt).decode()
    await auth_repository.update_password(rp.email, rp.role, dto.password) 
    return Response(status_code=status.HTTP_200_OK)
