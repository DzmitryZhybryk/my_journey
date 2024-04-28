import aiohttp

from app import schemas
from app.config import settings


# from app.handlers.exceptions import TownNotFoundException
# from app.schemas import GeographicDataResponse


class Geocoding:
    def __init__(self):
        self._geocoding_service_url = settings.GEOCODING_SERVICE_URL
        self._geocoding_api_key = settings.dump_secret(settings.GEOCODING_API_KEY)

    def _get_geocoding_headers(self):
        headers = {
            "X-RapidAPI-Key": self._geocoding_api_key,
            "X-RapidAPI-Host": "google-maps-geocoding.p.rapidapi.com"
        }
        return headers

    # @decorators.async_lru_cache_decorator
    async def _get_geographic_data(self, address: str, language: str) -> dict:
        headers = self._get_geocoding_headers()
        params = {"address": address, "language": language}
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self._geocoding_service_url, headers=headers, params=params) as resp:
                return await resp.json()

    async def get_geographic_data(self, address: str, language: str) -> schemas.Coordinate:
        response = await self._get_geographic_data(address=address, language=language)
        if not response.get("results"):
            #  TODO обработка исключения
            pass

        coordinates = response.get("results")[0].get("geometry").get("location")
        country = response.get("results")[0].get("address_components")[-1].get("long_name")
        return schemas.Coordinate(latitude=coordinates["lat"], longitude=coordinates['lng'], country=country)


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
