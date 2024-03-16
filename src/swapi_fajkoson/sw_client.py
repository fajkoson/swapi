import requests
from .conf_load import ConfLoader

config = ConfLoader().get_config()

def fetch_person(person_id):
    """
    fetch person by ID and return name and height.
    nonono..no hardcoding here boys!
    """
    url = f"{config['person_url']}{person_id}/"
    try:
        response = requests.get(url)
        # raise HTTPError if the request returned wrong code
        response.raise_for_status() 
        data = response.json()
        return {'name': data['name'], 'height': data['height']}
    except requests.exceptions.HTTPError as http_err:
        # check api if fetching fails and only then - to reduce requests
        check_base_url()
        raise Exception(f"HTTP error occurred while fetching person: {http_err}")
    except Exception as err:
        raise Exception(f"an unexpected error occurred while fetching person: {err}")

def fetch_planet(planet_id):
    """
    fetch planet by ID and return name and terrain.
    nonono..no hardcoding here boys!
    """
    url = f"{config['planet_url']}{planet_id}/"
    try:
        response = requests.get(url)
        # raise HTTPError if the request returned wrong code
        response.raise_for_status()
        data = response.json()
        return {'name': data['name'], 'terrain': data['terrain']}
    except requests.exceptions.HTTPError as http_err:
        # check api if fetching fails and only then - to reduce requests
        check_base_url()
        raise Exception(f"HTTP error occurred while fetching planet: {http_err}")
    except Exception as err:
        raise Exception(f"an unexpected error occurred while fetching planet: {err}")

def check_base_url():
    try:
        response = requests.get(config['base_url'])
        if response.status_code == config['status_code_OK']:
            print("base URL is reachable. The issue might be with the specific request...")
        else:
            print(f"base URL check failed with status code: {response.status_code}. Possible API issue...")
    except requests.exceptions.RequestException as e:
        print(f"failed to reach the base URL. Error: {e}")
