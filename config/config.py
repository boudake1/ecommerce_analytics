import yaml

class Config:

    def __init__(self, file_path):

        with open(file_path) as file:
            self.config = yaml.safe_load(file)

    def get(self, key):
        return self.config[key]