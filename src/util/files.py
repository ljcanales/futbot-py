import json

def read_json_file(path_file, object_hook=None):
    """
    Read a file
    :param object_hook:
    :param path_file:
    :return:
    """
    with open(path_file, 'r', encoding='utf8') as json_file:
        return json.load(json_file, object_hook=object_hook)

def write_json_file(data, path_file, default=None):
    """
    Write a file
    :param default:
    :param data:
    :param path_file:
    :return:
    """
    from pathlib import Path

    path_user = Path(path_file)
    path_user.parent.mkdir(exist_ok=True)

    with open(path_file, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=True, default=default)