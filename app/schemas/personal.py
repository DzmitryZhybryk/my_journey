from pydantic import BaseModel


class AddUserSchema(BaseModel):
    telegram_id: int
    full_name: str
    username: str | None
    nickname: str
