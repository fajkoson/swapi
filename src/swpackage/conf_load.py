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

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  

        config_path = os.path.join(base_dir, 'config', 'config.json') 
        logger.info(f"config path is: {config_path}")
        return config_path

    def load_config(self) -> dict:
        """load config from JSON."""  
        try:
            with open(self.file_path, 'r') as file:
                self.config = json.load(file)
                logger.info("config file has been loaded")

            running_in_container = os.getenv("RUNNING_IN_CONTAINER", "false").lower() == "true"

            if running_in_container:
                output_dir = self.config.get('container_output_path', '/app/data')
            else:
                output_dir = self.config.get('default_output_path', 'C:\\SW_OUTPUT')

            output_dir = os.path.normpath(output_dir)
            self.config['output_path'] = os.path.join(output_dir, 'output.yaml')
            return self.config
        
        except FileNotFoundError as e:
            logger.exception(f"configuration file not found at {self.file_path}: {e}")
            raise e
        except json.JSONDecodeError as e:
            logger.exception("Error decoding JSON from the configuration file.")
            raise e

    def validate_config(self) -> bool:
        """validate the configuration."""
        req_param = [
            "default_output_path",
            "container_output_path", 
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
                return False
            
        if "logging_level" in self.config:
            if not isinstance(self.config["logging_level"], dict):
                logger.error("logging_level must be a dictionary")
                return False
            
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "EXCEPTION"]
            for module, level in self.config["logging_level"].items():
                if level.upper() not in valid_levels:
                    logger.error(f"invalid logging level '{level}' for module '{module}'")
                    return False

        if not (1 <= self.config["max_person"] <= 82):
            logger.error("max_person range is 1-82")
            return False
    
        if not (1 <= self.config["max_planets"] <= 60):
            logger.error("max_planets range is 1-60")
            return False
    
        return True

    def get_config(self) -> dict:
        """get the validated configuration."""
        if self.validate_config():
            logger.info("configuration has been validated")
            return self.config
        else:
            logger.error("configuration validation failed")
            raise ValueError("configuration validation failed")

if __name__ == "__main__":
    print(ConfLoader().get_config())

