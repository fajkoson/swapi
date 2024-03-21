import aiofiles
import asyncio
import yaml
import os
import logging
from swpackage.decorators import time_decorator


logger = logging.getLogger(__name__)

class YamlManager:
    """ handles yaml file operations"""

    def __init__(self, output_path: str, config: dict) -> None:
        if not isinstance(output_path, str):
            logger.error(f"initialization failed: {output_path} must be a string.")
            raise ValueError("output path must be a string")
        
        self.output_path = output_path
        # pass also the configuration
        self.config = config

    @time_decorator
    async def write_to_yaml(self, data: dict) -> None:
        """write data to a YAML file"""
        try:
            # create dir. if it doesnt exist
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            # convert the data into yaml first before writting
            yaml_data = yaml.dump(data, sort_keys=False)
            # write data to yaml file
            async with aiofiles.open(self.output_path, 'w') as file:
                await file.write(yaml_data)
            logger.info("data written correctly")
        except Exception as e:
            logger.error(f"while writing to YAML file: {e}")

    @time_decorator
    async def read_from_yaml(self) -> dict:
        """read data from a YAML file."""
        if not os.path.exists(self.output_path):
            return {"people": [], "planets": []}  

        try:
            async with aiofiles.open(self.output_path, 'r') as file:
                data = yaml.safe_load(await file.read()) or {"people": [], "planets": []}
                if data is None:
                    logger.info(f"existing yaml file at {self.output_path} is empty")
                    # return a default structure in case of empty file
                    return {"people": [], "planets": []}  
                # otherwise return content of the file
                return data
        except Exception as e:
            logger.error(f"error occurred while reading from YAML file: {e}")
            # return a default structure in case of an error
            return {"people": [], "planets": []}
          
    @time_decorator      
    async def append_to_yaml(self, new_data: dict) -> None:
        """
        appends new data to the existing file, 
        with warnings if data is not appended
        """
        existing_data = await self.read_from_yaml()

        # flag to track if any new data was appended
        new_data_appended = False

        for key in ["people", "planets"]:
            existing_names = {item["name"].strip().lower() for item in existing_data[key]}

            for item in new_data[key]:
                normalized_new_name = item["name"].strip().lower()

                if len(existing_data[key]) >= self.config["count_of_people_and_planet"]:
                    # if the count has reached the limit, log a warning and skip appending
                    logger.warning(
                        f"the limit of {self.config['count_of_people_and_planet']} "
                        f"for {key} has been reached. No more data will be appended."
                    )
                    # exit the loop <-> limit is reached
                    break  

                # check for duplicates
                if normalized_new_name not in existing_names:
                    existing_data[key].append(item)
                    new_data_appended = True
                else:
                    # log a warning if the item is a duplicate
                    logger.warning(f"{item['name']} is already included in {key}")

        if new_data_appended:
            # if any new data was appended, write the updated data to the file
            await self.write_to_yaml(existing_data)
            logger.info(f"new data successfully appended to {self.output_path}")
        else:
            # if no new data was appended, inform the user
            logger.warning("no new data was appended to the OUTPUT file")

    @time_decorator 
    async def has_new_data_to_append(self, new_data: dict) -> bool:
        """
        this method checks if there are any items in the new data that are not
        already present in the existing YAML data. It considers data unique based
        on the 'name' attribute of each item, ignoring case and leading/trailing spaces.
        """
        # first, read the existing data from the YAML file.
        existing_data = await self.read_from_yaml()

        # iterate through each category
        for key in ["people", "planets"]:
            # extract a set
            existing_names = set()

            if key in existing_data:
                for item in existing_data[key]:
                    # normalize the name of the current item and add it to the set of existing names
                    normalized_name = item["name"].strip().lower()
                    existing_names.add(normalized_name)

            # now, iterate through each item in the new data for this category
            for item in new_data[key]:
                # normalize the name of the current item for comparison
                normalized_new_name = item["name"].strip().lower()

                # check if this normalized new name is not in the set of existing names
                if normalized_new_name not in existing_names:
                    # if not, we've found new unique data. Return True immediately
                    return True

        # if we reach this point, it means we didnt find any new unique data in any category
        # return False to indicate this
        return False
