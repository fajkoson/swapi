import pytest
from swpackage.yaml_mngr import YamlManager

@pytest.mark.asyncio
async def test_yaml_output_format(tmp_path):
    
    file_path = tmp_path / "output.yaml"
    yaml_manager = YamlManager(str(file_path), {"count_of_people_and_planet": 5})
    
    data_to_write = {
        "people": [{"name": "Luke Skywalker", "height": "172"}], 
        "planets": [{"name": "Tatooine", "terrain": "desert"}]
    }

    await yaml_manager.write_to_yaml(data_to_write)
    read_data = await yaml_manager.read_from_yaml()
    assert read_data == data_to_write

