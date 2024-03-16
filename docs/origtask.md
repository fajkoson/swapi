# Star Wars testing application

## Specification:

### Must have:
- generate list of people and planets from Star Wars world in provided range from configuration below
- use open source API https://swapi.dev/ - there is 10 000 rate limit per day for each ip address - a lot of space of testing
- get info about people /people/{random_choice} and planets /planets/{random_choice} from this API
- create json config file with output path, max range of people and planet
- example of config.json
```bash
{
  "output_path": "C:\SW_OUTPUT",
  "max_person": 5,  # Range of maximum people from swapi.dev (1-82)
  "max_planets": 5  # Range of maximum planet from swapi.dev (1-60)
  "count_of_people_and_planet": 3
}
```
- create argument of time interval between each call of people and planet - int seconds of delay
```bash
  sw_world.py --interval 5
```
- every interval get information about single randomly choosen person and planet up to max_person and max_planets configuration
- store info about person name and height and planet name and terrain into output yaml file
- example of output.yaml
```bash
people:
  - name: Luke Skywalker
    height: 172
planets:
  - name: Tatooine
    terrain: desert
```
- append new information into output.yaml
- if person or planet is already in yaml or number of people or planet reach `count_of_people_and_planet` do not store new information but only log warning message
- end script when output.yaml contains exactly number of people and planets from configuraiton key `count_of_people_and_planet`

### Optional (but you can get some extra points):
- use package manager and create python app
- call people and planet endpoint asynchronously using asyncio and aiohttp (whole app could be written as async)
- write basic tests (app is able to starts) for sw world app and output yaml data has correct format
- mock calling sw api in tests
- add mypy check within tests
- create dockerfile for creating app docker image


- last extra task is not directly connected to sw world app
  - create example of proto file with one service and one call
  - using grpcio-tools library parse proto file and get name of service and call (could be standalone script)
