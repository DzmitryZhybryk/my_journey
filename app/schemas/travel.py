from pydantic import BaseModel


class NewTravelContext(BaseModel):
    language: str
    first_place: str
    last_place: str
    transport: str
    year: int


class AddTravelSchema(BaseModel):
    distance: float
    transport_type: str
    travel_year: int
    user_id: int
    location: dict[str, str]
