from pydantic import BaseModel


class NewTravelContext(BaseModel):
    language: str
    first_place: str
    last_place: str
    transport: str
    year: int
