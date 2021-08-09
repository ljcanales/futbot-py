from typing import Dict
from src.util.files import read_json_file, write_json_file
from src.constants import file_path
from src.types import ConfigData

class ConfigMixin():
    _config: ConfigData

    def __init__(self):
        self._config = self.__read_config()
    
    def __read_config(self) -> ConfigData:
        print('[CONFIG] Reading config file')
        data: Dict = read_json_file(file_path.CONFIG)
        if data:
            return ConfigData(**data)
        else:
            default_config: ConfigData = ConfigData()
            write_json_file(default_config.dict(), file_path.CONFIG)
            print('[CONFIG] New config file created')
            return default_config
    
    def update_config(self) -> None:
        ''' update configuration, if update_config is true '''

        if self._config and self._config.update_config:
            self._config = self.__read_config()

    def is_activated(self, config_name: str) -> bool:
        ''' Check config state given by parameter '''

        if self._config:
            try:
                return self._config.__getattribute__(config_name)
            except:
                print('ERROR: config_name [{}]'.format(config_name))
                return False
