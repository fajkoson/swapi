import yaml
import os


class YamlManager:
    def __init__(self, output_path: str, config: dict) -> None:
        if not isinstance(output_path, str):
            raise ValueError("output path must be a string")
        
        self.output_path = output_path
        # pass also the configuration
        self.config = config 

    def write_to_yaml(self, data: dict) -> None:
        """write data to a YAML file"""
        try:
            # create dir. if it doesnt exist
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            
            # write data to yaml file
            with open(self.output_path, 'w') as file:
                yaml.dump(data, file, sort_keys=False)
            print(f"data successfully written to {self.output_path}")
        except Exception as e:
            print(f"error occurred while writing to YAML file: {e}")
    
    def read_from_yaml(self) -> dict:
        """read data from a YAML file."""
        if not os.path.exists(self.output_path):
            print(f"no existing YAML file found at {self.output_path}. start fresh.")
            # return default structure in case of non-existing file
            return {"people": [], "planets": []}  

        try:
            with open(self.output_path, 'r') as file:
                data = yaml.safe_load(file)
                if data is None:
                    print(f"existing yaml file at {self.output_path} is empty")
                    # return a default structure in case of empty file
                    return {"people": [], "planets": []}  
                # otherwise return content of the file
                return data
        except Exception as e:
            print(f"error occurred while reading from YAML file: {e}")
            # return a default structure in case of an error
            return {"people": [], "planets": []}  
    
 #   def append_to_yaml(self, new_data: dict) -> None:
 #       """append new data to existing file"""
 #       existing_data = self.read_from_yaml()
 #       for key in ["people", "planets"]:
 #           # ensure the total count does not exceed the configured limit before append
 #           while (
 #                   len(existing_data[key]) < self.config["count_of_people_and_planet"]
 #                   and len(new_data[key]) > 0
 #           ):
 #               # assuming new_data is pre-loaded with fetched items
 #               item = new_data[key].pop(0)  
 #               if item["name"].strip().lower() not in {e["name"].strip().lower() for e in existing_data[key]}:
 #                   existing_data[key].append(item)
 #       self.write_to_yaml(existing_data)
    
    def append_to_yaml(self, new_data: dict) -> None:
        """
        appends new data to the existing file, 
        with warnings if data is not appended
        """
        existing_data = self.read_from_yaml()

        # flags to track if any new data was appended
        new_data_appended = False

        for key in ["people", "planets"]:
            for item in new_data[key]:
                if len(existing_data[key]) >= self.config["count_of_people_and_planet"]:
                    # if the count has reached the limit, log a warning and skip appending
                    print(
                        f"[Warning:] the limit of {self.config['count_of_people_and_planet']} "
                        f"for {key} has been reached. No more data will be appended."
                    )
                    # exit the loop <-> limit is reached
                    break  

                # check for duplicates
                if item["name"].strip().lower() not in {e["name"].strip().lower() for e in existing_data[key]}:
                    existing_data[key].append(item)
                    new_data_appended = True
                else:
                    # log a warning if the item is a duplicate
                    print(f"[Warning:] {item['name']} is already included in {key}")

        if new_data_appended:
            # if any new data was appended, write the updated data to the file
            self.write_to_yaml(existing_data)
            print(f"new data successfully appended to {self.output_path}")
        else:
            # if no new data was appended, inform the user
            print("[Warning:] no new data was appended to the OUTPUT file")
