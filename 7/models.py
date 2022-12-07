from typing import List

class Model():
    @classmethod
    def filter(cls, **kwargs) -> List:
        return [obj for obj in cls.instances 
            if all(getattr(obj, key) == value for key, value in kwargs.items())]

class Directory(Model):
    instances = []

    def __init__(self, parent, name:str) -> None:
        self.parent = parent
        self.name = name
        Directory.instances.append(self)

    def __str__(self) -> None:
        return f"dir {self.name}"

    def get_subdirectories(self):
        return self.filter(parent=self)

    def get_files(self):
        return File.filter(parent=self)

    def list_children(self):
        directories = self.get_subdirectories()
        files = self.get_files()
        for item in directories + files:
            print(item)

    @property
    def size(self):
        size = 0
        files = self.get_files()
        subdirectories = self.get_subdirectories()
        for file in files:
            size += file.size
        for subdirectory in subdirectories:
            size += subdirectory.size
        return size

class File(Model):
    instances = []

    def __init__(self, parent, name:str, size:int, type:str) -> None:
        self.parent = parent
        self.name = name
        self.size = size
        self.type = type
        File.instances.append(self)

    def __str__(self) -> None:
        if self.type:
            return f"{self.size} {self.name}.{self.type}"
        else: 
            return f"{self.size} {self.name}"