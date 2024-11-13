import json
import os

ASSETS_FOLDER = os.path.join(os.path.dirname(__file__), 'assets')

def load_element(file_name, element):
    file_path = os.path.join(ASSETS_FOLDER, file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data[element]

def save_element(file_name, element, value):
    file_path = os.path.join(ASSETS_FOLDER, file_name)
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    data[element] = value
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def delete_element(file_name, element):
    file_path = os.path.join(ASSETS_FOLDER, file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    if element in data:
        del data[element]
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    return False

def update_element(file_name, element, value):
    file_path = os.path.join(ASSETS_FOLDER, file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    if element in data:
        data[element] = value
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    return False