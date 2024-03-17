import logging
import requests
from .conf_load import ConfLoader

logging.basicConfig(
    level=logging.INFO,  # (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'  
)

class SWFetcher:
    def __init__(self, config) -> None:
        self.config = config

    def fetch_person(self, person_id: int) -> dict:
        """fetch person by ID and return name and height"""
        url = f"{self.config['person_url']}{person_id}/"
        try:
            response = requests.get(url)
            # raise HTTPError if the request returned wrong code
            response.raise_for_status()
            data = response.json()
            return {'name': data['name'], 'height': data['height']}
        except requests.exceptions.HTTPError as http_err:
            # check api only if fetching fails - to reduce requests
            self.check_base_url()
            logging.exception(f"exception occured {http_err}")
            raise Exception(f"HTTP error occurred while fetching person: {http_err}")
        except Exception as err:
            logging.exception(f"exception occured {err}")
            raise Exception(f"an unexpected error occurred while fetching person: {err}")

    def fetch_planet(self, planet_id: int) -> dict:
        """fetch planet by ID and return name and terrain"""
        url = f"{self.config['planet_url']}{planet_id}/"
        try:
            response = requests.get(url)
            # raise HTTPError if the request returned wrong code
            response.raise_for_status()
            data = response.json()
            return {'name': data['name'], 'terrain': data['terrain']}
        except requests.exceptions.HTTPError as http_err:
            # check api only if fetching fails - to reduce requests           
            self.check_base_url()
            logging.exception(f"exception occured {http_err}")
            raise Exception(f"HTTP error occurred while fetching planet: {http_err}")
        except Exception as err:
            logging.exception(f"exception occured {err}")
            raise Exception(f"an unexpected error occurred while fetching planet: {err}")

    def check_base_url(self) -> None:
        """check if the base URL is reachable."""
        try:
            response = requests.get(self.config['base_url'])
            if response.status_code == self.config['status_code_OK']:
                logging.error("base URL is reachable. The issue might be with the specific request...")
            else:
                logging.error(f"base URL check failed with status code: {response.status_code}. Possible API issue...")
        except requests.exceptions.RequestException as e:
            logging.error(f"failed to reach the base URL. {e}")
