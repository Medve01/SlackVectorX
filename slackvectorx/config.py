import os
import json
import dotenv

class Config:
    def __init__(self, filename="config.json"):
        data_dir = dotenv.get_key('.env', 'DATA_DIR')
        openai_api_key = dotenv.get_key('.env', 'OPENAI_API_KEY')
        slack_bot_token = dotenv.get_key('.env', 'SLACK_BOT_TOKEN')
        slack_app_token = dotenv.get_key('.env', 'SLACK_APP_TOKEN')
        slack_signing_secret = dotenv.get_key('.env', 'SLACK_SIGNING_SECRET')
        try:
            with open(filename) as f:
                self.config = json.load(f)
                self.config["DATA_DIR"] = data_dir
                self.config["OPENAI_API_KEY"] = openai_api_key
                self.config["SLACK_BOT_TOKEN"] = slack_bot_token
                self.config["SLACK_APP_TOKEN"] = slack_app_token
                self.config["SLACK_SIGNING_SECRET"] = slack_signing_secret
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
