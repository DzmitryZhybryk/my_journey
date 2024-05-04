from pydantic import BaseModel


class NewTravelContext(BaseModel):
    first_place: str
    second_place: str
    transport: str
    year: int


class PointSchema(BaseModel):
    town: str
    country: str


class LocationSchema(BaseModel):
    from_: PointSchema
    to: PointSchema


class AddTravelSchema(BaseModel):
    distance: float
    transport_type: str
    travel_year: int
    user_id: int
    location: LocationSchema


class GetTravelSchema(BaseModel):
    travel_id: int
    distance: float
    transport_type: str
    travel_year: int
    location: LocationSchema
