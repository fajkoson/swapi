import yaml
import os

class YamlManager:
    def __init__(self, output_path: str) -> None:
        if not isinstance(output_path, str):
            raise ValueError("output path must be a string")
        
        self.output_path = output_path

    def write_to_yaml(self, data: dict) -> None:
        """write data to a YAML file"""
        try:
            # create dir. if it doesnt exist
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            
            # write data to YAML file
            with open(self.output_path, 'w') as file:
                yaml.dump(data, file, sort_keys=False)
            print(f"data successfully written to {self.output_path}")
        except Exception as e:
            print(f"Error occurred while writing to YAML file: {e}")
