from typing import Dict
from src.util.files import read_json_file
from src.constants import file_path
from src.types import BotModel, ConfigData

class ConfigMixin(BotModel):
    _config: ConfigData

    def __init__(self):
        self._config = self.__read_config()
    
    def __read_config(self) -> ConfigData:
        data: Dict = read_json_file(file_path.CONFIG)
        if data:
            return ConfigData(**data)
        else:
            return ConfigData()

    
    def update(self) -> None:
        ''' update configuration, if update_config is true '''

        if self._config and self._config.update_config:
            self._config = self.__read_config()

        super().update()

    def is_activated(self, config_name: str) -> bool:
        ''' Check config state given by parameter '''

        if self._config:
            try:
                return self._config.__getattribute__(config_name)
            except:
                print('ERROR: config_name [{}]'.format(config_name))
                return False
