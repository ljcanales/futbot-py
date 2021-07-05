from src.util.files import read_json_file

class Config:
    actual_config = None
    config_path = None

    def __init__(self, config_path):
        self.actual_config = read_json_file(config_path)
        self.config_path = config_path
    
    def update_config(self):
        if self.actual_config and self.actual_config['update_config']:
            self.actual_config = read_json_file(self.config_path)

    def is_activate(self, config_name):
        if self.actual_config and config_name in self.actual_config.keys():
            return self.actual_config[config_name]
        print('ERROR: config_name [{}]'.format(config_name))
        return False
