import json


def fetch_source(config_path):
    obj = dict()
    with open(config_path) as config:
        lines = [line.rstrip() for line in config.readlines()]
        for line in lines:
            index = line.index("=")
            obj[line[:index - 1]] = line[index + 3:-1]
    return obj


def write_json(obj, result_name):
    with open(result_name, 'w') as json_file:
        json.dump(obj, json_file)


def config_py_to_json(source_path: str, result_name: str) -> None:
    try:
        obj = fetch_source(source_path)
        write_json(obj, result_name)
    except Exception as ex:
        return print(ex)


config_py_to_json("/app/config/configProduction.py", "configProduction.json")
