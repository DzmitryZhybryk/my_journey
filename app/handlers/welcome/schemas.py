from pydantic import BaseModel


class AllCommandSchema(BaseModel):
    help: str = "Памагити!"
    start: str = "Начать работу с ботом"
    cancel: str = "Отменить все и вернуться к началу"


class AddUserSchema(BaseModel):
    telegram_id: int
    full_name: str
    username: str | None
    nickname: str
