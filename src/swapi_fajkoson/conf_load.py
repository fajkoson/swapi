import logging
import json
import os

logger = logging.getLogger(__name__)

class ConfLoader:
    def __init__(self) -> None:
        self.file_path = self.find_conf_path()
        self.config = self.load_config()

    def find_conf_path(self) -> str:
        """find dynamic path to config.json."""
        # project root (../SWAPI)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
        # path to the config.json
        config_path = os.path.join(base_dir, 'config', 'config.json') 
        logger.info(f"config path is: {config_path}")
        return config_path

    def load_config(self) -> dict:
        """load config from JSON."""
        try:
            with open(self.file_path, 'r') as file:
                logger.info("config file has been loaded")
                return json.load(file)
        except FileNotFoundError:
            logger.exception(f"configuration file not found at {self.file_path}: {e}")
            raise
        except json.JSONDecodeError:
            logger.exception("Error decoding JSON from the configuration file.")
            raise

    def validate_config(self) -> bool:
        """validate the configuration."""
        req_param = [
            "output_path", 
            "max_person", 
            "max_planets", 
            "count_of_people_and_planet",
            "base_url", 
            "person_url",  
            "planet_url",
            "status_code_OK",
            "logging_level"
        ]

        for param in req_param:
            if param not in self.config:
                logger.error(f"missing required configuration parameter: {param}")
                raise ValueError(f"missing required configuration parameter: {param}")
            
        if "logging_level" in self.config:
            if not isinstance(self.config["logging_level"], dict):
                logger.error("logging_level must be a dictionary")
                raise ValueError("logging_level must be a dictionary")
            
            # check if each modules logging level is a valid logging level string
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            for module, level in self.config["logging_level"].items():
                if level.upper() not in valid_levels:
                    logger.error(f"invalid logging level '{level}' for module '{module}'")
                    raise ValueError(f"invalid logging level '{level}' for module '{module}'")


        # check ranges
        if not (1 <= self.config["max_person"] <= 82):
            logger.error("max_person range is 1-82")
            raise ValueError("max_person range is 1-82")
    
        if not (1 <= self.config["max_planets"] <= 60):
            logger.error("max_planets range is 1-60")
            raise ValueError("max_planets range is 1-60")
    
        return True

    def get_config(self) -> dict:
        """get the validated configuration."""
        if self.validate_config():
            logger.info("configuration has been validated")
            return self.config

if __name__ == "__main__":
    print(ConfLoader().get_config())

