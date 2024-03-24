import aiofiles
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
        self.config = config

    @time_decorator
    async def write_to_yaml(self, data: dict) -> None:
        """write data to a YAML file"""
        try:
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            yaml_data = yaml.dump(data, sort_keys=False)

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
                    return {"people": [], "planets": []}  
                return data
        except Exception as e:
            logger.error(f"error occurred while reading from YAML file: {e}")
            return {"people": [], "planets": []}
          
    @time_decorator      
    async def append_to_yaml(self, new_data: dict) -> None:
        """
        appends new data to the existing file, 
        with warnings if data is not appended
        """
        existing_data = await self.read_from_yaml()

        new_data_appended = False

        for key in ["people", "planets"]:
            existing_names = {item["name"].strip().lower() for item in existing_data[key]}

            for item in new_data[key]:
                normalized_new_name = item["name"].strip().lower()

                if len(existing_data[key]) >= self.config["count_of_people_and_planet"]:

                    logger.warning(
                        f"the limit of {self.config['count_of_people_and_planet']} "
                        f"for {key} has been reached. No more data will be appended."
                    )

                    break  

                if normalized_new_name not in existing_names:
                    existing_data[key].append(item)
                    new_data_appended = True
                else:
                    logger.warning(f"{item['name']} is already included in {key}")

        if new_data_appended:
            await self.write_to_yaml(existing_data)
            logger.info(f"new data successfully appended to {self.output_path}")
        else:
            logger.warning("no new data was appended to the OUTPUT file")

    @time_decorator 
    async def has_new_data_to_append(self, new_data: dict) -> bool:
        """
        this method checks if there are any items in the new data that are not
        already present in the existing YAML data. It considers data unique based
        on the 'name' attribute of each item, ignoring case and leading/trailing spaces.
        """

        existing_data = await self.read_from_yaml()

        for key in ["people", "planets"]:
            existing_names = set()

            if key in existing_data:
                for item in existing_data[key]:
                    normalized_name = item["name"].strip().lower()
                    existing_names.add(normalized_name)

            for item in new_data[key]:
                normalized_new_name = item["name"].strip().lower()

                if normalized_new_name not in existing_names:
                    return True
        return False
