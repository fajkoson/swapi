import asyncio
from unittest.mock import patch
import pytest
from swpackage.sw_world import main

@pytest.mark.asyncio
async def test_start_and_fetch():
    with patch('swpackage.sw_client.SWFetcher.fetch_person', autospec=True) as mock_fetch_person, \
         patch('swpackage.sw_client.SWFetcher.fetch_planet', autospec=True) as mock_fetch_planet:
        
        mock_person_data = {'name': 'Luke Skywalker', 'height': '172'}
        mock_planet_data = {'name': 'Tatooine', 'terrain': 'desert'}
        
        mock_fetch_person.return_value = asyncio.Future()
        mock_fetch_person.return_value.set_result(mock_person_data)
        
        mock_fetch_planet.return_value = asyncio.Future()
        mock_fetch_planet.return_value.set_result(mock_planet_data)










