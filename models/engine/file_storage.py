#!/usr/bin/python3
""" serialization and deserialization of instances to & from json"""


import json
import os


class FileStorage():
    """ class FileStorage"""
    __file_path = "file.json"
    __objects = {}
    """ classes = {
            "Place": Place, "State": State, "City": City,
            "Amenity": Amenity, "Review": Review
            }
    """

    def all(self):
        """ return dictionary of objects """
        return self.__objects

    def new(self, obj):
        """ assigns objects """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """ save objects to json file """
        dic = {}
        for key, obj in self.__objects.items():
            dic[key] = obj.to_dict()
        with open(self.__file_path, 'w', encoding="utf-8") as file:
            json.dump(dic, file)

    def reload(self):
        """ loads objects from existing file.jason """
        # This import is uses here to prevent circular import
        from models.base_model import BaseModel
        from models.user import User
        from models.amenity import Amenity
        from models.city import City
        from models.place import Place
        from models.state import State
        from models.review import Review

        # a class mapping dictionary to get the class

        cls_dic = {'BaseModel': BaseModel, 'User': User,
                   'Amenity': Amenity, 'City': City,
                   'Place': Place, 'State': State,
                   'Review': Review}

        j_file = os.path.exists(self.__file_path)
        if j_file:
            with open(self.__file_path, 'r', encoding="utf-8") as file:
                new = json.load(file)
                for key, obj_dic in new.items():
                    get_class = obj_dic.get('__class__')
                    obj_class = cls_dic[get_class]
                    obj = obj_class(**obj_dic)
                    self.new(obj)
