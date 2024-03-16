import yaml
import os

class YamlManager:
    def __init__(self, output_path):
        self.output_path = output_path

    def update_output_path(self, new_path):
        """update the output path for the YAML file"""
        self.output_path = new_path

    def write_to_yaml(self, data):
        """write the data to a YAML file"""
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, 'w') as file:
            yaml.dump(data, file, sort_keys=False)
