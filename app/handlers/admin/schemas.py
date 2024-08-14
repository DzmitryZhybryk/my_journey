from pydantic import BaseModel

from app.models import RoleEnum


class ChangeUserRoleSchema(BaseModel):
    user_id: int
    role: RoleEnum
