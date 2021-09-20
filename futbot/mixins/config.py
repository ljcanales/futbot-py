from futbot.util.files import read_json_file
from futbot.types import ConfigData

class ConfigMixin():
    _config: ConfigData

    def __init__(self, **kwargs):
        if 'config' in kwargs.keys():
            print('[CONFIG] Reading config')
            self._config = ConfigData(**kwargs['config'])
        else:
            print('[CONFIG] Loading default config')
            self._config = ConfigData()
        #super().__init__(**kwargs)

    def get_config(self) -> dict:
        return self._config.dict().copy()

    def update_config(self, settings_path = None) -> None:
        ''' update configuration, if update_config is true '''

        if self._config and self._config.update_config and settings_path:
            print('[CONFIG] Updating config from file')
            data: dict = read_json_file(settings_path)
            if data and 'config' in data.keys():
                self._config = ConfigData(**data['config'])
                print('[CONFIG] Config updated')

    def is_activated(self, config_name: str) -> bool:
        ''' Check config state given by parameter '''

        if self._config:
            try:
                return self._config.__getattribute__(config_name)
            except:
                print('ERROR: config_name [{}]'.format(config_name))
                return False
