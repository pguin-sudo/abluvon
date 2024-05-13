import json
from typing import Type, List, TypeVar

T = TypeVar('T', bound='Model')


class Model:
    id = 'DefaultId'

    def save(self):
        # Get object as dictionary
        obj_dict = self.__dict__

        # Open or create JSON file
        try:
            with open('data/' + self.__class__.__name__ + '.json', 'r') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = {"objects": []}

        # Add object dictionary to the array
        data["objects"].append(obj_dict)

        # Write updated JSON to file
        with open('data/' + self.__class__.__name__ + '.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

    @classmethod
    def find(cls: Type[T], id: str) -> T:
        with open('data/' + cls.__name__ + '.json', 'r') as json_file:
            obj_list = json.load(json_file).get('objects')
            for obj in obj_list:
                if obj['id'] == id:
                    return cls(**obj)

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        objects = []
        try:
            with open('data/' + cls.__name__ + '.json', 'r') as json_file:
                data = json.load(json_file)
                for obj_dict in data['objects']:
                    obj = cls(**obj_dict)
                    objects.append(obj)
        except FileNotFoundError:
            print(f"File not found: {cls.__name__}.json")
        except Exception as e:
            print(f"An error occurred: {e}")
        return objects
