import json

CONFIG_FILE = 'config.json'


def load_shops():
    try:
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file).get('shops', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_shops(shops):
    config = load_shops()
    config_data = {"shops": shops}

    with open(CONFIG_FILE, 'w') as file:
        json.dump(config_data, file, ensure_ascii=False, indent=4)