from typing import List
from models import Directory, File

class App():
    def __init__(self, path:str, cwd:Directory) -> None:
        self.path = path
        self.cwd = cwd

    def get_commands(self) -> List[str]:
        with open(self.path) as f:
            return [line.rstrip("\n") for line in f.readlines()]

    def create_directory(self, name:str, parent:Directory) -> Directory:
        return Directory(name=name, parent=parent)
    
    def create_file(self, name:str, parent:Directory, size:int, type:int) -> File:
        return File(name=name, parent=parent, size=size, type=type)

    def change_directory(self, name: str) -> None:
        target_directory = Directory.filter(parent=self.cwd, name=name)[0]
        self.cwd = target_directory

    def move_parent_directory(self) -> None:
        if self.cwd.parent:
            self.cwd = self.cwd.parent

    def move_main_directory(self) -> None:
        self.cwd = Directory.filter(parent=None)[0]

    def get_command_parameters(self, text:str)->List[str]:
        return text.lstrip("$").split()

    def execute_command(self, command:str) -> None:
        command_parameters = self.get_command_parameters(command)
        if command_parameters[0] == "cd":
            if command_parameters[1] == "..":
                self.move_parent_directory()
            elif command_parameters[1] == "/":
                self.move_main_directory
            else:
                self.change_directory(command_parameters[1])
        elif command_parameters[0] == "ls":
            pass
        elif command_parameters[0] == "dir":
            self.create_directory(name=command_parameters[1], parent=self.cwd)
        elif command_parameters[0].isnumeric():
            if "." in command_parameters[1]:
                file_name, file_type = command_parameters[1].split(".")
            else:
                file_name = command_parameters[1]
                file_type = None
            self.create_file(name=file_name, parent=self.cwd, size=int(command_parameters[0]), type=file_type)

    def run(self) -> None:
        commands = self.get_commands()
        for command in commands:
            self.execute_command(command)

if __name__ == "__main__":
    main_dir = Directory(name="/", parent=None)
    app = App(path="7/no_space.txt", cwd=main_dir)
    app.run()
    # problem part1
    small_dirs = [dir.size for dir in Directory.instances if dir.size<=100000]
    print(sum(small_dirs))
    # problem part2
    used_space = main_dir.size
    available_space = 70000000 - used_space
    required_space = 30000000 - available_space
    big_enough_sizes = [directory.size for directory in Directory.instances if directory.size >= required_space]
    print(min(big_enough_sizes))
