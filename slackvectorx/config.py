import os
import json

class Config:
    def __init__(self, filename="config.json"):
        data_dir = os.getenv("DATA_DIR", "/data")
        try:
            with open(filename) as f:
                self.config = json.load(f)
                self.config["DATA_DIR"] = data_dir
        except FileNotFoundError:
            print("Error: config.json not found")
            self.config = {}
        except json.decoder.JSONDecodeError:
            print("Error: config.json is not a valid JSON file")
            self.config = {}
        except Exception as e:
            print("Error: {}".format(e))
            self.config = {}

    def get(self, key):
        try:
            return self.config[key]
        except KeyError:
            print("Error: key not found")
            return None
