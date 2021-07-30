from typing import Dict
from src.util.files import read_json_file

class Config:
    _actual_config: Dict[str, bool] = {}
    config_path: str = ''

    def __init__(self, config_path):
        self._actual_config = read_json_file(config_path)
        self.config_path = config_path
    
    def update_config(self) -> None:
        ''' update configuration, if update_config is true '''

        if self._actual_config and self._actual_config['update_config']:
            self._actual_config = read_json_file(self.config_path)

    def is_activated(self, config_name: str) -> bool:
        ''' Check config state given by parameter '''

        if self._actual_config and config_name in self._actual_config.keys():
            return self._actual_config[config_name]
        print('ERROR: config_name [{}]'.format(config_name))
        return False
