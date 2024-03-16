import argparse
import random
from time import sleep
from .conf_load import ConfLoader
from .sw_client import fetch_person, fetch_planet
from .yaml_mngr import YamlManager

def main(interval=5):
    config = ConfLoader().get_config()
   
    # YAML manager init. with output path
    yaml_manager = YamlManager(config["output_path"] + "\\output.yaml")

    output_data = {
        "people": [],
        "planets": []
    }

    # generate and fetch data, check for duplicities..
    while (len(output_data["people"]) < config["count_of_people_and_planet"] or
           len(output_data["planets"]) < config["count_of_people_and_planet"]):
        if len(output_data["people"]) < config["count_of_people_and_planet"]:
            person_id = random.randint(1, config["max_person"])
            try:
                person = fetch_person(person_id)
                if not any(p["name"] == person["name"] for p in output_data["people"]):
                    print(f"fetching person with ID: {person_id} - {person['name']}")
                    output_data["people"].append({"name": person["name"], "height": person["height"]})
                else:
                    print(f"warning: Person '{person['name']}' is already included.")
            except Exception as e:
                print(f"an error occurred while fetching person with ID {person_id}: {e}")

        if len(output_data["planets"]) < config["count_of_people_and_planet"]:
            planet_id = random.randint(1, config["max_planets"])
            try:
                planet = fetch_planet(planet_id)
                if not any(p["name"] == planet["name"] for p in output_data["planets"]):
                    print(f"fetching planet with ID: {planet_id} - {planet['name']}")
                    output_data["planets"].append({"name": planet["name"], "terrain": planet["terrain"]})
                else:
                    print(f"warning: Planet '{planet['name']}' is already included.")
            except Exception as e:
                print(f"an error occurred while fetching planet with ID {planet_id}: {e}")

        # wait for interval [sec]
        sleep(interval)

        # break the loop if both limits were reached
        if (len(output_data["people"]) >= config["count_of_people_and_planet"] and
            len(output_data["planets"]) >= config["count_of_people_and_planet"]):

            break

    # write the output into file
    yaml_manager.write_to_yaml(output_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='fetch SWAPI data.')
    parser.add_argument('--interval', type=int, default=5, help='interval in seconds')
    args = parser.parse_args()
    main(args.interval)


