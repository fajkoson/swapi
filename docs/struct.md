SWAPI/
|-- docs/
|   |-- origtask.md              # task requirements
|   |-- struct.md                # structure documentation
|   |-- docker.md                # guide for docker
|
|-- src/
|   |--config/
|   |   |-- config.json          # configuration
|   |
|   |-- swpackage/
|   |   |-- __init__.py
|   |   |-- conf_load.py         # config loader
|   |   |-- sw_world.py          # main function
|   |   |-- sw_client.py         # SWAPI client connecting to the API
|   |   |-- yaml_mngr.py         # manages YAML output
|   |   |-- decorators.py        # some decorators
|   |
|   |-- swpackage-tests/                  
|       |-- __init__.py   
|       |-- test_conf_load.py    # config loader
|       |-- test_sw_world.py     # main function
|       |-- test_sw_client.py    # SWAPI client connecting to the API
|       |-- test_yaml_mngr.py    # manages YAML output
|       |-- test_decorators.py   # some decorators
|
|
|-- .dockerignore
|-- .gitignore
|-- MANIFEST.in                  # include for config.json
|-- setup.py
|-- Dockerfile                
|-- EOF