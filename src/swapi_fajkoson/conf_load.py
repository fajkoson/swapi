import json
import os

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
        return config_path

    def load_config(self) -> dict:
        """load config from JSON."""
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"configuration file not found at {self.file_path}")
        except json.JSONDecodeError:
            raise Exception("error decoding JSON from the configuration file.")

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
            "status_code_OK" 
        ]

        for param in req_param:
            if param not in self.config:
                raise ValueError(f"missing required configuration parameter: {param}")
    
        # check ranges
        if not (1 <= self.config["max_person"] <= 82):
            raise ValueError("max_person range is 1-82")
    
        if not (1 <= self.config["max_planets"] <= 60):
            raise ValueError("max_planets range is 1-60")
    
        return True

    def get_config(self) -> dict:
        """get the validated configuration."""
        if self.validate_config():
            return self.config

if __name__ == "__main__":
    print(ConfLoader().get_config())

