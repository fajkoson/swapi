import argparse
import random
import logging
import asyncio
from swpackage.conf_load import ConfLoader
from swpackage.sw_client import SWFetcher
from swpackage.yaml_mngr import YamlManager
from swpackage.decorators import time_decorator

@time_decorator
async def main(interval=5) -> None:
    config = ConfLoader().get_config()
    # basic log config
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S'
    )

    logger = logging.getLogger(__name__)

    for module, level_str in config.get("logging_level", {}).items():
        level = getattr(logging, level_str.upper(), None)
        if level is not None:
            specific_logger = logging.getLogger(module)
            specific_logger.setLevel(level)
            specific_logger.propagate = True
        else:
            logging.warning(f"invalid logging level: {level_str} for module: {module}")

    # yaml manager init. with output path
    # added config due to another parameter in YamlManager
    yaml_manager = YamlManager(config["output_path"] + "\\output.yaml", config)

    output_data = {
        "people": [],
        "planets": []
    }

    fetcher = SWFetcher(config) 

    # generate and fetch data, check for duplicities..
    while (len(output_data["people"]) < config["count_of_people_and_planet"] or
           len(output_data["planets"]) < config["count_of_people_and_planet"]):
        if len(output_data["people"]) < config["count_of_people_and_planet"]:
            person_id = random.randint(1, config["max_person"])
            try:
                person = await fetcher.fetch_person(person_id)
                if not any(p["name"] == person["name"] for p in output_data["people"]):
                    logger.info(f"fetching person with ID: {person_id} - {person['name']}")
                    output_data["people"].append({"name": person["name"], "height": person["height"]})
                else:
                    logger.warning(f"person '{person['name']}' is already included.")
            except Exception as e:
                logger.error(f"an error occurred while fetching person with ID {person_id}: {e}")

        if len(output_data["planets"]) < config["count_of_people_and_planet"]:
            planet_id = random.randint(1, config["max_planets"])
            try:
                planet = await fetcher.fetch_planet(planet_id)
                if not any(p["name"] == planet["name"] for p in output_data["planets"]):
                    logger.info(f"fetching planet with ID: {planet_id} - {planet['name']}")
                    output_data["planets"].append({"name": planet["name"], "terrain": planet["terrain"]})
                else:
                    logger.warning(f"planet '{planet['name']}' is already included")
            except Exception as e:
                logger.error(f"an error occurred while fetching planet with ID {planet_id}: {e}")

        # wait for interval [sec]
        await asyncio.sleep(interval)

        # break the loop if both limits were reached
        if (len(output_data["people"]) >= config["count_of_people_and_planet"] and
            len(output_data["planets"]) >= config["count_of_people_and_planet"]):

            break
    # check if there anything to new append
    if await yaml_manager.has_new_data_to_append(output_data):
        # append the data instead of overwriting the file
        await yaml_manager.append_to_yaml(output_data)
    else:
        logger.warning("no new unique data to append. The OUTPUT file remains unchanged")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='fetch SWAPI data.')
    parser.add_argument('--interval', type=int, default=5, help='interval in seconds')
    args = parser.parse_args()
    #main(args.interval)
    asyncio.run(main(args.interval))

def run_main():
    """entry point for setup tools"""
    parser = argparse.ArgumentParser(description='fetch SWAPI data.')
    parser.add_argument('--interval', type=int, default=5, help='interval in seconds')
    args = parser.parse_args()
    asyncio.run(main(args.interval))