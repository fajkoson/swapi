import logging
import aiohttp
from swpackage.decorators import time_decorator

logger = logging.getLogger(__name__)

class SWFetcher:
    def __init__(self, config) -> None:
        self.config = config

    @time_decorator
    async def fetch_person(self, person_id: int) -> dict:
        """fetch person by ID and return name and height"""
        url = f"{self.config['person_url']}{person_id}/"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return {'name': data['name'], 'height': data['height']}
            except aiohttp.ClientResponseError as http_err:
                await self.check_base_url()
                logger.exception(f"HTTP error occurred while fetching person: {http_err}")
                raise Exception(f"HTTP error occurred while fetching person: {http_err}") from http_err
            except Exception as err:
                logger.exception(f"exception occured {err}")
                raise Exception(f"an unexpected error occurred while fetching person: {err}") from err
    @time_decorator
    async def fetch_planet(self, planet_id: int) -> dict:
        """fetch planet by ID and return name and terrain"""
        url = f"{self.config['planet_url']}{planet_id}/"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return {'name': data['name'], 'terrain': data['terrain']}
            except aiohttp.ClientResponseError as http_err:
                await self.check_base_url()
                logger.exception(f"exception occured {http_err}")
                raise Exception(f"HTTP error occurred while fetching planet: {http_err}") from http_err
            except Exception as err:
                logger.exception(f"exception occured {err}")
                raise Exception(f"an unexpected error occurred while fetching planet: {err}") from err
    @time_decorator
    async def check_base_url(self) -> None:
        """check if the base URL is reachable."""
        async with aiohttp.ClientSession() as session:    
            try:
                async with session.get(self.config['base_url']) as response:
                    if response.status != self.config['status_code_OK']:
                        logger.error(f"base URL check failed with status code: {response.status_code}. Possible API issue...")   
            except aiohttp.ClientError as e:
                logger.error(f"failed to reach the base URL. {e}")
