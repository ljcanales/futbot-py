import json

def read_json_file(path_file: str, object_hook=None) -> dict:
    ''' Read a json file '''

    try:
        with open(path_file, 'r', encoding='utf8') as json_file:
            return json.load(json_file, object_hook=object_hook)
    except:
        return None

def write_json_file(data: dict, path_file: str, default=None) -> None:
    ''' Write a json file '''

    from pathlib import Path

    path_user = Path(path_file)
    path_user.parent.mkdir(exist_ok=True)

    with open(path_file, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=True, default=default)
