import aiohttp

from app import exceptions
from app.handlers import travel
from app.config import settings


# from app.handlers.exceptions import TownNotFoundException
# from app.schemas import GeographicDataResponse


class Geocoding:
    def __init__(self):
        self._geocoding_service_url = settings.GEOCODING_SERVICE_URL

    async def _get_geographic_data(self, city: str, _format: str = "json") -> dict:
        headers = {"Accept-Language": "ru, en"}
        async with aiohttp.ClientSession(headers=headers) as session:
            url = f"{self._geocoding_service_url}q={city}&format={_format}&addressdetails=1&limit=0&featureType=city"
            async with session.get(url=url) as resp:
                if resp.status == 200:
                    return await resp.json()
                raise exceptions.ExternalServiceError

    async def get_geographic_data(self, city: str) -> travel.Coordinate:
        response = await self._get_geographic_data(city=city)
        if response:
            country = response[0]["address"]["country"]
            return travel.Coordinate(latitude=response[0]["lat"],
                                      longitude=response[0]['lon'],
                                      country=country)
        raise exceptions.NoGeographicDataException(
            message=f"Не удалось найти данные для {city}"
        )


class Distance:

    def __init__(self):
        self._distance_service_url = settings.DISTANCE_SERVICE_URL
        self._distance_api_key = settings.dump_secret(settings.DISTANCE_API_KEY)

    def _get_distance_headers(self):
        headers = {
            "Content-Type": "application/json",
            "X-RapidAPI-Key": self._distance_api_key,
            "X-RapidAPI-Host": "distance-calculator.p.rapidapi.com"
        }
        return headers

    async def get_distance(self, lat_1: float, long_1: float, lat_2: float, long_2: float) -> dict:
        headers = self._get_distance_headers()
        params = {"lat_1": lat_1, "long_1": long_1, "lat_2": lat_2, "long_2": long_2,
                  "unit": "kilometers ", "decimal_places": "0"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self._distance_service_url, headers=headers, params=params) as resp:
                return await resp.json()


geocoding = Geocoding()
distance = Distance()
